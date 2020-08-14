from dataflow.base import BaseNode
from dataflow.gen import *


class MinNode(BaseNode):
    """
    Takes the minimum between two inputs

    Inputs
    ------
    arg1: First input to check

    arg2: Second input to check

    Outputs
    -------
    result: Smaller of the two input values
    """

    def __init__(self):
        super().__init__()

        self.declare_input('arg1')
        self.declare_input('arg2')
        self.declare_output('result', self.get_output__result, self.deploy_output__result)

    def get_output__result(self, env):
        return min(self.resolve_input('arg1', env), self.resolve_input('arg2', env))

    def deploy_output__result(self):
        result_var = NodeOutputVariableName(self.id, 'result')
        return LanguageConcat(
            self.resolve_input_deploy('arg1'),
            self.resolve_input_deploy('arg2'),
            VariableSetStatement(
                result_var,
                self.get_input_connection_variable_name('arg1')
            ),
            IfStatement(
                LanguageOperation(
                    LessThanSymbol(),
                    self.get_input_connection_variable_name('arg2'),
                    result_var
                ),
                VariableSetStatement(
                    result_var,
                    self.get_input_connection_variable_name('arg2')
                )
            )
        )
