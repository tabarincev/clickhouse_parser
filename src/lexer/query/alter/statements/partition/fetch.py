from pyparsing import ParserElement

from src.literals import string_literal
from src.lexer.statement import Statement
from src.keywords import FETCH, PARTITION, PART, FROM


class FetchPartition(Statement):
    def __init__(self, column_expr: ParserElement):
        self._partition_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            FETCH + (PARTITION | PART)('partition')
            + self._partition_expr('partition_expr')
            + FROM + string_literal('from')
        ).set_parse_action(
            lambda term: {
                'fetch_{}'.format(term['partition'].lower()): {
                    'partition_expr': term['partition_expr']
                }
            }
        )
