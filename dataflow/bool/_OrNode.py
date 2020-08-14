from dataflow.OperationNode import OperationNode
from dataflow.gen import *


class OrNode(OperationNode):
    """
    Performs a boolean or operation on arg1 and arg2

    Inputs
    ------
    arg1: Left-hand operand for or operation

    arg2: Right-hand operand for or operation

    Outputs
    -------
    result: Output of the boolean or operation
    """

    def __init__(self):
        super().__init__(lambda x, y: x or y, BooleanOrSymbol())
