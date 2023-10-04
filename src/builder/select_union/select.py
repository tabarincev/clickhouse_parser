from typing import Dict
from textwrap import dedent

from src.builder.builder import BaseBuilder
from src.builder.columns import ColumnBuilder


class SelectBuilder(BaseBuilder):  # todo не добавляется алиас
    def build(self, ast: Dict) -> str:
        if 'select' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "select" key'
            )

        columns = ([
            ColumnBuilder().build_full_expr(column)
            for column in ast['select']['columns']
        ])

        pre_statement = '{distinct}{top}'.format(
            distinct=(
                'distinct'
                if ast['select'].get('distinct') else ''
            ),
            top='{num}{with_ties}'.format(
                num='top {num}'.format(
                    num=ast['select']['top']
                ) if ast['select'].get('top') else '',
                with_ties=(
                    ' with ties'
                    if ast['select'].get('with_ties') else ''
                )
            )
        )

        if pre_statement:
            columns[0] = '{pre_statement} {column}'.format(
                pre_statement=pre_statement,
                column=columns[0]
            )

        return dedent(
            'select\n{columns}'.format(
                columns=',\n'.join(
                    map(lambda term: '\t{}'.format(term), columns)
                )
            )
        )


if __name__ == '__main__':
    ast = {'select': {'columns': [{'function_term': {'name': 'func', 'args': [{'index_term': {'term': {'column_term': {'column': 'arr'}}, 'index': {'literal_term': {'numeric': '0'}}}}]}}, {'column_term': {'column': 'name'}, 'alias': 'a1'}], 'distinct': True}, 'from': {'join_expr': {'union_distinct': [{'select': {'columns': [{'literal_term': {'numeric': '2'}, 'alias': 'a2'}]}}, {'select': {'columns': [{'literal_term': {'numeric': '4'}}]}}], 'alias': 's2'}}}
    print(SelectBuilder().build(ast))
