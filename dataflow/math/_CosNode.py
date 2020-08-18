import math

from dataflow.FunctionNode import FunctionNode
from dataflow.gen.math import MathCosCall


class CosNode(FunctionNode):
    def __init__(self):
        super().__init__(math.cos, MathCosCall)
