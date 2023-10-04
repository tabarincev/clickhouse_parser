from typing import Dict
from textwrap import dedent

from src.builder.builder import BaseBuilder
from src.builder.columns import ColumnBuilder


class PreWhereBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'prewhere' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "prewhere" key'
            )
        return dedent(
            'prewhere {prewhere_expr}'.format(
                prewhere_expr=ColumnBuilder().build_full_expr(
                    ast['prewhere']['expr']
                )
            )
        )
