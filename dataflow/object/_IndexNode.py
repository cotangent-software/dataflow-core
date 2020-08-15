from dataflow.base import BaseNode
from dataflow.gen import LanguageConcat, VariableSetStatement, NodeOutputVariableName, ArrayIndex


class IndexNode(BaseNode):
    """
    Dynamically accesses the index of input data

    Inputs
    ------
    data: The data which the index will be applied to

    index: The index to access from the input data

    Outputs
    -------
    value: Result of the indexed operation
    """

    def __init__(self, multiple=False):
        super().__init__()

        self.multiple = multiple

        self.declare_input('data')
        self.declare_input('index')
        self.declare_output('value', self.get_output__value, self.deploy_output__value)

    def get_output__value(self, env):
        data = self.resolve_input('data', env)
        idx = self.resolve_input('index', env)
        if self.multiple:
            idx_split = idx.split('.')
            current_val = data
            for current_idx in idx_split:
                if self.is_int_indexed(current_val):
                    current_val = current_val[current_idx]
                else:
                    current_val = getattr(current_val, current_idx)
            return current_val
        else:
            if self.is_int_indexed(data):
                return data[idx]
            else:
                return getattr(data, idx)

    def deploy_output__value(self):
        return LanguageConcat(
            self.resolve_input_deploy('data'),
            self.resolve_input_deploy('index'),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'value'),
                ArrayIndex(
                    self.get_input_connection_variable_name('data'),
                    self.get_input_connection_variable_name('index')
                )
            )
        )

    @staticmethod
    def is_int_indexed(obj):
        # return isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, dict)
        return hasattr(obj, '__getitem__')
