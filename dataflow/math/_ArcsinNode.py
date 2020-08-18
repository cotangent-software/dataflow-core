import math

from dataflow.FunctionNode import FunctionNode
from dataflow.gen.math import MathArcsinCall


class ArcsinNode(FunctionNode):
    def __init__(self):
        super().__init__(math.asin, MathArcsinCall)
