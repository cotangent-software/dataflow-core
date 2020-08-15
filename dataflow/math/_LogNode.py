from dataflow.base import BaseNode
from dataflow.gen import *
from dataflow.gen.math import MathLogCall

import math


class LogNode(BaseNode):
    """
    Takes the log of a value given a base

    Inputs
    ------
    value: Value to take the logarithm of

    base: Base of the logarithm

    Outputs
    -------
    result: The value of log base of value
    """

    def __init__(self):
        super().__init__()

        self.declare_input('value')
        self.declare_input('base')
        self.declare_output('result', self.get_output__result, self.deploy_output__result)

    def get_output__result(self, env):
        return math.log(self.resolve_input('value', env), self.resolve_input('base', env))

    def deploy_output__result(self):
        return LanguageConcat(
            self.resolve_input_deploy('value'),
            self.resolve_input_deploy('base'),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'result'),
                MathLogCall(
                    self.get_input_connection_variable_name('value'),
                    self.get_input_connection_variable_name('base')
                )
            )
        )
