from dataflow.base import BaseNode
from dataflow.gen import IfStatement, LanguageOperation, CompareEqualsSymbol, FunctionCall, VariableSetStatement, \
    NodeOutputVariableName, LanguageConcat, LanguageNone


class SwitchNode(BaseNode):
    """
    Depending on an input value, choose which path to return on the basis of the value's equality with a test

    Inputs
    ------
    value: Value which will be tested for equality

    default: Returned path given that no equality test is satisfied

    test_<n>: Value which equality should be tested for

    return_<n>: Associated return path given that test_<n> is satisfied

    Outputs
    -------
    selected: Outputted value of the selected return path
    """

    def __init__(self, condition_count):
        super().__init__()

        self.condition_count = condition_count

        self.declare_input('value')
        self.declare_input('default')
        for n in range(self.condition_count):
            self.declare_input('test_%d' % n)
            self.declare_input('return_%d' % n)
        self.declare_output('selected', self.get_output__selected, self.deploy_output__selected)

    def get_output__selected(self, env):
        value = self.resolve_input('value', env)
        for n in range(self.condition_count):
            if self.resolve_input('test_%d' % n, env) == value:
                return self.resolve_input('return_%d' % n, env)
        default_value = self.resolve_input('default', env, allow_unconnected=True)
        return default_value

    def deploy_output__selected(self):
        test_functions = []
        return_functions = []
        if_statements = []
        for n in range(self.condition_count):
            test_functions.append(self.resolve_input_deploy_function('test_%d' % n))
            return_functions.append(self.resolve_input_deploy_function('return_%d' % n))
            if_statements.append(
                IfStatement(
                    LanguageOperation(
                        CompareEqualsSymbol(),
                        FunctionCall(self.get_input_connection_function_name('test_%d' % n)),
                        self.get_input_connection_variable_name('value')
                    ),
                    VariableSetStatement(
                        NodeOutputVariableName(self.id, 'selected'),
                        FunctionCall(self.get_input_connection_function_name('return_%d' % n))
                    ),
                    if_type=('if' if n == 0 else 'elseif')
                )
            )
        return_functions.append(self.resolve_input_deploy_function('default'))
        if_statements.append(
            IfStatement(
                None,
                VariableSetStatement(
                    NodeOutputVariableName(self.id, 'selected'),
                    FunctionCall(self.get_input_connection_function_name('default'))
                ),
                if_type='else'
            )
        )

        return LanguageConcat(
            self.resolve_input_deploy('value'),
            *test_functions,
            *return_functions,
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'selected'),
                LanguageNone()
            ),
            *if_statements
        )
