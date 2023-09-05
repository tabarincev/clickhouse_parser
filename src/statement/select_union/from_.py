from pyparsing import *

from src.keywords import *
from src.literals import LPAR, RPAR, SLASH, COMMA, DOT, string_literal
from src.statement.statement import Statement


class Sample(Statement):
    @property
    def notation(self):
        return (
            SAMPLE + MatchFirst([
                (
                    pyparsing_common.integer('int1')
                    + SLASH + pyparsing_common.integer('int2')
                ).set_parse_action(
                    lambda term: str(term['int1']) + '/' + str(term['int2'])
                )('coeff'),
                pyparsing_common.number('coeff')
            ])
            + Optional(OFFSET + pyparsing_common.integer('offset'))
        ).set_parse_action(
            lambda term: ({
                'sample': (
                    {'coeff': term['coeff']}
                    | ({'offset': term['offset']}
                       if term.get('offset') else {})
                )
            })
        )


class TableExpr:
    def __init__(
        self,
        table_expr: ParserElement,
        select_union_statement: ParserElement
    ):
        self._table_expr = table_expr
        self._select_union_statement = select_union_statement

    @property
    def notation(self) -> ParserElement:
        return MatchFirst([
            self.table_identifier,
            self.table_function,
            self.subquery,
            self.expr_alias
        ])

    @property
    def table_identifier(self) -> ParserElement:
        return (
            pyparsing_common.identifier
            + DOT + pyparsing_common
        )

    @property
    def table_function(self) -> ParserElement:
        return (
            pyparsing_common.identifier
            + LPAR + delimited_list(
                MatchFirst([
                    self.table_identifier,
                    self.table_function,
                    (Word(nums) | string_literal | NULL)
                ])
            ) + RPAR
        )

    @property
    def subquery(self) -> ParserElement:
        return self._select_union_statement

    @property
    def expr_alias(self) -> ParserElement:
        return (
            self._table_expr
            + Optional(Optional(AS) + pyparsing_common.identifier)
        )


class JoinExpr:
    def __init__(
        self,
        join_expr: ParserElement,
        table_expr: ParserElement,
        column_expr: ParserElement,
        select_union_statement: ParserElement
    ):
        self._join_expr = join_expr
        self._table_expr = table_expr
        self._column_expr = column_expr
        self._select_union_statement = select_union_statement

    @property
    def notation(self) -> ParserElement:
        self._join_expr << MatchFirst([
            # operator
            self._join_expr + Optional(GLOBAL | LOCAL) + Optional(self.operator)
            + JOIN + self._join_expr + self.constraint,
            # cross operator
            self._join_expr + MatchFirst([
                Optional(GLOBAL | LOCAL) + CROSS + JOIN,
                COMMA
            ]) + self._join_expr,
            # table
            TableExpr(
                self._table_expr,
                self._select_union_statement
            ).notation + Optional(FINAL) + Sample().notation,
            # parens
            LPAR + self._join_expr + RPAR
        ])
        return self._join_expr

    @property
    def operator(self) -> ParserElement:
        return MatchFirst([
            # Inner
            MatchFirst([
                Optional(MatchFirst([ALL, ANY, ASOF])('inner_type')) + INNER,
                INNER + Optional(MatchFirst([ALL, ANY, ASOF])('inner_type')),
                MatchFirst([ALL, ANY, ASOF])('inner_type')
            ]).set_parse_action(
                lambda term: (
                    {'join_type': 'inner'}
                    | ({'inner_type': term['inner_type'].lower()}
                        if term.get('inner_type') else {})
                )
            ),
            # Left Right
            MatchFirst([
                (
                    Optional(MatchFirst([SEMI, ALL, ANTI, ASOF])('prejoin_type'))
                    + (LEFT | RIGHT)('join_type') + Optional(OUTER('outer'))
                ),
                (
                    (LEFT | RIGHT)('join_type') + Optional(OUTER('outer'))
                    + Optional(MatchFirst([SEMI, ALL, ANTI, ASOF])('prejoin_type'))
                )
            ]).set_parse_action(
                lambda term: (
                    {'join_type': term['join_type'].lower()}
                    | {'outer': True if term.get('outer') else False}
                    | ({'prejoin_type': term['prejoin_type']}
                        if term.get('prejoin_type') else {})
                )
            ),
            # Full
            MatchFirst([
                Optional(ALL | ANY)('prejoin_type') + FULL + Optional(OUTER('outer')),
                FULL + Optional(OUTER('outer')) + Optional(ALL | ANY)('prejoin_type')
            ]).set_parse_action(
                lambda term: (
                    {'join_type': 'full'}
                    | {'outer': True if term.get('outer') else False}
                    | ({'prejoin_type': term['prejoin_type']}
                        if term.get('prejoin_type') else {})
                )
            )
        ])

    @property
    def constraint(self) -> ParserElement:
        return MatchFirst([
            ON('on') + delimited_list(self._column_expr)('exprs'),
            USING('using') + LPAR + delimited_list(self._column_expr)('exprs') + RPAR,
            USING('using') + delimited_list(self._column_expr)('exprs')
        ]).set_parse_action(
            lambda term: {
                'constraint': {
                    'type': 'on' if term.get('on') else 'using',
                    'exprs': term['exprs'].as_list()
                }
            }
        )


class From(Statement):
    def __init__(
        self,
        join_expr: ParserElement,
        column_expr: ParserElement
    ):
        self._join_expr = join_expr
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            FROM
            + JoinExpr(
                self._join_expr,
                self._column_expr
            ).notation('join_expr')
        ).set_parse_action(
            lambda term: {'from': {'join_expr': term['join_expr']}}
        )

if __name__ == '__main__':
    s = Sample().notation
    print(s.parse_string('sample 1.10 offset 3', parse_all=True))