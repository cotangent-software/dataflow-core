import math

from dataflow.FunctionNode import FunctionNode
from dataflow.gen.math import MathSinCall


class SinNode(FunctionNode):
    def __init__(self):
        super().__init__(math.sin, MathSinCall)
