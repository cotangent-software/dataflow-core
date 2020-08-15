from dataflow.base import BaseNode
from dataflow.gen import LanguageConcat, VariableSetStatement, NodeOutputVariableName, UtilsArraySlice


class SliceNode(BaseNode):
    """
    Slices an array according to python slice rules

    Inputs
    ------
    array: Array which should be sliced

    slice_start: Starting index of array slice

    slice_end: Ending index of array slice

    slice_step: Step size for slice operation

    Outputs
    -------
    array: Sliced version of input array
    """

    def __init__(self):
        super().__init__()

        self.declare_input('array')
        self.declare_input('slice_start')
        self.declare_input('slice_end')
        self.declare_input('slice_step')
        self.declare_output('array', self.get_output__array, self.deploy_output__array)

    def get_output__array(self, env):
        slice_obj = slice(
            self.resolve_input('slice_start', env, allow_unconnected=True),
            self.resolve_input('slice_end', env, allow_unconnected=True),
            self.resolve_input('slice_step', env, allow_unconnected=True)
        )
        return self.resolve_input('array', env)[slice_obj]

    def deploy_output__array(self):
        return LanguageConcat(
            self.resolve_input_deploy('array'),
            self.resolve_input_deploy('slice_start', allow_unconnected=True),
            self.resolve_input_deploy('slice_end', allow_unconnected=True),
            self.resolve_input_deploy('slice_step', allow_unconnected=True),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'array'),
                UtilsArraySlice(
                    self.get_input_connection_variable_name('array'),
                    self.get_input_connection_variable_name('slice_start', allow_unconnected=True),
                    self.get_input_connection_variable_name('slice_end', allow_unconnected=True),
                    self.get_input_connection_variable_name('slice_step', allow_unconnected=True),
                )
            )
        )
