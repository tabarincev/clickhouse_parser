from pyparsing import pyparsing_common
from pyparsing import ParserElement, Optional

from src.literals import string_literal
from src.lexer.statement import Statement
from src.keywords import COMMENT, COLUMN, IF, EXISTS


class CommentColumn(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            COMMENT + COLUMN
            + Optional(IF + EXISTS('exists'))
            + pyparsing_common.identifier('column')
            + string_literal('comment')
        ).set_parse_action(
            lambda term: ({
                'comment_column': (
                    {'column': term['column'][0]}
                    | {'comment': term['comment']}
                    | ({'if_exists': True} if term.get('exists') else {})
                )
            })
        )
