from dataflow.base import BaseNode
from dataflow.gen import *
from dataflow.math._FloorOperation import FloorOperation

import math


class FloorNode(BaseNode):
    """
    Performs the floor operation on a number

    Inputs
        value: The value for which floor should be performed

    Outputs
        result: Output of the floor operation performed on value
    """

    def __init__(self):
        super().__init__()

        self.declare_input('value')
        self.declare_output('result', self.get_output__result, self.deploy_output__result)

    def get_output__result(self, env):
        return math.floor(self.resolve_input('value', env))

    def deploy_output__result(self):
        return LanguageConcat(
            self.resolve_input_deploy('value'),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'result'),
                FloorOperation(self.get_input_connection_variable_name('value'))
            )
        )
