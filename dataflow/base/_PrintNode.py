from dataflow.base import BaseNode
from dataflow.gen import LanguageConcat, VariableSetStatement, PrintStatement, NodeOutputVariableName


class PrintNode(BaseNode):
    """
    Acts as a PassThroughNode, but prints the value which is passed through

    Inputs
        in: Source of the data to be passed

    Outputs
        out: Place to pass the input data
    """

    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_output('out', self.get_output__out, self.deploy_output__out)

    def get_output__out(self, env):
        val = self.resolve_input('in')
        print(val)
        return val

    def deploy_output__out(self):
        return LanguageConcat(
            self.resolve_input_deploy('in'),
            VariableSetStatement(NodeOutputVariableName(self.id, 'out'),
                                 self.get_input_connection_variable_name('in')),
            PrintStatement(NodeOutputVariableName(self.id, 'out'))
        )
