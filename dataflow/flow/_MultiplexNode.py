from dataflow.base import BaseNode
from dataflow.gen import LanguageConcat, NodeOutputVariableName, VariableSetStatement, LanguageNone, IfStatement, \
    LanguageOperation, CompareEqualsSymbol, LanguageValue


class MultiplexNode(BaseNode):
    """
    Chooses the input corresponding to the given number. If less than 0, chooses 0. If greater than "count",
    chooses last input

    Inputs
    ------
    number: Number from which to choose the input

    in_<n>: Value to be resolved given 'number' resolves to be equal to <n>

    Outputs
    -------
    value: The value of the chosen 'in_<n>' input
    """
    def __init__(self, count: int):
        super().__init__()

        self.count = count

        self.declare_input('number')
        for n in range(count):
            self.declare_input(f'in_{n}')
        self.declare_output('value', self.get_output__value, self.deploy_output__value)

    def get_output__value(self, env):
        num = self.resolve_input('number', env)
        if num < 0:
            return self.resolve_input('in_0', env)
        if num >= self.count:
            return self.resolve_input(f'in_{self.count - 1}', env)
        return self.resolve_input(f'in_{num}')

    def deploy_output__value(self):
        num_var = self.get_input_connection_variable_name('number')
        value_var = NodeOutputVariableName(self.id, 'value')

        if_statements = []
        for n in range(self.count):
            if_statements.append(
                IfStatement(
                    LanguageOperation(
                        CompareEqualsSymbol(),
                        num_var,
                        LanguageValue(n)
                    ),
                    LanguageConcat(
                        self.resolve_input_deploy(f'in_{n}'),
                        VariableSetStatement(
                            value_var,
                            self.get_input_connection_variable_name(f'in_{n}')
                        )
                    ),
                    if_type='if' if n == 0 else 'elseif' if n != self.count - 1 else 'else'
                )
            )

        return LanguageConcat(
            self.resolve_input_deploy('number'),
            VariableSetStatement(
                value_var,
                LanguageNone()
            ),
            *if_statements
        )
