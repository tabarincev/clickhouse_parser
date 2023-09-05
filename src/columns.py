from pyparsing import *

from src.keywords import *
from src.literals import *

from src.utils.infix_processing import (
    UnaryOperator, BinaryOperator, BetweenOperator,
    IsInLikeOperator
)

ParserElement.enable_left_recursion()


class ColumnExprTerm:
    def __init__(
        self,
        column_expr: ParserElement,
        select_union_statement: ParserElement
    ):
        self._column_expr = column_expr
        self._select_union_statement = select_union_statement

    @property
    def notation(self) -> ParserElement:
        return (
            MatchFirst([
                self.case,
                # self.cast,
                self.date,
                self.extract,
                self.interval,
                self.substring,
                self.timestamp,
                # self.trim,
                # self.window_function,
                # self.window_function_target,
                self.function,
                # self.lambda_function,
                self.asterisk,
                self.column_identifier,
                self.literal,
                self.select_union_statement,
                self.parens,
                self.tuple_,
                self.array_
            ])('term')
            + Optional(LBRACKET + self._column_expr('index') + RBRACKET)
            + Optional(Optional(AS) + identifier('alias'))
        ).set_parse_action(
            lambda term: (
                {'index_term': {'term': term['term'], 'index': term['index']}}
                if term.get('index') else term['term']
            ) | ({'alias': term['alias'][0]} if term.get('alias') else {})
        )

    @property
    def case(self) -> ParserElement:
        case_else = (
            ELSE + self._column_expr('else_expr')
        ).set_parse_action(
            lambda term: {'else': term['else']}
        )

        return (
            CASE
            + Optional(identifier('identifier'))
            + OneOrMore(
                (
                    (WHEN + self._column_expr('expr')).set_parse_action(
                        lambda term: {'when': term['expr']}
                    )('when')
                    + (THEN + self._column_expr('expr')).set_parse_action(
                        lambda term: {'then': term['expr']}
                    )('then')
                ).set_parse_action(
                    lambda term: {'case': term['when'] | term['then']}
                )
            )('cases')
            + Optional(
                (ELSE + self._column_expr('expr')).set_parse_action(
                    lambda term: term['expr']
                )('else')
            )
            # + Optional(case_else('else'))
            + END
        ).set_parse_action(
            lambda term: {
                'case_term': (
                    ({'identifier': term['identifier'][0]}
                     if term.get('identifier') else {})
                    | ({'cases': term['cases'].as_list()})
                    | ({'else': term['else']}
                       if term.get('else') else {})
                )
            }
        )

    @property  # todo cast_type_expr
    def cast(self) -> ParserElement:
        return CAST + LPAR + self._column_expr('cast_object') + AS  # + column_type_expr + RPAR

    @property
    def date(self) -> ParserElement:
        return (DATE + string_literal('date_string')).set_parse_action(
            lambda term: {'date_term': term['date_string']}
        )

    @property
    def extract(self) -> ParserElement:
        return (
            EXTRACT
            + LPAR
            + MatchFirst([
                SECOND,
                MINUTE,
                HOUR,
                DAY,
                WEEK,
                MONTH,
                QUARTER,
                YEAR
            ])('date_type')
            + FROM + self._column_expr('extract_from')
            + RPAR
        ).set_parse_action(
            lambda term: {
                'extract_term': {
                    'extract_type': term['date_type'],
                    'extract_from': term['extract_from']
                }
            }
        )

    @property
    def interval(self) -> ParserElement:
        return (
            INTERVAL + self._column_expr('interval_expr')
            + MatchFirst([
                SECOND,
                MINUTE,
                HOUR,
                DAY,
                WEEK,
                MONTH,
                QUARTER,
                YEAR
            ])('date_type')
        ).set_parse_action(
            lambda term: {
                'interval_term': {
                    'expr': term['interval_expr'],
                    'date_type': term['date_type']
                }
            }
        )

    @property  # todo test
    def substring(self) -> ParserElement:
        return (
            SUBSTRING
            + LPAR
            + self._column_expr('string')
            + FROM + self._column_expr('substring_from')
            + Optional(FOR + self._column_expr('for_expr'))
            + RPAR
        ).set_parse_action(
            lambda term: {
                'substring_term': {
                    'string': term['string'],
                    'substring_from': term['substring_from']
                } | ({'for': term['for']} if term.get('for') else {})
            }
        )

    @property
    def timestamp(self) -> ParserElement:
        return (TIMESTAMP + string_literal('timestamp_string')).set_parse_action(
            lambda term: {'timestamp_term': term['timestamp_string']}
        )

    @property  # todo test
    def trim(self) -> ParserElement:
        return (
            TRIM
            + LPAR
            + MatchFirst([
                BOTH,
                LEADING,
                TRAILING
            ])('type')
            + string_literal('string')
            + FROM + self._column_expr('from_expr')
            + RPAR
        ).set_parse_action(
            lambda term: {
                'trim_term': {
                    'string': term['string'],
                    'type': term['type'],
                    'from_expr': term['from_expr']
                }
            }
        )

    @property  # todo WindowExpr
    def window_function(self) -> ParserElement:
        return (
            identifier('window_identifier')
            + LPAR + delimited_list(self._column_expr)('window_args') + RPAR
            + OVER + LPAR  # todo WindowExpr()
            + RPAR
        )

    @property  # todo test
    def window_function_target(self) -> ParserElement:
        return (
            identifier('identifier')
            + LPAR + delimited_list(self._column_expr)('args') + RPAR
            + OVER + identifier('over_identifier')
        ).set_parse_action(
            lambda term: {
                'window_function_target_term': {
                    'identifier': term['identifier'],
                    'args': term['args'],
                    'over_identifier': term['over_identifier']
                }
            }
        )

    @property
    def function(self) -> ParserElement:
        return (
            function_name('function_name')
            + LPAR
            + Optional(
                Optional(DISTINCT('distinct'))
                + delimited_list(
                    MatchFirst([
                        self.lambda_function,
                        self._column_expr
                    ])
                )('column_arg_expr')
            )
            + RPAR
        ).set_parse_action(
            lambda term: {
                'function_term': {
                    'name': term['function_name'],
                    'args': term['column_arg_expr'].as_list() if term.get('column_arg_expr') else []
                } | ({'distinct': True} if term.get('distinct') else {})
            }
        )

    @property  # todo test
    def lambda_function(self) -> ParserElement:
        return (
            MatchFirst([
                LPAR + delimited_list(identifier)('identifiers_list') + RPAR,
                delimited_list(identifier)('identifiers_list')
            ])
            + ARROW + self._column_expr('lambda_expr')
        ).set_parse_action(
            lambda term: {
                'lambda_function_term': {
                    'identifiers_list': term['identifiers_list'],
                    'expr': term['lambda_expr']
                }
            }
        )

    @property
    def asterisk(self) -> ParserElement:
        return MatchFirst([
            (
                table('table')
                + DOT + ASTERISK
            ).set_parse_action(
                lambda term: {
                    'asterisk_term': {
                        'table': term['table'],
                        'column': '*'
                    }
                }
            ),
            ASTERISK.set_parse_action(
                lambda term: {
                    'asterisk_term': {
                        'column': '*'
                    }
                }
            )
        ])

    @property
    def column_identifier(self) -> ParserElement:
        return MatchFirst([
            (
                database('database') + DOT
                + table('table') + DOT
                + column('column')
            ).set_parse_action(
                lambda term: {
                    'column_term': {
                        'database': term['database'],
                        'table': term['table'],
                        'column': term['column']
                    }
                }
            ),
            (
                table('table') + DOT
                + column('column')
            ).set_parse_action(
                lambda term: {
                    'column_term': {
                        'table': term['table'],
                        'column': term['column']
                    }
                }
            ),
            (
                column('column')
            ).set_parse_action(
                lambda term: {
                    'column_term': {
                        'column': term['column']
                    }
                }
            )
        ])

    @property
    def literal(self) -> ParserElement:
        return MatchFirst([
            Word(nums)('num'),
            string_literal('string'),
            NULL('null')
        ]).set_parse_action(
            lambda term: {
                'literal_term': (
                    {'numeric': term['num']} if term.get('num') else {}
                    | {'string': term['string']} if term.get('string') else {}
                    | {'literal': 'NULL'} if term.get('null') else {}
                )
            }
        )

    @property  # todo
    def select_union_statement(self) -> ParserElement:
        return self._select_union_statement

    @property
    def parens(self) -> ParserElement:
        return (
            LPAR + self._column_expr('term') + RPAR
        ).set_parse_action(
            lambda term: {
                'parens_term': {
                    'term': term['term']
                }
            }
        )

    @property
    def tuple_(self) -> ParserElement:
        return (
            LPAR
            + Optional(delimited_list(self._column_expr)('args'))
            + RPAR
        ).set_parse_action(
            lambda term: {
                'tuple_term': {
                    'args': term['args'].as_list() if term.get('args') else []
                }
            }
        )

    @property
    def array_(self) -> ParserElement:
        return (
            LBRACKET
            + Optional(delimited_list(self._column_expr)('args'))
            + RBRACKET
        ).set_parse_action(
            lambda term: {
                'array_term': {
                    'args':  (
                        term['args'].as_list()
                        if term.get('args') else []
                    )
                }
            }
        )


