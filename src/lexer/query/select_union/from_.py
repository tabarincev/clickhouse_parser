from ast import literal_eval

from pyparsing import delimited_list, pyparsing_common
from pyparsing import MatchFirst, Optional, ParserElement, ZeroOrMore

from src.keywords import (
    SAMPLE, OFFSET, AS, GLOBAL, LOCAL, JOIN, ANY, ALL,
    ASOF, INNER, LEFT, RIGHT, OUTER, SEMI, ANTI, FULL, ON, USING, FROM
)
from src.literals import LPAR, RPAR, SLASH, DOT, identifier, string_literal
from src.lexer.statement import Statement

ParserElement.enable_left_recursion()


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
        self._table_expr << (
            MatchFirst([
                self.table_function,
                self.table_identifier,
                string_literal,
                self._select_union_statement,
            ])('table')
            + Optional(
                Optional(AS)
                + identifier('alias')
            )
        ).set_parse_action(
            lambda term: (
                literal_eval(str(term['table']))
                | ({'alias': term['alias'][0]}
                   if term.get('alias') else {})
            )
        )
        return self._table_expr

    @property
    def table_identifier(self) -> ParserElement:
        return MatchFirst([
            (
                pyparsing_common.identifier('project')
                + DOT + pyparsing_common.identifier('database')
                + DOT + pyparsing_common.identifier('table')
            ),
            (
                pyparsing_common.identifier('database')
                + DOT + pyparsing_common.identifier('table')
            ),
            (
                pyparsing_common.identifier('table')
            )
        ]).set_parse_action(
            lambda term: {
                'table_identifier': (
                    ({'project': term['project']}
                     if term.get('project') else {})
                    | ({'database': term['database']}
                       if term.get('database') else {})
                    | ({'table': term['table']})
                )
            }
        )

    @property
    def table_function(self) -> ParserElement:
        return (
            pyparsing_common.identifier('name')
            + LPAR
            + delimited_list(self._table_expr)('args')
            + RPAR
        ).set_parse_action(
            lambda term: ({
                'table_function': {
                    'name': term['name'],
                    'args': term['args'].as_list()
                }
            })
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
            (
                TableExpr(
                    table_expr=self._table_expr,
                    select_union_statement=self._select_union_statement
                ).notation('table')
                + ZeroOrMore(
                    (Optional(MatchFirst([GLOBAL, LOCAL])('prejoin_type'))
                        + Optional(self.operator('operator')) + JOIN
                        + TableExpr(
                            table_expr=self._table_expr,
                            select_union_statement=self._select_union_statement
                        ).notation('table_to_join')
                        + self.constraint('constraint')
                    ).set_parse_action(
                        lambda term: (
                            ({'prejoin_type': term['prejoin_type']}
                               if term.get('prejoin_type') else {})
                            | ({'operator': term['operator'][0]}
                               if term.get('operator') else {})
                            | {'table_to_join': term['table_to_join'][0]}
                            | term['constraint']
                        )
                    )
                )('joins')
            ).set_parse_action(
                lambda term: (
                    term['table'][0]
                    | ({'joins': term['joins'].as_list()}
                       if term.get('joins') else {})
                )
            )
        ])
        # @property
        # def notation(self) -> ParserElement:
        #     self._join_expr << (
        #         TableExpr(
        #             table_expr=self._table_expr,
        #             select_union_statement=self._select_union_statement
        #         ).notation('table')
        #         + ZeroOrMore(
        #             (
        #                 Optional(
        #                     MatchFirst([GLOBAL, LOCAL])('prejoin_type')
        #                 )
        #                 + Optional(self.operator('operator')) + JOIN
        #                 + TableExpr(
        #                     table_expr=self._table_expr,
        #                     select_union_statement=self._select_union_statement
        #                 ).notation('table_to_join')
        #                 + self.constraint
        #             ).set_parse_action(
        #                 lambda term: (
        #                     ({'prejoin_type': term['prejoin_type']}
        #                        if term.get('prejoin_type') else {})
        #                     | ({'operator': term['operator'][0]}
        #                        if term.get('operator') else {})
        #                     | {'table_to_join': term['table_to_join'][0]}
        #                 )
        #             )
        #         )('joins')
        #     ).set_parse_action(
        #         lambda term: (
        #             term['table'][0]
        #             | ({'joins': term['joins'].as_list()}
        #                if term.get('joins') else {})
        #         )
        #     )
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
                    Optional(
                        MatchFirst([SEMI, ALL, ANTI, ASOF])('prejoin_type'))
                    + (LEFT | RIGHT)('join_type') + Optional(OUTER('outer'))
                ),
                (
                    (LEFT | RIGHT)('join_type') + Optional(OUTER('outer'))
                    + Optional(
                    MatchFirst([SEMI, ALL, ANTI, ASOF])('prejoin_type'))
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
                Optional(ALL | ANY)('prejoin_type') + FULL + Optional(
                    OUTER('outer')),
                FULL + Optional(OUTER('outer')) + Optional(ALL | ANY)(
                    'prejoin_type')
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
            USING('using') + LPAR + delimited_list(self._column_expr)(
                'exprs') + RPAR,
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
        column_expr: ParserElement,
        table_expr: ParserElement,
        select_union_statement: ParserElement
    ):
        self._join_expr = join_expr
        self._column_expr = column_expr
        self._table_expr = table_expr
        self._select_union_statement = select_union_statement

    @property
    def notation(self) -> ParserElement:
        return (
            FROM
            + JoinExpr(
                join_expr=self._join_expr,
                column_expr=self._column_expr,
                table_expr=self._table_expr,
                select_union_statement=self._select_union_statement
            ).notation('join_expr')
        ).set_parse_action(
            lambda term: {'from': {'join_expr': term['join_expr']}}
        )
