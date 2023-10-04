from pyparsing import pyparsing_common
from pyparsing import ParserElement, Optional

from src.lexer.statement import Statement
from src.keywords import CLEAR, PROJECTION, IF, EXISTS
from src.lexer.query.alter.clauses.in_partition import InPartition


class ClearProjection(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            CLEAR + PROJECTION + Optional(IF + EXISTS('exists'))
            + pyparsing_common.identifier('projection_name')
            + InPartition(self._column_expr).notation('in_partition')
        ).set_parse_action(
            lambda term: {
                'clear_projection': (
                    {'projection_name': term['projection_name']}
                    | term['in_partition']
                    | ({'if_exists': True} if term.get('exists') else {})
                )
            }
        )
