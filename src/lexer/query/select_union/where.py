from pyparsing import ParserElement

from src.keywords import WHERE
from src.lexer.statement import Statement


class Where(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self):
        return (
            WHERE
            + self._column_expr('expr')
        ).set_parse_action(
            lambda term: {'where': {'expr': term['expr']}}
        )
