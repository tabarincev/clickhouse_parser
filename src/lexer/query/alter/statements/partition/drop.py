from src.keywords import DROP, DETACHED

from src.lexer.query.alter.statements.partition.base import (
    BasePartition, MetaPartition
)


class DropPartition(BasePartition):
    __metaclass__ = MetaPartition
    keyword = DROP


class DropDetachedPartition(BasePartition):
    __metaclass__ = MetaPartition
    keyword = DROP + DETACHED
