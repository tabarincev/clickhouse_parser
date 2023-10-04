from typing import Dict

from src.builder.builder import BaseBuilder
from src.builder.columns import ColumnBuilder


class CTEBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'with' not in ast['select_union_statement']:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "with" key'
            )
        return 'with {with_exprs}'.format(
            with_exprs=', '.join([
                ColumnBuilder().build_full_expr(expr)
                for expr in ast['select_union_statement']['with']['exprs']
            ])
        )