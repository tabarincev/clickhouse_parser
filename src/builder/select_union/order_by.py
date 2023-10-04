from typing import Dict
from textwrap import dedent

from src.builder.builder import BaseBuilder
from src.builder.columns import ColumnBuilder


class OrderByBuilder(BaseBuilder):
    @staticmethod
    def _build_order_term(order_term: Dict) -> str:
        return '{column}{order_type}{nulls}'.format(
            column=ColumnBuilder().build_full_expr(
                order_term['order_by_term']
            ),
            order_type=(
                ' {}'.format(
                    order_term['order_by_term']['order_type']
                ) if order_term['order_by_term'].get('order_type') else ''
            ),
            nulls=(
                ' nulls {}'.format(
                    order_term['order_by_term']['nulls']
                ) if order_term['order_by_term'].get('nulls') else ''
            )
        )

    def build(self, ast: Dict) -> str:
        if 'order_by' not in ast['select_union_statement']:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "order_by" key'
            )
        return dedent(
            'order by {order_by_expr}'.format(
                order_by_expr=', '.join([
                    self._build_order_term(order_term)
                    for order_term in ast['select_union_statement']['order_by']
                ])
            )
        )
