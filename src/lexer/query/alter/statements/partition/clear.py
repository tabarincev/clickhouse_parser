from src.keywords import COLUMN, INDEX

from src.lexer.query.alter.statements.partition.base import (
    MetaPartition, BaseClearPartition
)


class ClearColumn(BaseClearPartition):
    __metaclass__ = MetaPartition
    keyword = COLUMN


class ClearIndex(BaseClearPartition):
    __metaclass__ = MetaPartition
    keyword = INDEX
