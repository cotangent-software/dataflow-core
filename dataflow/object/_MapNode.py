from dataflow.base import BaseNode
from dataflow.gen import NodePrivateVariableName, NodeOutputVariableName, LanguageConcat, VariableSetStatement, \
    LanguageNone, UtilsArrayClone, SimpleLoopStatement, LanguageValue, UtilsArrayLength, ArrayIndex, FunctionCall, \
    LanguageNoop


class MapNode(BaseNode):
    """
    Maps an input array to an output array of equal length with each element transformed based on an internal graph

    Inputs
    ------
    array: Input array to be transformed

    value (internal): Result of an elementwise transformation

    Outputs
    -------
    mapped: Output array which has been mapped by a transformation

    entry (internal): Element of the input array to be transformed

    index (internal): Index of the element to be transformed
    """

    def __init__(self):
        super().__init__()

        self.declare_input('array')
        self.declare_input('value', internal=True)
        self.declare_output('mapped', self.get_output__mapped, self.deploy_output__mapped)
        self.declare_output('entry', self.get_ioutput__entry, self.deploy_ioutput__entry, internal=True)
        self.declare_output('index', self.get_ioutput__index, self.deploy_ioutput__index, internal=True)

    def get_output__mapped(self, env):
        arr = self.resolve_input('array', env)
        out_arr = []
        for i in range(len(arr)):
            self.state['current_index'] = i
            self.state['current_entry'] = arr[i]
            out_arr.append(self.resolve_input('value', env))
        return out_arr

    def deploy_output__mapped(self):
        i_var = NodePrivateVariableName(self.id, 'i')
        entry_var = NodeOutputVariableName(self.id, 'entry')
        index_var = NodeOutputVariableName(self.id, 'index')
        mapped_var = NodeOutputVariableName(self.id, 'mapped')
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
            self.resolve_input_deploy_function('value'),
            VariableSetStatement(
                mapped_var,
                UtilsArrayClone(self.get_input_connection_variable_name('array'))
            ),
            SimpleLoopStatement(
                i_var,
                LanguageValue(0),
                UtilsArrayLength(self.get_input_connection_variable_name('array')),
                LanguageConcat(
                    VariableSetStatement(index_var, i_var),
                    VariableSetStatement(
                        entry_var,
                        ArrayIndex(
                            self.get_input_connection_variable_name('array'),
                            i_var
                        )
                    ),
                    VariableSetStatement(
                        ArrayIndex(mapped_var, i_var),
                        FunctionCall(
                            self.get_input_connection_function_name('value')
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
