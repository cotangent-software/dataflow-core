from ..base import BaseNode

from ._AbsoluteValueNode import AbsoluteValueNode
from ._CeilNode import CeilNode
from ._ConstantNode import ConstantNode
from ._DivideNode import DivideNode
from ._EulerConstantNode import EulerConstantNode
from ._FloorNode import FloorNode
from ._LogNode import LogNode
from ._MaxNode import MaxNode
from ._MinNode import MinNode
from ._ModulusNode import ModulusNode
from ._MultiplyNode import MultiplyNode
from ._PiConstantNode import PiConstantNode
from ._PowerNode import PowerNode
from ._RootNode import RootNode
from ._RoundNode import RoundNode
from ._OperationNode import OperationNode
from ._AddNode import AddNode
from ._SubtractNode import SubtractNode

BaseNode.NodeRegistry.extend([
    AddNode,
    SubtractNode,
    MultiplyNode,
    DivideNode,
    ModulusNode,
    PowerNode,
    RootNode,
    LogNode,
    AbsoluteValueNode,
    MinNode,
    MaxNode,
    FloorNode,
    CeilNode,
    RoundNode,
    ConstantNode,
    EulerConstantNode,
    PiConstantNode
])
