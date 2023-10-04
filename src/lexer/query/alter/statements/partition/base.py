from pyparsing import pyparsing_common
from pyparsing import ParserElement, MatchFirst

from src.lexer.statement import Statement
from src.keywords import PARTITION, PART, FROM, CLEAR, IN


class MetaPartition(type):
    def __new__(cls, name, bases, attrs):
        if not attrs.get('keyword'):
            raise KeyError('Expected a "keyword" class field')

        if not isinstance(attrs['keyword'], ParserElement):
            raise TypeError('Expected "ParserElement" type')

        return super().__new__(cls, name, bases, attrs)


class BasePartition(Statement):
    def __init__(self, column_expr: ParserElement):
        self._partition_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            self.keyword('keyword') + MatchFirst([
                PARTITION, PART
            ])('partition') + self._partition_expr('partition_expr')
        ).set_parse_action(
            lambda term: ({
                '{keyword}_{partition}'.format(
                    keyword=term['keyword'],
                    partition=term['partition']
                ): {'partition_expr': term['partition_expr']}
            })
        )


class BasePartitionFrom(Statement):
    def __init__(self, column_expr: ParserElement):
        self._partition_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            self.keyword('keyword') + PARTITION
            + self._partition_expr('partition_expr')
            + FROM + pyparsing_common.identifier('table')  # todo table_identifier
        ).set_parse_action(
            lambda term: ({
                '{keyword}_partition_from'.format(keyword=term['keyword']): {
                    'partition_expr': term['partition_expr'],
                    'from': term['table']
                }
            })
        )


class BaseClearPartition(Statement):
    def __init__(self, column_expr: ParserElement):
        self._partition_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            CLEAR + self.keyword('keyword')
            + pyparsing_common.identifier('column')  # todo column_identifier
            + IN + PARTITION + self._partition_expr('partition_expr')
        ).set_parse_action(
            lambda term: {
                'clear_{keyword}_in_partition'.format(
                    keyword=term['keyword']
                ): {
                    'column': term['column'],
                    'partition_expr': term['partition_expr']
                }
            }
        )
