from dataflow.OperationNode import OperationNode
from ..gen import ModuloSymbol


class ModulusNode(OperationNode):
    """
    Takes the modulus of two numbers

    Inputs
        arg1: First (left-hand) operand of the modulus operation

        arg2: Second (right-hand) operand of the modulus operation

    Outputs
        result: Modulus of inputs arg1 and arg2
    """

    def __init__(self):
        super().__init__(lambda x, y: x % y, ModuloSymbol())
