from pyparsing import *
from src.keywords import *
from src.statement.statement import Statement

from src.columns import ColumnExpr


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
            ) + delimited_list(self._columns_expr)('select_columns')
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

if __name__ == '__main__':
    column_expr = Forward()

    c = ColumnExpr(column_expr).notation

    select = Select(c).notation
    print(select.parse_string('select distinct top 1 with ties func(n.name, 1) as b1, b.n.a', parse_all=True))