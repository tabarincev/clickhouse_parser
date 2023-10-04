from pyparsing import pyparsing_common
from pyparsing import ParserElement, Optional

from src.lexer.statement import Statement
from src.keywords import DROP, PROJECTION, IF, EXISTS


class DropProjection(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            DROP + PROJECTION
            + Optional(IF + EXISTS('exists'))
            + pyparsing_common.identifier('projection_name')
        ).set_parse_action(
            lambda term: {
                'drop_projection': (
                    {'projection_name': term['projection_name']}
                    | ({'if_exists': True} if term.get('exists') else {})
                )
            }
        )
