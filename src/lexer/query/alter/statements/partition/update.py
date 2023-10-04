
from pyparsing import ParserElement, Optional
from pyparsing import pyparsing_common, delimited_list

from src.literals import EQ_SINGLE
from src.lexer.statement import Statement
from src.keywords import UPDATE, PARTITION, WHERE, IN


class UpdatePartition(Statement):
    def __init__(self, column_expr: ParserElement):
        self._partition_expr = column_expr
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            UPDATE + delimited_list(
                (
                    pyparsing_common.identifier('identifier')
                    + EQ_SINGLE
                    + self._column_expr('value')
                ).set_parse_action(
                    lambda term: {
                        'eq': {
                            'identifier': term['identifier'][0],
                            'value': term['value']
                        }
                    }
                )('columns')
            )
            + Optional(
                IN + PARTITION
                + pyparsing_common.integer('partition_id')
            )
            + WHERE + self._column_expr('where_expr')
        ).set_parse_action(
            lambda term: ({
                'update_column': (
                    {'columns': term['columns'].as_list()}
                    | {'where': term['where_expr']}
                    | ({'partition_id': term['partition_id']}
                        if term.get('partition_id') else {})
                )
            })
        )
