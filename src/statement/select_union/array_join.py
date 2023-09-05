from pyparsing import *

from src.keywords import *
from src.statement.statement import Statement


class ArrayJoin(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self):
        return (
            Optional(MatchFirst([LEFT, INNER])('type'))
            + ARRAY + JOIN
            + delimited_list(self._column_expr)('join_term')
        ).set_parse_action(
            lambda term: ({
                'array_join': {'join_term': term['join_term'].as_list()}
                | ({'type': term['type'].lower()} if term.get('type') else {})
            })
        )
