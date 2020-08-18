import math

from dataflow.FunctionNode import FunctionNode
from dataflow.gen.math import MathArctanCall


class ArctanNode(FunctionNode):
    def __init__(self):
        super().__init__(math.atan, MathArctanCall)
