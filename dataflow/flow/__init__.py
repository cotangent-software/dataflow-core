from ._DummyNode import DummyNode
from ._IfNode import IfNode
from ._LoopNode import LoopNode
from ._MultiplexNode import MultiplexNode
from ._PassThroughNode import PassThroughNode
from ._SwitchNode import SwitchNode
from ..base import BaseNode

exported_nodes = [
    PassThroughNode,
    IfNode,
    SwitchNode,
    MultiplexNode,
    LoopNode,
    DummyNode
]

__all__ = [x.__name__ for x in exported_nodes]
BaseNode.NodeRegistry.extend(exported_nodes)
