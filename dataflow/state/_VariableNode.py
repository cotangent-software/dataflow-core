from dataflow.base import BaseNode
from dataflow.gen import LanguageConcat, VariableSetStatement, NodeOutputVariableName, LanguageValue, FunctionCall


class VariableNode(BaseNode):
    """
    Stores a given value so long as the state is preserved

    Inputs
    ------
    value: New value for the variable if update is triggered

    Outputs
    -------
    value: Nondestructive current value of the variable

    update: Triggers a variable update and passes the updated variable through this output
    """

    def __init__(self, init_value=0):
        super().__init__()

        self.init_value = init_value
        self.state['value'] = self.init_value

        self.declare_input('value')
        self.declare_output('update', self.get_output__update, self.deploy_output__update)
        self.declare_output('value', self.get_output__value, self.deploy_output__value)

    def get_output__update(self, env):
        next_value = self.resolve_input('value', env)
        if next_value is not None:
            self.state['value'] = next_value
        return self.get_output__value(env)

    def deploy_output__update(self):
        return LanguageConcat(
            self.resolve_input_deploy_function('value'),
            self.deploy_state_init('value', LanguageValue(self.init_value)),
            self.deploy_state_update('value', FunctionCall(self.get_input_connection_function_name('value'))),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'update'),
                self.deploy_state_value('value')
            )
        )

    def get_output__value(self, env):
        return self.state['value']

    def deploy_output__value(self):
        return LanguageConcat(
            self.deploy_state_init('value', LanguageValue(self.init_value)),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'value'),
                self.deploy_state_value('value')
            )
        )

    def reset_state(self):
        super().reset_state()
        self.state['value'] = self.init_value
