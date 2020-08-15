from dataflow.base._BaseNode import BaseNode
from dataflow.gen import VariableSetStatement, NodeOutputVariableName, LanguageValue


class DataSourceNode(BaseNode):
    """
    Acts as an output-only node which sends a predetermined constant output

    Inputs
    ------
    None

    Outputs
    -------
    data: Predetermined constant output
    """

    def __init__(self, data):
        super().__init__()

        self.data = data

        self.declare_output('data', self.get_output__data, self.deploy_output__data)

    def get_output__data(self, env):
        return self.data

    def deploy_output__data(self):
        return VariableSetStatement(NodeOutputVariableName(self.id, 'data'), LanguageValue(self.data))
