from pyparsing import pyparsing_common
from pyparsing import ParserElement

from src.keywords import MATERIALIZE, INDEX, PARTITION, IN
from src.lexer.statement import Statement


class MaterializeIndex(Statement):
    def __init__(self, column_expr: ParserElement):
        self._partition_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            MATERIALIZE + INDEX + pyparsing_common.identifier('index_name')
            + IN + PARTITION + self._partition_expr('partition_expr')
        ).set_parse_action(
            lambda term: {
                'materialize_index': {
                    'index_name': term['index_name'][0],
                    'partition_expr': term['partition_expr']
                }
            }
        )
