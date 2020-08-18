import math

from dataflow.math._ConstantNode import ConstantNode


class EulerConstantNode(ConstantNode):
    """
    Outputs euler's constant (e)

    Inputs
        None

    Outputs
        value: An approximated value of euler's constant
    """

    def __init__(self):
        super().__init__(math.e)
