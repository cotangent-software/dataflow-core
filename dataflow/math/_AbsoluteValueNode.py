from dataflow.base import BaseNode
from dataflow.gen import *
from dataflow.gen.math import MathAbsoluteValueCall


class AbsoluteValueNode(BaseNode):
    """
    Takes the absolute value of the input connection

    Inputs
    ------
    in: Number to take the absolute value of

    Outputs
    -------
    result: Absolute value of input in
    """

    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_output('result', self.get_output__out, self.deploy_output__out)

    def get_output__out(self, env):
        return abs(self.resolve_input('in', env))

    def deploy_output__out(self):
        return LanguageConcat(
            self.resolve_input_deploy('in'),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'result'),
                MathAbsoluteValueCall(self.get_input_connection_variable_name('in'))
            )
        )
