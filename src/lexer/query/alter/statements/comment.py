from pyparsing import ParserElement

from src.literals import string_literal
from src.lexer.statement import Statement
from src.keywords import MODIFY, COMMENT


class AlterComment(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            MODIFY + COMMENT + string_literal('comment')
        ).set_parse_action(
            lambda term: {'modify_comment': {'comment': term['comment']}}
        )
