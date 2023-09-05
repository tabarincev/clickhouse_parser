from pyparsing import *

from src.keywords import *
from src.statement.statement import Statement


class CommonTableExpr(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self):
        return (
            WITH + delimited_list(self._column_expr)('exprs')
        ).set_parse_action(
            lambda term: {'with': {'exprs': term['exprs'].as_list()}}
        )
