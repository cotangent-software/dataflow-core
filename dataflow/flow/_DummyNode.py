from dataflow.base import BaseNode
from dataflow.gen import LanguageConcat, VariableSetStatement, NodeOutputVariableName


class DummyNode(BaseNode):
    """
    Passes through an input while requiring another input and throwing its value out

    Inputs
        in: Input value to be passed on to output

        extra: Input value which will be resolved but then thrown out

    Outputs
        out: Resolved value of the in input
    """

    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_input('extra')
        self.declare_output('out', self.get_output__out, self.deploy_output__out)

    def get_output__out(self, env):
        self.resolve_input('extra', env)
        return self.resolve_input('in', env)

    def deploy_output__out(self):
        return LanguageConcat(
            self.resolve_input_deploy('extra'),
            self.resolve_input_deploy('in'),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'out'),
                self.get_input_connection_variable_name('in')
            )
        )
