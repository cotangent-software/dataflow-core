from collections.abc import Iterable

from dataflow.base import BaseNode
from dataflow.gen import NodeOutputVariableName, VariableSetStatement, UtilsArrayConcat, LanguageConcat, LanguageValue,\
    EmptyArraySymbol


class ArrayNode(BaseNode):
    """
    Merges arrays or scalar values into an output array

    Inputs
        in_<n>: Arrays or scalars to be merged into the output array

    Outputs
        merged: The result of the array merging operation
    """

    def __init__(self, array_count):
        super().__init__()

        self.array_count = array_count

        for n in range(self.array_count):
            self.declare_input('in_%d' % n)
        self.declare_output('merged', self.get_output__merged, self.deploy_output__merged)

    def get_output__merged(self, env):
        out = []
        for n in range(self.array_count):
            val = self.resolve_input('in_%d' % n, env)
            if isinstance(val, Iterable):
                out.extend(val)
            else:
                out.append(val)
        return out

    def deploy_output__merged(self):
        merged_var = NodeOutputVariableName(self.id, 'merged')
        input_deploys = []
        input_concats = []
        for n in range(self.array_count):
            input_deploys.append(self.resolve_input_deploy('in_%d' % n))
            input_concats.append(
                VariableSetStatement(
                    merged_var,
                    UtilsArrayConcat(merged_var, self.get_input_connection_variable_name('in_%d' % n))
                )
            )
        return LanguageConcat(
            *input_deploys,
            VariableSetStatement(merged_var, LanguageValue(EmptyArraySymbol())),
            *input_concats
        )
