from dataflow.base import BaseNode
from ..gen import *
from ..gen.math import MathPowerCall


class PowerNode(BaseNode):
    """
    Raises one number to the power of another

    Inputs
    ------
    base: Base of the power operation

    power: Power to raise the base to

    Outputs
    -------
    result: Power operation from base raised to power
    """

    def __init__(self):
        super().__init__()

        self.declare_input('base')
        self.declare_input('power')
        self.declare_output('result', self.get_output__result, self.deploy_output__result)

    def get_output__result(self, env):
        return self.resolve_input('base', env) ** self.resolve_input('power', env)

    def deploy_output__result(self):
        return LanguageConcat(
            self.resolve_input_deploy('base'),
            self.resolve_input_deploy('power'),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'result'),
                MathPowerCall(
                    self.get_input_connection_variable_name('base'),
                    self.get_input_connection_variable_name('power')
                )
            )
        )
