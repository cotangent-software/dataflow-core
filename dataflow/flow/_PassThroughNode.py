from dataflow.base import BaseNode
from dataflow.gen import LanguageConcat, VariableSetStatement, NodeOutputVariableName


class PassThroughNode(BaseNode):
    """
    Passes data with no variation across a single input and output

    Inputs
    ------
    in: Source of the data to be passed

    Outputs
    -------
    out: Place to pass the input data
    """

    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_output('out', self.get_output__out, self.deploy_output__out)

    def get_output__out(self, env):
        return self.resolve_input('in', env)

    def deploy_output__out(self):
        return LanguageConcat(
            self.resolve_input_deploy('in'),
            VariableSetStatement(NodeOutputVariableName(self.id, 'out'),
                                 self.get_input_connection_variable_name('in'))
        )
