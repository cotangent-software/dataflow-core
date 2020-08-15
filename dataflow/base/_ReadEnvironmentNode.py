from dataflow.gen import VariableSetStatement, NodeOutputVariableName, VariableName
from dataflow.object import IndexNode


class ReadEnvironmentNode(IndexNode):
    """
    Returns the environment state as an object

    Inputs
    ------
    None

    Outputs
    -------
    value: The value of the environment state in object form
    """

    def __init__(self):
        super().__init__()

        self.declare_output('value', self.get_output__value, self.deploy_output__value)

    def get_output__value(self, env):
        return env

    def deploy_output__value(self):
        return VariableSetStatement(
            NodeOutputVariableName(self.id, 'value'),
            VariableName('env')
        )
