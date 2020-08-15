from dataflow.base import BaseNode
from dataflow.gen import LanguageConcat, VariableSetStatement, NodeOutputVariableName, ParseFloatCall


class ParseFloatNode(BaseNode):
    """
    Parses an input type to a float

    Inputs
    ------
    in: Source of the data to be parsed

    Outputs
    -------
    out: Parsed float output
    """

    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_output('out', self.get_output__out, self.deploy_output__out)

    def get_output__out(self, env):
        return float(self.resolve_input('in', env))

    def deploy_output__out(self):
        return LanguageConcat(
            self.resolve_input_deploy('in'),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'out'), ParseFloatCall(self.get_input_connection_variable_name('in'))
            )
        )
