from .attach import AttachPartition, AttachPartitionFrom
from .clear import ClearColumn, ClearIndex
from .detach import DetachPartition
from .drop import DropPartition, DropDetachedPartition
from .fetch import FetchPartition
from .freeze import FreezePartition, UnfreezePartition
from .move import MovePartition
from .move_to_table import MoveToPartition
from .replace import ReplacePartitionFrom
from .update import UpdatePartition
from .main import AlterPartition


__all__ = [
    AttachPartition,
    AttachPartitionFrom,
    ClearColumn,
    ClearIndex,
    DetachPartition,
    DropPartition,
    DropDetachedPartition,
    FetchPartition,
    FreezePartition,
    UnfreezePartition,
    MovePartition,
    MoveToPartition,
    ReplacePartitionFrom,
    UpdatePartition,
    AlterPartition
]
