from typing import Dict
from textwrap import dedent

from src.builder.builder import BaseBuilder
from src.builder.columns import ColumnBuilder


class WindowBuilder(BaseBuilder):
    @staticmethod
    def build_partition_by(window_ast: Dict) -> str:
        return 'partition by {} '.format(
            ', '.join([
                ColumnBuilder().build_full_expr(column)
                for column in window_ast['window_expr']['partition_by']
            ])
        )

    @staticmethod
    def build_order_by(window_ast: Dict) -> str:
        return 'order by {} '.format(
            ', '.join([
                ColumnBuilder().build_full_expr(column['order_by_term'])
                for column in window_ast['window_expr']['order_by']
            ])
        )

    @staticmethod
    def build_frame(window_ast: Dict) -> str:
        return '{by} {bound}'.format(
            by=window_ast['by'],
            bound=(
                window_ast['bound']
                if window_ast.get('bound')
                else 'between {start} and {end}'.format(
                    start=window_ast['between']['start']['bound'],
                    end=window_ast['between']['end']['bound']
                )
            )
        )

    def build(self, ast: Dict) -> str:
        if 'window' not in ast['select_union_statement']:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "window" key'
            )

        window_ast = ast['select_union_statement']['window']

        return dedent(
            'window {identifier} as ({window_expr})'.format(
                identifier=window_ast['identifier'],
                window_expr='{partition_by}{order_by}{frame}'.format(
                    partition_by=(
                        self.build_partition_by(
                            window_ast['window_expr']['partition_by']
                        ) if window_ast['window_expr'].get(
                            'partition_by') else ''
                    ),
                    order_by=(
                        self.build_order_by(
                            window_ast['window_expr']['order_by']
                        ) if window_ast['window_expr'].get('order_by') else ''
                    ),
                    frame=(
                        self.build_frame(
                            window_ast['window_expr']['frame']
                        ) if window_ast['window_expr']['frame'].get(
                            'between') else ''
                    )
                )
            )
        )
