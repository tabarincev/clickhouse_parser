from pyparsing import ParserElement, Optional

from src.literals import string_literal
from src.lexer.statement import Statement
from src.keywords import UNFREEZE, FREEZE, PARTITION, WITH, NAME


class FreezePartition(Statement):
    def __init__(self, column_expr: ParserElement):
        self._partition_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            FREEZE + Optional(PARTITION + self._partition_expr)
            + Optional(WITH + NAME + string_literal)
        )


class UnfreezePartition(Statement):
    def __init__(self, column_expr: ParserElement):
        self._partition_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            UNFREEZE + Optional(PARTITION + self._partition_expr)
            + WITH + NAME + string_literal
        )
