from ..base import BaseNode
from ..gen import *


class NotNode(BaseNode):
    """
    A boolean logic node performing the boolean not operation

    Inputs
        in: Boolean value to be transformed

    Outputs
        out: Boolean value representing the boolean not operation performed on input in
    """

    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_output('out', self.get_output__out, self.deploy_output__out)

    def get_output__out(self, env):
        return not self.resolve_input('in', env)

    def deploy_output__out(self):
        return LanguageConcat(
            self.resolve_input_deploy('in'),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'out'),
                LanguageOperation(
                    BooleanNotSymbol(),
                    None,
                    self.get_input_connection_variable_name('in')
                )
            )
        )
