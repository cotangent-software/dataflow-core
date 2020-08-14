from dataflow.math import OperationNode


class SubtractNode(OperationNode):
    """
    Subtracts one number from another

    Inputs
    ------
    arg1: First (left-hand) operand of the subtraction operation

    arg2: Second (right-hand) operand of the subtraction operation

    Outputs
    -------
    result: Difference between inputs arg1 and arg2
    """

    def __init__(self):
        super().__init__('-')
