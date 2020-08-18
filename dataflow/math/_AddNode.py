from dataflow.OperationNode import OperationNode
from ..gen import AddSymbol


class AddNode(OperationNode):
    """
    Adds two numbers together

    Inputs
        arg1: First (left-hand) operand of the addition operation

        arg2: Second (right-hand) operand of the addition operation

    Outputs
        result: Sum of inputs arg1 and arg2
    """

    def __init__(self):
        super().__init__(lambda x, y: x + y, AddSymbol())
