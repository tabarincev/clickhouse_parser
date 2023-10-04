from typing import Dict
from textwrap import dedent

from src.builder.builder import BaseBuilder
from src.builder.columns import ColumnBuilder


class WhereBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'where' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "where" key'
            )
        return dedent(
            'where {where_expr}'.format(
                where_expr=ColumnBuilder().build_full_expr(
                    ast['where']['expr']
                )
            )
        )
