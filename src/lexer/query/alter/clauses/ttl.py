from pyparsing import ParserElement, Optional

from src.keywords import TTL
from src.lexer.statement import Statement


class TTL(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            TTL + self._column_expr('ttl_expr')
            + Optional(self._column_expr.interval('interval'))  # todo check
        ).set_parse_action(
            lambda term: {
                'ttl_term': (
                    {'ttl_expr': term['ttl_expr']}
                    | ({'interval': term['interval']}
                       if term.get('interval') else {})
                )
            }
        )
