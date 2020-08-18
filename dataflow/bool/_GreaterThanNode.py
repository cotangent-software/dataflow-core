from dataflow.OperationNode import OperationNode
from dataflow.gen import *


class GreaterThanNode(OperationNode):
    """
    Performs a boolean greater than operation on arg1 and arg2

    Inputs
        arg1: Left-hand operand for greater than operation

        arg2: Right-hand operand for greater than operation

    Outputs
        result: Output of the boolean greater than operation
    """

    def __init__(self):
        super().__init__(lambda x, y: x > y, GreaterThanSymbol())
