from pyparsing import pyparsing_common
from pyparsing import ParserElement

from src.lexer.statement import Statement
from src.keywords import MOVE, TO, PARTITION, TABLE


class MoveToPartition(Statement):
    def __init__(self, column_expr: ParserElement):
        self._partition_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            MOVE + PARTITION + self._partition_expr('partition_expr')
            + TO + TABLE + pyparsing_common.identifier('table')  # todo table_identifier
        ).set_parse_action(
            lambda term: ({
                'move_partition_to_table': {
                    'partititon_expr': term['partition_expr'],
                    'to': term['table'][0]
                }
            })
        )
