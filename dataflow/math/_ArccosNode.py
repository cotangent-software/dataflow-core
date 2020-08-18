import math

from dataflow.FunctionNode import FunctionNode
from dataflow.gen.math import MathArccosCall


class ArccosNode(FunctionNode):
    def __init__(self):
        super().__init__(math.acos, MathArccosCall)
