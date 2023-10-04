from functools import lru_cache
from pyparsing import delimited_list, pyparsing_common, nums
from pyparsing import ParserElement, Optional, MatchFirst, Word

from src.keywords import (
    PARTITION, BY, ORDER, ROWS, RANGE, BETWEEN, AND, AS,
    CURRENT, ROW, UNBOUNDED, PRECEDING, FOLLOWING, WINDOW
)
from src.literals import LPAR, RPAR

from src.lexer.statement import Statement
from src.utils.singleton import Singleton
from src.lexer.query.select_union.order_by import OrderBy


class WindowExpr:
    def __init__(
        self,
        window_expr: ParserElement,
        column_expr: ParserElement
    ):
        self._window_expr = window_expr
        self._column_expr = column_expr

    @property
    @lru_cache
    def notation(self):
        self._window_expr << (
            Optional(
                PARTITION + BY
                + delimited_list(self._column_expr)('partition_by_args')
            )
            + Optional(
                ORDER + BY
                + OrderBy(self._column_expr).order_by_expr_list('order_by_args')
            )
            + Optional(
                MatchFirst([ROWS, RANGE])('by')
                + MatchFirst([
                    self.window_frame_bound('bound'),
                    (
                        BETWEEN('between')
                        + self.window_frame_bound('start_bound')
                        + AND
                        + self.window_frame_bound('end_bound')
                    )
                ])
            )

        ).set_parse_action(
            lambda term: {
                'window_expr': (
                    ({'partition_by': term['partition_by_args'].as_list()}
                     if term.get('partition_by_args') else {})
                    | ({'order_by': term['order_by_args'].as_list()}
                       if term.get('order_by_args') else {})
                    | ({'frame': (
                            {'by': term['by']}
                            | ({'between': {
                                    'start': term['start_bound'],
                                    'end': term['end_bound']
                            }} if term.get('between') else term['bound'])
                    )} if term.get('by') else {})
                )
            }
        )
        return self._window_expr

    @property
    def window_frame_bound(self):
        return MatchFirst([
            CURRENT + ROW,
            UNBOUNDED + PRECEDING,
            UNBOUNDED + FOLLOWING,
            Word(nums) + PRECEDING,
            Word(nums) + FOLLOWING
        ]).set_parse_action(lambda term: {'bound': ' '.join(term)})


class Window(Statement):
    def __init__(
        self,
        window_expr: ParserElement,
        column_expr: ParserElement,
    ):
        self._window_expr = window_expr
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        self._window_expr << (
            WINDOW + pyparsing_common.identifier('window_identifier')
            + AS
            + LPAR
            + WindowExpr(
                column_expr=self._column_expr,
                window_expr=self._window_expr
            ).notation('expr')
            + RPAR
        ).set_parse_action(
            lambda term: {
                'window': (
                    {'identifier': term['window_identifier']}
                    | term['expr'][0]
                )
            }
        )
        return self._window_expr


class WindowFunction:
    def __init__(self, column_expr, window_expr):
        self._column_expr = column_expr
        self._window_expr = window_expr

    @property
    def notation(self) -> ParserElement:
        return (
            pyparsing_common.identifier['name']
            + LPAR + self._window_expr + RPAR
        )

# if __name__ == '__main__':
#     from src.columns import ColumnExpr
#     from pyparsing import Forward
#
#     window_expr = Forward()
#     column_expr = Forward()
#     select = Forward()
#
#     we = WindowExpr(
#         window_expr=window_expr,
#         column_expr=ColumnExpr(
#             column_expr=column_expr,
#             select_union_statement=select,
#             window_expr=window_expr
#         ).notation).notation
#     print(we.parse_string('partition by name order by name', parse_all=True))
#
# if __name__ == '__main__':
#     from src.columns import ColumnExpr
#     from pyparsing import Forward
#
#     window_expr = Forward()
#     column_expr = Forward()
#     select = Forward()
#
#     w = Window(
#         window_expr=window_expr,
#         column_expr=ColumnExpr(
#             column_expr=column_expr,
#             select_union_statement=select,
#         ).notation
#     ).notation
#
#     # print(w.parse_string('window w1 as (rows current row)', parse_all=True))
#     print(w.parse_string('window w1 as (partition by name, id order by id2 rows between current row and 1 preceding)'))