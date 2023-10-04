from pyparsing import delimited_list
from pyparsing import ParserElement, Optional

from src.keywords import (
    ORDER, BY, ASC, ASCENDING, DESC, DESCENDING, NULLS, FIRST, LAST, COLLATE
)
from src.literals import string_literal
from src.lexer.statement import Statement

from src.columns import ColumnExpr
from pyparsing import Forward


class OrderBy(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self):
        return (
            ORDER + BY + self.order_by_expr_list('order_by_list')
        ).set_parse_action(
            lambda term: {'order_by': term['order_by_list'].as_list()}
        )

    @property
    def order_by_expr(self):
        return (
            self._column_expr('expr')
            + Optional((ASCENDING | DESCENDING | DESC | ASC)('order_type'))
            + Optional(NULLS + (FIRST | LAST)('nulls'))
            + Optional(COLLATE + string_literal('collate_string'))
        ).set_parse_action(
            lambda term: ({
                'order_by_term':
                term['expr']
                | ({'order_type': term['order_type']}
                    if term.get('order_type') else {})
                | ({'nulls': term['nulls']}
                    if term.get('nulls') else {})
                | ({'collate': term['collate_string']}
                    if term.get('collate_string') else {})

            })
        )

    @property
    def order_by_expr_list(self) -> ParserElement:
        return delimited_list(self.order_by_expr)


if __name__ == '__main__':
    column_expr = Forward()
    select = Forward()

    ob = OrderBy(
        ColumnExpr(
            column_expr=column_expr,
            select_union_statement=select
        ).notation
    ).notation

    print(ob.parse_string('order by 1, name descending nulls first, id, func(na)'))