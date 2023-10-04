from pyparsing import ParserElement
from pyparsing import pyparsing_common

from src.lexer.statement import Statement
from src.keywords import MATERIALIZE, PROJECTION
from src.lexer.query.alter.clauses.in_partition import InPartition


class MaterializeProjection(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            MATERIALIZE + PROJECTION
            + pyparsing_common.identifier('projection_name')
            + InPartition(self._column_expr).notation('in_partition')
        ).set_parse_action(
            lambda term: {
                'materialize_projection': (
                    {'projection_name': term['projection_name'][0]}
                    | (term['in_partition'])
                )
            }
        )
