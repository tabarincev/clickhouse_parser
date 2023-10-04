from pyparsing import pyparsing_common
from pyparsing import ParserElement, Optional

from src.lexer.statement import Statement
from src.keywords import DROP, COLUMN, IF, EXISTS


class DropColumn(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            DROP + COLUMN
            + Optional(IF + EXISTS('exists'))
            + pyparsing_common.identifier('column')
        ).set_parse_action(
            lambda term: ({
                'drop_column': (
                    {'column': term['column'][0]}
                    | ({'if_exists': True} if term.get('exists') else {})
                )
            })
        )
