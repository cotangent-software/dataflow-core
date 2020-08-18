from dataflow.base import BaseNode
from dataflow.gen import NodeOutputVariableName, LanguageConcat, VariableSetStatement, LanguageValue, \
    LanguageOperation, AddSymbol


class IncrementNode(BaseNode):
    """
    Keeps an internal state which will be incremented or read depending on activated output

    Inputs
        None

    Outputs
        increment: First adds 1 to internal state, then outputs new value

    value: Reads the internal state without modifying it
    """

    def __init__(self):
        super().__init__()

        self.state['value'] = 0

        self.declare_output('increment', self.get_output__increment, self.deploy_output__increment)
        self.declare_output('value', self.get_output__value, self.deploy_output__value)

    def get_output__increment(self, env):
        self.state['value'] += 1
        return self.state['value']

    def deploy_output__increment(self):
        increment_var = NodeOutputVariableName(self.id, 'increment')

        return LanguageConcat(
            self.deploy_state_init('value', LanguageValue(0)),
            VariableSetStatement(
                increment_var,
                LanguageOperation(
                    AddSymbol(),
                    self.deploy_state_value('value'),
                    LanguageValue(1)
                )
            ),
            self.deploy_state_update('value', increment_var)
        )

    def get_output__value(self, env):
        return self.state['value']

    def deploy_output__value(self):
        return LanguageConcat(
            self.deploy_state_init('value', LanguageValue(0)),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'value'),
                self.deploy_state_value('value')
            )
        )
