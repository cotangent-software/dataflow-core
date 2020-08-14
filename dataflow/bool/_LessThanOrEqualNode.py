from dataflow.OperationNode import OperationNode
from dataflow.gen import *


class LessThanOrEqualNode(OperationNode):
    """
    Performs a boolean less than or equal operation on arg1 and arg2

    Inputs
    ------
    arg1: Left-hand operand for less than or equal operation

    arg2: Right-hand operand for less than or equal operation

    Outputs
    -------
    result: Output of the boolean less or equal than operation
    """

    def __init__(self):
        super().__init__(lambda x, y: x > y, LessThanOrEqualSymbol())
