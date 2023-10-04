from typing import Dict
from textwrap import dedent

from src.builder.builder import BaseBuilder


class FormatBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'format' not in ast['select_union_statement']:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "format" key'
            )
        return dedent(
            'format {format_file}'.format(
                format_file=ast['select_union_statement']['format']['format_file']
            )
        )
