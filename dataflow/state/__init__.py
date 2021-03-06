from ._IncrementNode import IncrementNode
from ._VariableNode import VariableNode
from ..base import BaseNode

exported_nodes = [
    VariableNode,
    IncrementNode
]

__all__ = [x.__name__ for x in exported_nodes]
BaseNode.NodeRegistry.extend(exported_nodes)
