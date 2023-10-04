from pyparsing import ParserElement
from pyparsing import pyparsing_common, delimited_list

from src.literals import EQ_SINGLE
from src.keywords import UPDATE, WHERE
from src.lexer.statement import Statement


class AlterUpdate(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            UPDATE +
            delimited_list(
                (
                    pyparsing_common.identifier('column')
                    + EQ_SINGLE
                    + self._column_expr('value')
                ).set_parse_action(
                    lambda term: {
                        'column': term['column'],
                        'value': term['value']
                    }
                )
            )('columns_to_update')
            + WHERE + self._column_expr('where_expr')
        ).set_parse_action(
            lambda term: {
                'update': {
                    'columns': term['columns_to_update'].as_list(),
                    'where': term['where_expr']
                }
            }
        )
