from pyparsing import ParserElement
from pyparsing import pyparsing_common

from src.keywords import DROP, INDEX
from src.lexer.statement import Statement


class DropIndex(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            DROP + INDEX
            + pyparsing_common.identifier('index_name')
        ).set_parse_action(
            lambda term: {'drop_index': {'index': term['index_name'][0]}}
        )
