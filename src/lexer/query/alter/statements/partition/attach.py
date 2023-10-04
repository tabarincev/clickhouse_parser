from src.keywords import ATTACH

from src.lexer.query.alter.statements.partition.base import (
    BasePartition, BasePartitionFrom, MetaPartition
)


class AttachPartition(BasePartition):
    __metaclass__ = MetaPartition
    keyword = ATTACH


class AttachPartitionFrom(BasePartitionFrom):
    __metaclass__ = MetaPartition
    keyword = ATTACH
