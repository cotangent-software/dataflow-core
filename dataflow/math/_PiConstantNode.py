import math

from dataflow.math._ConstantNode import ConstantNode


class PiConstantNode(ConstantNode):
    """
    Outputs pi constant

    Inputs
        None

    Outputs
        value: An approximated value of pi
    """

    def __init__(self):
        super().__init__(math.pi)
