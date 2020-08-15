from dataflow.OperationNode import OperationNode
from dataflow.gen import *


class GreaterThanOrEqualNode(OperationNode):
    """
    Performs a boolean greater than or equal operation on arg1 and arg2

    Inputs
    ------
    arg1: Left-hand operand for greater than or equal operation

    arg2: Right-hand operand for greater than or equal operation

    Outputs
    -------
    result: Output of the boolean greater or equal than operation
    """

    def __init__(self):
        super().__init__(lambda x, y: x >= y, GreaterThanOrEqualSymbol())
