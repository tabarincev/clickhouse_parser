from pyparsing import ParserElement

from src.keywords import IN, PARTITION
from src.lexer.statement import Statement


class InPartition(Statement):
    def __init__(self, column_expr: ParserElement):
        self._partition_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            IN + PARTITION
            + self._partition_expr('partition_expr')
        ).set_parse_action(
            lambda term: {
                'in_partition': {'partition_expr': term['partition_expr']}
            }
        )
