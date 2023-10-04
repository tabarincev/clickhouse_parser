from pyparsing import *

from src.keywords import MODIFY, QUERY
from src.lexer.statement import Statement
from src.lexer.query.select_union.main import SelectUnion


class AlterModifyQuery(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            MODIFY + QUERY + SelectUnion().notation('select')
        ).set_parse_action(
            lambda term: print(term['select'])
        )
