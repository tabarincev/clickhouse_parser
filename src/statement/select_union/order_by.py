from pyparsing import *

from src.keywords import *
from src.literals import string_literal
from src.statement.statement import Statement


class OrderBy(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self):  # todo
        return

    @property
    def order_by_expr(self):
        return (
            self._column_expr
            + Optional(ASCENDING | DESCENDING | DESC)
            + Optional(NULLS + (FIRST | LAST))
            + Optional(COLLATE + string_literal)
        )

    @property
    def order_by_expr_list(self) -> ParserElement:
        return delimited_list(self.order_by_expr)
