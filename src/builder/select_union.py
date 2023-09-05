from typing import Dict
from abc import ABC, abstractmethod
from src.builder.columns import ColumnBuilder


class BaseBuilder(ABC):
    @abstractmethod
    def build(self, ast: Dict) -> str:
        pass


class CTEBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'with' not in ast:
            raise ValueError('')
        return 'with {with_exprs}'.format(
            with_exprs=', '.join([
                ColumnBuilder().build_full_expr(expr)
                for expr in ast['with']['exprs']
            ])
        )


class SelectBuilder(BaseBuilder):  # todo не добавляется алиас
    def build(self, ast: Dict) -> str:
        if 'select' not in ast:
            raise ValueError('')
        return 'select {distinct} {top} {columns}'.format(
            distinct='distinct' if ast['select'].get('distinct') else '',
            top='top {top_nums} {with_ties}'.format(
                top_nums=ast['select']['top'],
                with_ties='with ties'
            ),
            columns=', '.join([
                ColumnBuilder().build_full_expr(column)
                for column in ast['select']['columns']
            ])
        )


# class FromBuilder(BaseBuilder):
#     def build(self, ast: Dict) -> str:
#         if 'from' not in ast:
#             raise ValueError('')
#         return 'from {join_expr}'.format(join_expr=)
#
#
# class ArrayJoinBuilder(BaseBuilder):
#     def build(self, ast: Dict) -> str:
#         if 'array_join' not in ast:
#             raise ValueError('')
#         return 'array {join_type} join'.format(join_type=)
#
#
# class WindowBuilder(BaseBuilder):
#     def build(self, ast: Dict) -> str:
#         pass
#
#
class PreWhereBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'prewhere' not in ast:
            raise ValueError('')
        return 'prewhere {prewhere_expr}'.format(
            prewhere_expr=ColumnBuilder().build_full_expr(
                ast['prewhere']['expr']
            )
        )


class WhereBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'where' not in ast:
            raise ValueError('')
        return 'where {where_expr}'.format(
            where_expr=ColumnBuilder().build_full_expr(
                ast['where']['expr']
            )
        )


# class GroupByBuilder(BaseBuilder):
#     def build(self, ast: Dict) -> str:
#         if 'group_by' not in ast:
#             raise ValueError('')
#         return 'group by {group_by_expr}'.format(
#             group_by_expr=
#         )
#
#
class HavingBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'having' not in ast:
            raise ValueError('')
        return 'having {having_expr}'.format(
            having_expr=ColumnBuilder().build_full_expr(
                ast['having']['expr']
            )
        )


# class OrderByBuilder(BaseBuilder):
#     def build(self, ast: Dict) -> str:
#         if 'order_by' not in ast:
#             raise ValueError('')
#         return 'order by {order_by_expr}'.format(
#             order_by_expr=
#         )
#
#
# class LimitByBuilder(BaseBuilder):
#     def build(self, ast: Dict) -> str:
#         if 'limit_by' not in ast:
#             raise ValueError('')
#         return 'limit {limit_expr} by {by_expr}'.format(
#             limit_expr=1,
#             by_expr=2
#         )
#
#
# class LimitBuilder(BaseBuilder):
#     def build(self, ast: Dict) -> str:
#         pass


class SettingsBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'settings' not in ast:
            raise ValueError('')
        return 'settings {settings_list}'.format(
            settings_list=','.join([
                '{name}={value}'.format(
                    name=setting['setting'],
                    value=setting['value']
                ) for setting in ast['select']['settings']
            ])
        )


class FormatBuilder(BaseBuilder):
    def build(self, ast: Dict) -> str:
        if 'format' not in ast:
            raise ValueError('')
        return 'format {format_file}'.format(format_file=ast['format_file'])
