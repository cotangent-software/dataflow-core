from dataflow.base import BaseNode
from dataflow.gen import *
from dataflow.math._CeilOperation import CeilOperation
from dataflow.math._FloorOperation import FloorOperation

import math


class RoundNode(BaseNode):
    """
    Rounds the input value to the nearest whole number

    Inputs
    ------
    value: The value which should be rounded

    Outputs
    -------
    result: Rounded value
    """

    def __init__(self):
        super().__init__()

        self.declare_input('value')
        self.declare_output('result', self.get_output__result, self.deploy_output__result)

    def get_output__result(self, env):
        val = self.resolve_input('value', env)
        if val % 1 == 0.5:
            return math.ceil(val)
        return round(val)

    def deploy_output__result(self):
        value_var = self.get_input_connection_variable_name('value')
        result_var = NodeOutputVariableName(self.id, 'result')
        return LanguageConcat(
            self.resolve_input_deploy('value'),
            VariableSetStatement(
                result_var,
                FloorOperation(value_var)
            ),
            IfStatement(
                LanguageOperation(
                    GreaterThanOrEqualSymbol(),
                    LanguageOperation(
                        SubtractSymbol(),
                        value_var,
                        result_var
                    ),
                    LanguageValue(0.5)
                ),
                VariableSetStatement(
                    result_var,
                    CeilOperation(value_var)
                )
            )
        )
