from dataflow.base import BaseNode
from dataflow.gen import *


class ConstantNode(BaseNode):
    """
    Nearly the same as DataSourceNode, but stores only numbers and outputs them from value

    Inputs
    ------
    None

    Outputs
    -------
    value: The value associated with the constant
    """
    def __init__(self, value: Union[int, float]):
        super().__init__()

        self.value = value

        self.declare_output('value', self.get_output__value, self.deploy_output__value)

    def get_output__value(self, env):
        return self.value

    def deploy_output__value(self):
        return VariableSetStatement(
            NodeOutputVariableName(self.id, 'value'),
            LanguageValue(self.value)
        )
