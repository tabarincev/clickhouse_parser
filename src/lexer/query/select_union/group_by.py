from pyparsing import delimited_list
from pyparsing import MatchFirst, Optional, ParserElement

from src.literals import LPAR, RPAR
from src.lexer.statement import Statement
from src.keywords import GROUP, BY, WITH, CUBE, ROLLUP, TOTALS


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
            + Optional(WITH + (CUBE | ROLLUP)('type'))
            + Optional(WITH + TOTALS('with_totals'))
        ).set_parse_action(
            lambda term: {
                'group_by': (
                    {'by_exprs': term['exprs'].as_list()}
                    | ({'type': term['type']} if term.get('type') else {})
                    | ({'with_totals': True} if term.get('with_totals') else {})
                )
            }
        )
