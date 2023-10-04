from typing import Dict
from textwrap import dedent

from src.builder.builder import BaseBuilder
from src.builder.columns import ColumnBuilder


class LimitBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'limit' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "limit" key'
            )

        # limit_ast = ast['select_union_statement']['limit']

        return dedent(
            'limit {limit_expr}'.format(
                limit_expr='{limit} {with_ties}'.format(
                    limit='{value}{offset}'.format(
                        value=ColumnBuilder().build_full_expr(
                            ast['limit']['expr']['limit_expr']['value']
                        ),
                        offset=' offset {value}'.format(
                            value=ColumnBuilder().build_full_expr(
                                ast['limit']['expr']['limit_expr']['offset']
                            )
                        ) if ast['limit']['expr']['limit_expr'].get(
                            'offset') else ''
                    ),
                    with_ties='with ties' if ast['limit']['with_ties'] else ''
                )
            )
        )
