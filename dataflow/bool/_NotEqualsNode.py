from ..base import BaseNode, ExtendedNode
from ._EqualsNode import EqualsNode
from ._NotNode import NotNode


class NotEqualsNode(ExtendedNode):
    """
    Checks whether two inputs are not equal

    Inputs
    ------
    arg1: First operand of the not equals statement

    arg2: Second operand of the not equals statement

    Outputs
    -------
    result: A boolean being true if arg1 and arg2 are not equal and otherwise being false
    """

    def __init__(self):
        super().__init__()

        self.equals_node = EqualsNode()
        self.not_node = NotNode()

        BaseNode.connect(self.equals_node, self.not_node, 'result', 'in')

        self.declare_extended_input('arg1', self.equals_node, 'arg1')
        self.declare_extended_input('arg2', self.equals_node, 'arg2')
        self.declare_extended_output('result', self.not_node, 'out')
