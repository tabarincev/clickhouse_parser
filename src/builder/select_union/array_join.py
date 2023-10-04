from typing import Dict

from src.builder.builder import BaseBuilder
from src.builder.columns import ColumnBuilder


class ArrayJoinBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'array_join' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "array_join" key'
            )
        return '{prejoin_type}array join {join_terms}'.format(
            prejoin_type='{join_type} '.format(
                join_type=ast['array_join']['type']
            ) if ast['array_join'].get('type') else '',
            join_terms=', '.join([
                ColumnBuilder().build_full_expr(column)
                for column in ast['array_join']['join_term']
            ])
        )
