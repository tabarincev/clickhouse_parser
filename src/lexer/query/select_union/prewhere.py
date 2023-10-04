from pyparsing import ParserElement

from src.keywords import PREWHERE
from src.lexer.statement import Statement


class PreWhere(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self):
        return (PREWHERE + self._column_expr('expr')).set_parse_action(
            lambda term: {'prewhere': {'expr': term['expr']}}
        )


