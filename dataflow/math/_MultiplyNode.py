from dataflow.OperationNode import OperationNode
from ..gen import MultiplySymbol


class MultiplyNode(OperationNode):
    """
    Multiplies two numbers together

    Inputs
        arg1: First (left-hand) operand of the multiplication operation

        arg2: Second (right-hand) operand of the multiplication operation

    Outputs
        result: Product of inputs arg1 and arg2
    """

    def __init__(self):
        super().__init__(lambda x, y: x * y, MultiplySymbol())
