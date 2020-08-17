from ._ArrayMergeNode import ArrayMergeNode
from ._DictionaryNode import DictionaryNode
from ._FilterNode import FilterNode
from ._IndexNode import IndexNode
from ._IndexOfNode import IndexOfNode
from ._MapNode import MapNode
from ._SliceNode import SliceNode
from ..base import BaseNode

exported_nodes = [
    MapNode,
    ArrayMergeNode,
    DictionaryNode,
    IndexNode,
    IndexOfNode,
    SliceNode,
    FilterNode
]

__all__ = [x.__name__ for x in exported_nodes]
BaseNode.NodeRegistry.extend(exported_nodes)
