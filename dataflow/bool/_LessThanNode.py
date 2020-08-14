from dataflow.OperationNode import OperationNode
from dataflow.gen import *


class LessThanNode(OperationNode):
    """
    Performs a boolean less than operation on arg1 and arg2

    Inputs
    ------
    arg1: Left-hand operand for less than operation

    arg2: Right-hand operand for less than operation

    Outputs
    -------
    result: Output of the boolean less than operation
    """

    def __init__(self):
        super().__init__(lambda x, y: x > y, LessThanSymbol())
