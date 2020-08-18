from dataflow.base import BaseNode
from dataflow.gen import LanguageConcat, VariableSetStatement, NodeOutputVariableName


class FunctionNode(BaseNode):
    """
    Generic superclass node for single-parameter functions

    Inputs
        in: Input value for the parameter of the function

    Outputs
        out: Output value of the function given input 'in'
    """
    def __init__(self, func, dep_func):
        super().__init__()

        self.func = func
        self.dep_func = dep_func

        self.declare_input('in')
        self.declare_output('out', self.get_output__out, self.deploy_output__out)

    def get_output__out(self, env):
        return self.func(self.resolve_input('in', env))

    def deploy_output__out(self, env):
        return LanguageConcat(
            self.resolve_input_deploy('in'),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'out'),
                self.dep_func(self.get_input_connection_variable_name('in'))
            )
        )
