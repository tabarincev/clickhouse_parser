from pyparsing import *
from functools import lru_cache


from src.literals import *
from src.keywords import FROM, AS
from src.utils.infix_processing import (
    UnaryOperator, BinaryOperator, BetweenOperator,
    IsInLikeOperator
)


ParserElement.enable_left_recursion()


class ColumnExprTerm:
    def __init__(
        self,
        column_expr: ParserElement,
        select_union_statement: ParserElement,
        window_expr: ParserElement
    ):
        self._column_expr = column_expr
        self._select_union_statement = select_union_statement
        self._window_expr = window_expr

    @property
    def notation(self) -> ParserElement:
        return (
            MatchFirst([
                self.case,
                # self.cast, # todo
                self.date,
                self.extract,
                self.interval,
                self.substring,
                self.timestamp,
                # self.trim,
                self.lambda_function,
                self.window_function,
                # self.window_function_target,

                self.function,
                self.asterisk,
                self.column_identifier,
                self.literal,
                self.select_union_statement,
                self.braces,
                self.parens,
                self.tuple_,
                self.array_
            ])('term')
            + Optional(LBRACKET + self._column_expr('index') + RBRACKET)
            + Optional(Optional(AS) + ~FROM + identifier('alias'))
        ).set_parse_action(
            lambda term: ({
                'index_term': {
                    'term': term['term'],
                    'index': term['index']}
                } if term.get('index') else term['term']
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
        return CAST + LPAR + self._column_expr('cast_object') \
               + AS  # + column_type_expr + RPAR

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
        return (TIMESTAMP + string_literal(
            'timestamp_string')).set_parse_action(
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

    @property
    def window_function(self) -> ParserElement:
        return (
            identifier('window_identifier')
            + LPAR
            + Optional(delimited_list(self._column_expr)('window_args'))
            + RPAR
            + OVER + LPAR + Optional(self._window_expr('over')) + RPAR
        ).set_parse_action(
            lambda term: {
                'window_function': {
                    'identifier': term['window_identifier'][0],
                    'window_args': (term['window_args'].as_list()
                                    if term.get('window_args') else []),
                    'over': (term['over'][0]
                             if term.get('over') else {})
                }
            }
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
            ) + RPAR
        ).set_parse_action(
            lambda term: {
                'function_term': {
                    'name': term['function_name'],
                    'args': (term['column_arg_expr'].as_list()
                             if term.get('column_arg_expr') else [])
                } | ({'distinct': True}
                     if term.get('distinct') else {})
            }
        )

    @property  # todo test
    def lambda_function(self) -> ParserElement:
        return (
            function_name('function_name')
            + LPAR
            + MatchFirst([
                LPAR + delimited_list(self._column_expr)('identifiers_list') + RPAR,
                delimited_list(identifier)('identifiers_list')
            ])
            + ARROW + delimited_list(self._column_expr)('lambda_expr')
            + RPAR
        ).set_parse_action(
            lambda term: {
                'lambda_function_term': {
                    'identifiers_list': term['identifiers_list'].as_list(),
                    'expr': term['lambda_expr'].as_list()
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
            )
        ])

    @property
    def column_identifier(self) -> ParserElement:
        return MatchFirst([
            (
                pyparsing_common.identifier('database') + DOT
                + pyparsing_common.identifier('table') + DOT
                + pyparsing_common.identifier('column')
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
                pyparsing_common.identifier('table') + DOT
                + pyparsing_common.identifier('column')
            ).set_parse_action(
                lambda term: {
                    'column_term': {
                        'table': term['table'],
                        'column': term['column']
                    }
                }
            ),
            (
                pyparsing_common.identifier('column')
            ).set_parse_action(
                lambda term: {
                    'column_term': {
                        'column': term['column']
                    }
                }
            ),
            (
                ASTERISK('asterisk')
            ).set_parse_action(
                lambda term: {'column_term': '*'}
            )
        ])

    @property
    def literal(self) -> ParserElement:
        return MatchFirst([
            pyparsing_common.number.set_parse_action(
                lambda term: {'numeric': term[0]}
            ),
            string_literal.set_parse_action(
                lambda term: {'string': term[0]}
            ),
            NULL.set_parse_action(
                lambda term: {'literal': 'NULL'}
            )
        ]).set_parse_action(
            lambda term: {'literal_term': term[0]}
        )

    @property  # todo
    def select_union_statement(self) -> ParserElement:
        return self._select_union_statement

    @property
    def parens(self) -> ParserElement:
        return (
            LPAR + self._column_expr('term') + RPAR
        ).set_parse_action(
            lambda term: {'parens_term': term['term']}
        )

    @property
    def braces(self):
        return (
            Literal('{') + self._column_expr('term') + Literal('}')
        ).set_parse_action(
            lambda term: {'brace_term': term['term']}
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
                    'args': (term['args'].as_list()
                             if term.get('args') else [])
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
                    'args': (
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
        select_union_statement: ParserElement,
        window_expr: ParserElement
    ):
        self._column_expr = column_expr
        self._select_union_statement = select_union_statement
        self._window_expr = window_expr

    @property
    @lru_cache
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
        return ColumnExprTerm(
            self._column_expr,
            self._select_union_statement,
            self._window_expr
        ).notation


if __name__ == '__main__':
    from ast import literal_eval
    from src.lexer.query.select_union.window import WindowExpr

    column_expr = Forward()
    select = Forward()
    window_expr = Forward()

    c = ColumnExpr(
        column_expr,
        select_union_statement=select,
        window_expr=WindowExpr(
            window_expr=window_expr,
            column_expr=ColumnExpr(
                column_expr=column_expr,
                select_union_statement=select,
                window_expr=window_expr
            ).notation
        ).notation
    )

    print(c.notation.parse_string('`name`', parse_all=True))

    # ct = ColumnExprTerm(
    #     column_expr=column_expr,
    #     select_union_statement=select,
    #     window_expr=WindowExpr(
    #         window_expr=window_expr,
    #         column_expr=ColumnExpr(
    #             column_expr=column_expr,
    #             select_union_statement=select,
    #             window_expr=window_expr
    #         ).notation
    #     ).notation
    # ).notation
