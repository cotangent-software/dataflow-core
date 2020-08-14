from ..OperationNode import OperationNode
from ..gen import CompareEqualsSymbol


class EqualsNode(OperationNode):
    """
    Checks whether two inputs are equal or not

    Inputs
    ------
    arg1: First operand of the equals statement

    arg2: Second operand of the equals statement

    Outputs
    -------
    result: A boolean being true if arg1 and arg2 are equal and otherwise being false
    """

    def __init__(self):
        super().__init__(lambda x, y: x == y, CompareEqualsSymbol())
