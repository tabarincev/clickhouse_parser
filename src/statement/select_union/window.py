from pyparsing import *

from src.keywords import *
from src.literals import LPAR, RPAR, identifier
from src.statement.statement import Statement
from src.statement.select_union.order_by import OrderBy


class WindowExpr:
    def __init__(
        self,
        window_expr: ParserElement,
        column_expr: ParserElement,
        columns_expr: ParserElement
    ):
        self._window_expr = window_expr
        self._column_expr = column_expr
        self._columns_expr = columns_expr

    @property
    def notation(self):
        self._window_expr << (
            Optional(
                PARTITION + BY
                + delimited_list(self._columns_expr)('partition_by_args')
            )
            + Optional(
                ORDER + BY
                + OrderBy(self._column_expr).order_by_expr_list('order_by_args')
            )
            + Optional(MatchFirst([ROWS, RANGE])('by'))
            + MatchFirst([
                self.window_frame_bound('bound'),
                BETWEEN('between')
                + self.window_frame_bound('start_bound')
                + AND
                + self.window_frame_bound('end_bound')
            ])
        ).set_parse_action(
            lambda term: ({
                'window_expr': (
                    ({'partition_by': term['partition_by_args']}
                     if term.get('partition_by_args') else {})
                    | ({'order_by': term['order_by_args']}
                       if term.get('order_by_args') else {})
                    | ({'by': term['by'].lower()}
                       if term.get('by') else {})
                    | ({'frame': {
                            'between': {
                                'start': term['start_bound'],
                                'end': term['end_bound']
                            }
                        }
                        if term.get('between') else {'frame_bound': term['bound']}
                    })
                )
            })
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
        columns_expr: ParserElement
    ):
        self._window_expr = window_expr
        self._column_expr = column_expr
        self._columns_expr = columns_expr

    @property
    def notation(self) -> ParserElement:
        return (
            WINDOW + identifier('window_identifier')
            + AS
            + LPAR
            + WindowExpr(
                column_expr=self._column_expr,
                columns_expr=self._columns_expr,
                window_expr=self._window_expr
            ).notation('expr')
            + RPAR
        ).set_parse_action(
            lambda term: {
                'window': {
                    'identifier': term['window_identifier'],
                    'expr': term['expr']
                }
            }
        )
