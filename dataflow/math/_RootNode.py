from dataflow.base import BaseNode
from ..gen import *
from ..gen.math import MathRootCall


class RootNode(BaseNode):
    """
    Takes the nth root of a number

    Inputs
        value: Value to take the nth root of

        root: Root to take of value. ex. root 2 would be a square root

    Outputs
        result: Nth root of value
    """

    def __init__(self):
        super().__init__()

        self.declare_input('value')
        self.declare_input('root')
        self.declare_output('result', self.get_output__result, self.deploy_output__result)

    def get_output__result(self, env):
        return self.resolve_input('value', env) ** (1 / self.resolve_input('root', env))

    def deploy_output__result(self):
        return LanguageConcat(
            self.resolve_input_deploy('value'),
            self.resolve_input_deploy('root'),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'result'),
                MathRootCall(
                    self.get_input_connection_variable_name('value'),
                    self.get_input_connection_variable_name('root')
                )
            )
        )
