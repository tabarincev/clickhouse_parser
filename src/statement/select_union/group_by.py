from pyparsing import *

from src.keywords import *
from src.literals import LPAR, RPAR
from src.statement.statement import Statement


class GroupBy(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self):
        return (
            GROUP + BY
            + MatchFirst([
                LPAR + delimited_list(self._column_expr)('exprs') + RPAR,
                delimited_list(self._column_expr)('exprs')
            ])
            + Optional(WITH + (CUBE('cube') | ROLLUP('rollup')))
            + Optional(WITH + TOTALS('totals'))
        ).set_parse_action(
            lambda term: {
                'group_by': {'by_exprs': term['expr']} | ({'type': term['type']} if term.get('type') else {})
            }
        )
