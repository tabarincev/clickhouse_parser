from pyparsing import pyparsing_common, delimited_list
from pyparsing import ParserElement, Optional

from src.keywords import (
    ADD, PROJECTION, IF, NOT, EXISTS, SELECT, GROUP, BY, ORDER
)
from src.lexer.statement import Statement


class AddProjection(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            ADD + PROJECTION + Optional(IF + NOT + EXISTS('exists'))
            + pyparsing_common.identifier('projection_name')
            + (
                SELECT + delimited_list(self._column_expr)('columns')
                + Optional(
                    GROUP + BY
                    + delimited_list(self._column_expr)('group_by_expr')
                )  # todo уточнить корректность
                + Optional(
                    ORDER + BY
                    + delimited_list(self._column_expr)('order_by_expr')
                )  # todo уточнить корректность
            )
        ).set_parse_action(
            lambda term: {
                'add_projection': {
                    'projection_name': term['projection_name'][0],
                    'select': (
                        {'columns': term['columns'].as_list()}
                        | ({'group_by': term['group_by_expr'].as_list()}
                            if term.get('group_by_expr') else {})
                        | ({'order_by': term['order_by_expr'].as_list()}
                            if term.get('order_by_expr') else {})
                    )
                }
            }
        )
