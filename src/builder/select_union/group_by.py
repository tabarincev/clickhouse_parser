from typing import Dict
from textwrap import dedent

from src.builder.builder import BaseBuilder
from src.builder.columns import ColumnBuilder


class GroupByBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'group_by' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "group_by" key'
            )
        return dedent(
            'group by {group_by_expr}{with_type}{with_totals}'.format(
                group_by_expr=', '.join([
                    ColumnBuilder().build_full_expr(column)
                    for column in ast['group_by']['by_exprs']
                ]),
                with_type=(
                    ' with {}'.format(ast['group_by']['type'])
                    if ast['group_by'].get('type') else ''
                ),
                with_totals=(
                    ' with totals'
                    if ast['group_by'].get('with_totals') else ''
                )
            )
        )
