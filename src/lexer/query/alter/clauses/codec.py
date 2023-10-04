from pyparsing import delimited_list
from pyparsing import ParserElement

from src.keywords import CODEC
from src.literals import LPAR, RPAR
from src.lexer.statement import Statement


class Codec(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            CODEC + LPAR + delimited_list(self._column_expr)('codecs') + RPAR
        ).set_parse_action(
            lambda term: {'codec_term': {'codecs': term['codecs'].as_list()}}
        )
