import math

from dataflow.FunctionNode import FunctionNode
from dataflow.gen.math import MathTanCall


class TanNode(FunctionNode):
    def __init__(self):
        super().__init__(math.tan, MathTanCall)
