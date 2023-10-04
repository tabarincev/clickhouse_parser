from pyparsing import delimited_list, nums
from pyparsing import ParserElement, Optional, Word

from src.lexer.statement import Statement
from src.keywords import SELECT, DISTINCT, TOP, WITH, TIES, FROM


class Select(Statement):
    def __init__(self, columns_expr: ParserElement):
        self._columns_expr = columns_expr

    @property
    def notation(self) -> ParserElement:
        return (
            SELECT + Optional(DISTINCT('distinct'))
            + Optional(
                TOP('top') + Word(nums)('top_num')
                + Optional((WITH + TIES)('with_ties'))
            ) + delimited_list(~FROM + self._columns_expr)('select_columns')
        ).set_parse_action(
            lambda term: ({
                'select': (
                    ({'columns': term['select_columns'].as_list()})
                    | ({'distinct': True} if term.get('distinct') else {})
                    | ({'top': term['top_num']} if term.get('top_num') else {})
                    | ({'with_ties': True} if term.get('with_ties') else {})
                )
            })
        )
