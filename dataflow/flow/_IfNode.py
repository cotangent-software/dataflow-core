from dataflow.base import BaseNode
from dataflow.gen import LanguageConcat, IfStatement, NodeOutputVariableName, VariableSetStatement, LanguageNoop


class IfNode(BaseNode):
    """
    Resolves one input if a condition is true and another if it is false

    Inputs
        condition: A boolean value which will resolve if input if true and else input if false

        if: Input resolved when the input 'condition' is true

        else: Input resolved when the input 'condition' is false

    Outputs
        value: The value of either 'if' or 'else', depending on the value of 'condition'
    """

    def __init__(self):
        super().__init__()

        self.declare_input('condition')
        self.declare_input('if')
        self.declare_input('else')
        self.declare_output('value', self.get_output__value, self.deploy_output__value)

    def get_output__value(self, env):
        if self.resolve_input('condition', env):
            return self.resolve_input('if', env)
        else:
            return self.resolve_input('else', env)

    def deploy_output__value(self):
        value_var = NodeOutputVariableName(self.id, 'value')
        return LanguageConcat(
            self.resolve_input_deploy('condition'),
            IfStatement(
                self.get_input_connection_variable_name('condition'),
                LanguageConcat(
                    self.resolve_input_deploy('if'),
                    VariableSetStatement(
                        value_var,
                        self.get_input_connection_variable_name('if')
                    )
                )
            ),
            IfStatement(
                None,
                LanguageConcat(
                    self.resolve_input_deploy('else'),
                    VariableSetStatement(
                        value_var,
                        self.get_input_connection_variable_name('else')
                    )
                )
            )
        )
