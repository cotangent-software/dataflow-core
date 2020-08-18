from dataflow.base import BaseNode
from dataflow.gen import LanguageConcat, ConditionalLoopStatement, FunctionCall, LanguageNoop, VariableSetStatement, \
    NodeOutputVariableName


class LoopNode(BaseNode):
    """
    Loops a certain number of times based on the state of an input

    Inputs
        iter: Node will continue to loop as long as this input resolves to be boolean true

        value: The value which will be passed through once iter becomes false

    Outputs
        value: Outputted value of the loop, passed through from the value input
    """

    def __init__(self):
        super().__init__()

        self.declare_input('iter')
        self.declare_input('value')
        self.declare_input('__continue__')
        self.declare_output('value', self.get_output__value, self.deploy_output__value)
        self.declare_output('__continue__', self.get_output____continue__)

        BaseNode.connect(self, self, '__continue__', '__continue__')

        self.state['init'] = False

    def get_output__value(self, env):
        if self.resolve_input('iter'):
            return self.resolve_input('__continue__', env)
        else:
            return self.resolve_input('value', env)

    def deploy_output__value(self):
        return LanguageConcat(
            self.resolve_input_deploy_function('iter'),
            ConditionalLoopStatement(
                FunctionCall(self.get_input_connection_function_name('iter')),
                LanguageNoop()
            ),
            self.resolve_input_deploy('value'),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'value'),
                self.get_input_connection_variable_name('value')
            )
        )

    def get_output____continue__(self, env):
        return self.get_output__value(env)
