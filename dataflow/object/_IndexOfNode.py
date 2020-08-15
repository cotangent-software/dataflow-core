from dataflow.base import BaseNode
from dataflow.gen import LanguageConcat, VariableSetStatement, NodeOutputVariableName, UtilsArrayIndexOf


class IndexOfNode(BaseNode):
    """
    Searches for a value based on equality in a given array

    Inputs
    ------
    array: The array to search through

    search: Value to search for in target array

    Outputs
    -------
    index: The index of the search element in target array. If not found, it is equal to -1
    """

    def __init__(self):
        super().__init__()

        self.declare_input('array')
        self.declare_input('search')
        self.declare_output('index', self.get_output__index, self.deploy_output__index)

    def get_output__index(self, env):
        arr = self.resolve_input('array', env)
        search = self.resolve_input('search', env)
        for i in range(len(arr)):
            if arr[i] == search:
                return i
        return -1

    def deploy_output__index(self):
        return LanguageConcat(
            self.resolve_input_deploy('array'),
            self.resolve_input_deploy('search'),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'index'),
                UtilsArrayIndexOf(
                    self.get_input_connection_variable_name('array'),
                    self.get_input_connection_variable_name('search'),
                )
            )
        )
