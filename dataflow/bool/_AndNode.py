from dataflow.OperationNode import OperationNode
from dataflow.gen import *


class AndNode(OperationNode):
    """
    Performs a boolean and operation on arg1 and arg2

    Inputs
        arg1: Left-hand operand for and operation

        arg2: Right-hand operand for and operation

    Outputs
        result: Output of the boolean and operation
    """

    def __init__(self):
        super().__init__(lambda x, y: x and y, BooleanAndSymbol())
