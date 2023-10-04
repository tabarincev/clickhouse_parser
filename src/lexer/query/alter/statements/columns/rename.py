from pyparsing import pyparsing_common
from pyparsing import ParserElement, Optional

from src.lexer.statement import Statement
from src.keywords import RENAME, COLUMN, IF, EXISTS, TO


class RenameColumn(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            RENAME + COLUMN
            + Optional(IF + EXISTS('exists'))
            + pyparsing_common.identifier('old_column')
            + TO + pyparsing_common.identifier('new_column')
        ).set_parse_action(
            lambda term: {
                'rename_column': (
                    {'old_column': term['old_column'][0]}
                    | {'new_column': term['new_column'][0]}
                    | ({'if_exists': True} if term.get('exists') else {})
                )
            }
        )
