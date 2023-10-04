from pyparsing import pyparsing_common
from pyparsing import ParserElement, Optional, MatchFirst

from src.lexer.statement import Statement
from src.keywords import ADD, INDEX, TYPE, FIRST, AFTER, GRANULARITY


class AddIndex(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            ADD + INDEX + pyparsing_common.identifier('index_name')
            + self._column_expr('expr')
            + TYPE + pyparsing_common.identifier('index_type')
            + GRANULARITY + pyparsing_common.identifier('granularity')
            + Optional(
                MatchFirst([
                    FIRST,
                    AFTER + pyparsing_common.identifier
                ])  # todo вынести в стэйтмент
            )
        ).set_parse_action(
            lambda term: {
                'add_index': {
                    'index_name': term['index_name'][0],
                    'expr': term['expr'],
                    'index_type': term['index_type'][0],
                    'granularity': term['granularity'][0]
                }
            }
        )