class ColumnExpr:
    def __init__(
        self,
        column_expr: ParserElement,
        select_union_statement: ParserElement
    ):
        self._column_expr = column_expr
        self._select_union_statement = select_union_statement

    @property
    def notation(self) -> ParserElement:
        self._column_expr << infix_notation(
            self.term, [
                (
                    MatchFirst([
                        DASH,
                        PLUS,
                        NOT
                    ]),
                    1, opAssoc.RIGHT, UnaryOperator
                ),
                (
                    MatchFirst([
                        ASTERISK,
                        SLASH,
                        PERCENT
                    ]),
                    2, opAssoc.LEFT, BinaryOperator
                ),
                (
                    MatchFirst([
                        PLUS,
                        DASH,
                        CONCAT
                    ]),
                    2, opAssoc.LEFT, BinaryOperator
                ),
                (
                    MatchFirst([
                        EQ_DOUBLE,
                        EQ_SINGLE,
                        NOT_EQ,
                        LE,
                        GE,
                        LT,
                        GT
                    ]),
                    2, opAssoc.LEFT, BinaryOperator
                ),
                (
                    MatchFirst([
                        Group(IS + Optional(NOT)),
                        Group(Optional(GLOBAL) + Optional(NOT) + IN),
                        Group(Optional(NOT) + (LIKE | ILIKE))
                    ]),
                    2, opAssoc.LEFT, IsInLikeOperator
                ),
                (
                    (Group(Optional(NOT) + BETWEEN), AND),
                    3, opAssoc.LEFT, BetweenOperator
                ),
                (
                    AND,
                    2, opAssoc.LEFT, BinaryOperator
                ),
                (
                    OR,
                    2, opAssoc.LEFT, BinaryOperator
                ),
                (
                    DOT + Word(nums),
                    1, opAssoc.LEFT
                ),
            ]
        )
        return self._column_expr

    @property
    def term(self) -> ParserElement:
        return ColumnExprTerm(self._column_expr, self._select_union_statement).notation
#
#
# if __name__ == '__main__':
#     from ast import literal_eval
#     column_expr = Forward()
#
#     c = ColumnExpr(column_expr)
#     print(literal_eval(str(c.notation.parse_string('funct(distinct name, a, t.*)', parse_all=True))))
