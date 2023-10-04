from typing import Dict

from src.builder.builder import BaseBuilder
from src.builder.columns import ColumnBuilder


class SampleBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'sample' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - '
                'Expected necessary "sample" key'
            )
        return 'sample {coeff}{offset}'.format(
            coeff=ast['sample']['coeff'],
            offset=ast['sample'].get('coeff', '')
        )


class TableExprBuilder(BaseBuilder):
    expected_keys = [
        'table_identifier',
        'table_function',
        'string_literal',
        'select'
    ]

    def build(self, ast: Dict) -> str:
        if (
            'table_identifier' or 'table_function' or
            'string_literal' or 'select'
        ):
            raise ValueError(
                'Invalid structure of SQL AST - '
                'Expected {expected_keys} keys'.format(
                    expected_keys=', '.join(self.expected_keys)
                )
            )


class JoinExprBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'join_expr' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - '
                'Expected necessary "join_expr" key'
            )


class FromBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'from' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - '
                'Expected necessary "from" key'
            )
        return 'from {join_expr}'.format(
            join_expr=ast['from']['join_expr']
        )

