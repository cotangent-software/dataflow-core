from dataflow.OperationNode import OperationNode
from ..gen import DivideSymbol


class DivideNode(OperationNode):
    """
    Divides two numbers

    Inputs
    ------
    arg1: First (left-hand) operand of the division operation

    arg2: Second (right-hand) operand of the division operation

    Outputs
    -------
    result: Quotient of inputs arg1 and arg2
    """

    def __init__(self):
        super().__init__(lambda x, y: x / y, DivideSymbol())
