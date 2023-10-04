from pyparsing import ParserElement
from pyparsing import pyparsing_common

from src.lexer.statement import Statement
from src.keywords import MATERIALIZE, COLUMN


class MaterializeColumn(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            MATERIALIZE + COLUMN + pyparsing_common.identifier('column')
        ).set_parse_action(
            lambda term: {'materialize_column': {'column': term['column'][0]}}
        )
