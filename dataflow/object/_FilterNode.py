from dataflow.base import BaseNode
from dataflow.gen import LanguageConcat, VariableSetStatement, LanguageNone, NodeOutputVariableName, LanguageOperation, \
    EmptyArraySymbol, LanguageValue, SimpleLoopStatement, UtilsArrayLength, NodePrivateVariableName, ArrayIndex, \
    UtilsArrayConcat, FunctionCall, IfStatement, LanguageNoop


class FilterNode(BaseNode):
    """
    Filters array elements, only keeping elements when the 'keep' input resolves to true

    Inputs
    ------
    array: The array to filter from

    keep (internal): A boolean value determining if the current array element should be kept

    Outputs
    -------
    filtered: New array only containing the unfiltered values in 'array'

    entry (internal): Current entry in the filter operation

    index (internal): Current entry's index in the filter operation
    """

    def __init__(self):
        super().__init__()

        self.declare_input('array')
        self.declare_input('keep', internal=True)
        self.declare_output('filtered', self.get_output__filtered, self.deploy_output__filtered)
        self.declare_output('entry', self.get_ioutput__entry, self.deploy_ioutput__entry, internal=True)
        self.declare_output('index', self.get_ioutput__index, self.deploy_ioutput__index, internal=True)

    def get_output__filtered(self, env):
        arr = self.resolve_input('array', env)
        out_arr = []
        for i in range(len(arr)):
            self.state['current_index'] = i
            self.state['current_entry'] = arr[i]
            if self.resolve_input('keep', env):
                out_arr.append(arr[i])
        return out_arr

    def deploy_output__filtered(self):
        filtered_var = NodeOutputVariableName(self.id, 'filtered')
        entry_var = NodeOutputVariableName(self.id, 'entry')
        index_var = NodeOutputVariableName(self.id, 'index')
        array_var = self.get_input_connection_variable_name('array')
        i_var = NodePrivateVariableName(self.id, 'i')
        return LanguageConcat(
            self.resolve_input_deploy('array'),
            VariableSetStatement(
                entry_var,
                LanguageNone()
            ),
            VariableSetStatement(
                index_var,
                LanguageNone()
            ),
            self.resolve_input_deploy_function('keep'),
            VariableSetStatement(
                filtered_var,
                LanguageValue(EmptyArraySymbol())
            ),
            SimpleLoopStatement(
                i_var,
                LanguageValue(0),
                LanguageValue(UtilsArrayLength(array_var)),
                LanguageConcat(
                    VariableSetStatement(index_var, i_var),
                    VariableSetStatement(entry_var, ArrayIndex(array_var, i_var)),
                    IfStatement(
                        FunctionCall(self.get_input_connection_function_name('keep')),
                        VariableSetStatement(
                            filtered_var,
                            UtilsArrayConcat(
                                filtered_var,
                                entry_var
                            )
                        )
                    )
                )
            )
        )

    def get_ioutput__entry(self, env):
        return self.state['current_entry']

    def deploy_ioutput__entry(self):
        return LanguageNoop()

    def get_ioutput__index(self, env):
        return self.state['current_index']

    def deploy_ioutput__index(self):
        return LanguageNoop()
