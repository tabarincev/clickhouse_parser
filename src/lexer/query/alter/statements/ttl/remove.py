from pyparsing import ParserElement

from src.keywords import REMOVE, TTL
from src.lexer.statement import Statement


class RemoveTTL(Statement):
    def __init__(self, column_expr: ParserElement):
        self._ttl_expression = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            REMOVE + TTL
        ).set_parse_action(lambda term: {'remove_ttl': True})
