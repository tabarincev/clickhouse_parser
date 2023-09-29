from typing import Dict

from src.builder.builder import BaseBuilder

from src.builder.select_union.cte import CTEBuilder
from src.builder.select_union.select import SelectBuilder
from src.builder.select_union.from_ import FromBuilder
from src.builder.select_union.array_join import ArrayJoinBuilder
from src.builder.select_union.window import WindowBuilder
from src.builder.select_union.prewhere import PreWhereBuilder
from src.builder.select_union.where import WhereBuilder
from src.builder.select_union.group_by import GroupByBuilder
from src.builder.select_union.having import HavingBuilder
from src.builder.select_union.order_by import OrderByBuilder
from src.builder.select_union.limit_by import LimitByBuilder
from src.builder.select_union.limit import LimitBuilder
from src.builder.select_union.settings import SettingsBuilder


class SelectTermBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'select' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - '
                'Expected necessary "select" key'
            )
        result = ''

        if 'cte' in ast:
            result += f'{CTEBuilder().build(ast)}\n'

        result += f'{SelectBuilder().build(ast)}\n'

        if 'from' in ast:
            result += f'{FromBuilder().build(ast)}\n'

        if 'array_join' in ast:
            result += f'{ArrayJoinBuilder().build(ast)}\n'

        if 'window' in ast:
            result += f'{WindowBuilder().build(ast)}\n'

        if 'prewhere' in ast:
            result += f'{PreWhereBuilder().build(ast)}\n'

        if 'where' in ast:
            result += f'{WhereBuilder().build(ast)}\n'

        if 'group_by' in ast:
            result += f'{GroupByBuilder().build(ast)}\n'

            if 'having' in ast:
                result += f'{HavingBuilder().build(ast)}\n'

        if 'order_by' in ast:
            result += f'{OrderByBuilder().build(ast)}\n'

        if 'limit_by' in ast:
            result += f'{LimitByBuilder().build(ast)}\n'

        if 'limit' in ast:
            result += f'{LimitBuilder().build(ast)}\n'

        if 'settings' in ast:
            result += f'{SettingsBuilder().build(ast)}\n'
        return result


ast = {'select': {'columns': [{'index_term': {'term': {'function_term': {'name': 'func', 'args': [{'column_term': {'column': 'name'}}], 'distinct': True}}, 'index': {'literal_term': {'numeric': 0}}}, 'alias': 'a2'}]}, 'from': {'join_expr': {'table_identifier': {'database': 't', 'table': 'a'}}}}

print(SelectTermBuilder().build(ast))
