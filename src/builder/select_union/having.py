from pyparsing import Dict
from textwrap import dedent

from src.builder.builder import BaseBuilder
from src.builder.columns import ColumnBuilder


class HavingBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'having' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "having" key'
            )
        return dedent(
            'having {having_expr}'.format(
                having_expr=ColumnBuilder().build_full_expr(
                    ast['having']['expr']
                )
            )
        )
