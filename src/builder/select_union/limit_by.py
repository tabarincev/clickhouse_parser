from typing import Dict
from textwrap import dedent

from src.builder.builder import BaseBuilder
from src.builder.columns import ColumnBuilder


class LimitByBuilder(BaseBuilder):
    @staticmethod
    def build_limit_expr(expr: Dict) -> str:
        return '{value}{offset}'.format(
            value=ColumnBuilder().build_full_expr(
                expr['limit_expr']['value']
            ),
            offset=' offset {value}'.format(
                value=ColumnBuilder().build_full_expr(
                    expr['limit_expr']['offset']
                )
            ) if expr['limit_expr'].get('offset') else ''
        )

    @staticmethod
    def build_by_expr(by: Dict) -> str:
        return ', '.join([
            ColumnBuilder().build_full_expr(column)
            for column in by['by_expr']
        ])

    def build(self, ast: Dict) -> str:
        if 'limit_by' not in ast['select_union_statement']:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "limit_by" key'
            )
        return dedent(
            'limit {limit_expr} by {by_expr}'.format(
                limit_expr=self.build_limit_expr(ast),
                by_expr=self.build_by_expr(ast)
            )
        )
