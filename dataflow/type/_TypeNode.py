from dataflow.base import BaseNode
from dataflow.gen import LanguageConcat, VariableSetStatement, NodeOutputVariableName, FunctionCall, VariableName


class TypeNode(BaseNode):
    """
    Outputs a string containing the type of the input

    Inputs
    ------
    in: Value to check the type of

    Outputs
    -------
    out: String value of input type
    """

    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_output('out', self.get_output__out, self.deploy_output__out)

    def get_output__out(self, env):
        t = self.resolve_input('in', env).__class__
        if t == dict:
            return 'dict'
        if t == list:
            return 'array'
        if t == int:
            return 'int'
        if t == float:
            return 'float'
        if t == str:
            return 'string'
        return t

    def deploy_output__out(self):
        return LanguageConcat(
            self.resolve_input_deploy('in'),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'out'),
                FunctionCall(VariableName('utils_type'), self.get_input_connection_variable_name('in'))
            )
        )
