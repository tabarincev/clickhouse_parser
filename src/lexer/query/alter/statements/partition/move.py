from pyparsing import ParserElement

from src.literals import string_literal
from src.lexer.statement import Statement
from src.keywords import MOVE, PARTITION, PART, TO, DISK, VOLUME


class MovePartition(Statement):
    def __init__(self, column_expr: ParserElement):
        self._partition_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            MOVE + (PARTITION | PART) + self._partition_expr
            + TO + (DISK | VOLUME) + string_literal
        )
