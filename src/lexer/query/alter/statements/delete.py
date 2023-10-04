from pyparsing import ParserElement

from src.keywords import DELETE, WHERE
from src.lexer.statement import Statement


class AlterDelete(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            DELETE + WHERE + self._column_expr('expr')
        ).set_parse_action(lambda term: {'delete': {'where': term['expr']}})
