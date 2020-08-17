from dataflow.base import BaseNode
from dataflow.gen import LanguageNoop, NodePrivateVariableName, LanguageConcat, VariableSetStatement, \
    NodeOutputVariableName, ArrayIndex, LanguageValue, LanguageNone, SimpleLoopStatement, UtilsArrayLength, FunctionCall


class ReduceNode(BaseNode):
    """
    Reduces all array values into a single value based on an internal accumulator network

    Inputs
    ------
    array: Array to be reduced

    accumulator (internal): New accumulated value accounting for current array value

    Outputs
    -------
    reduced: Outputted reduced value of the inputted array

    accumulator (internal): Current accumulated value

    current (internal): Current value to factor into the current accumulated value
    """

    def __init__(self):
        super().__init__()

        self.declare_input('array')
        self.declare_input('accumulator', internal=True)
        self.declare_output('reduced', self.get_output__reduced, self.deploy_output__reduced)
        self.declare_output('accumulator', self.get_ioutput__accumulator, self.deploy_ioutput__accumulator, internal=True)
        self.declare_output('current', self.get_ioutput__current, self.deploy_ioutput__current, internal=True)

    def get_output__reduced(self, env):
        arr = self.resolve_input('array', env)
        acc = arr[0]
        for i in range(1, len(arr)):
            self.state['current_accumulator'] = acc
            self.state['current_value'] = arr[i]
            acc = self.resolve_input('accumulator', env)
        return acc

    def deploy_output__reduced(self):
        array_var = self.get_input_connection_variable_name('array')
        i_var = NodePrivateVariableName(self.id, 'i')
        acc_var = NodeOutputVariableName(self.id, 'accumulator')
        cur_var = NodeOutputVariableName(self.id, 'current')
        return LanguageConcat(
            self.resolve_input_deploy('array'),
            VariableSetStatement(
                acc_var,
                ArrayIndex(
                    array_var,
                    LanguageValue(0)
                )
            ),
            VariableSetStatement(
                cur_var,
                LanguageNone()
            ),
            self.resolve_input_deploy_function('accumulator'),
            SimpleLoopStatement(
                i_var,
                LanguageValue(1),
                UtilsArrayLength(array_var),
                LanguageConcat(
                    VariableSetStatement(
                        cur_var,
                        ArrayIndex(array_var, i_var)
                    ),
                    VariableSetStatement(
                        acc_var,
                        FunctionCall(self.get_input_connection_function_name('accumulator'))
                    )
                )
            ),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'reduced'),
                acc_var
            )
        )

    def get_ioutput__accumulator(self, env):
        return self.state['current_accumulator']

    @staticmethod
    def deploy_ioutput__accumulator():
        return LanguageNoop()

    def get_ioutput__current(self, env):
        return self.state['current_value']

    @staticmethod
    def deploy_ioutput__current():
        return LanguageNoop()
