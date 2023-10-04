from src.keywords import DETACH

from src.lexer.query.alter.statements.partition.base import (
    BasePartition, MetaPartition
)


class DetachPartition(BasePartition):
    __metaclass__ = MetaPartition
    keyword = DETACH
