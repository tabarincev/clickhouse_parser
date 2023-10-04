from pyparsing import ParserElement

from src.keywords import MODIFY, TTL
from src.lexer.statement import Statement


class ModifyTTL(Statement):
    def __init__(self, column_expr: ParserElement):
        self._ttl_expression = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            MODIFY + TTL + self._ttl_expression('ttl_expr')
        ).set_parse_action(lambda term: {'modify_ttl': term['ttl_expr']})
