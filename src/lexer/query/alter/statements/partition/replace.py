from src.keywords import REPLACE

from src.lexer.query.alter.statements.partition.base import (
    BasePartitionFrom, MetaPartition
)


class ReplacePartitionFrom(BasePartitionFrom):
    __metaclass__ = MetaPartition
    keyword = REPLACE
