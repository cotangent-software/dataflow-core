from dataflow.base import BaseNode
from dataflow.gen import LanguageNoop, LanguageConcat, VariableSetStatement, NodeOutputVariableName, LanguageNone, \
    SimpleLoopStatement, LanguageValue, UtilsArrayLength, NodePrivateVariableName, ArrayIndex, FunctionCall, IfStatement


class FindNode(BaseNode):
    """
    Finds and outputs an array element based on an internal condition loop

    Inputs
        array: The array to search through

        matches (internal): Boolean value, true if the entry is found and false if not

    Outputs
        match: Matched value from the inputted array

        entry (internal): Current array entry to check for a match on

        index (internal): Current array entry index to check for a match on
    """

    def __init__(self):
        super().__init__()

        self.declare_input('array')
        self.declare_input('matches', internal=True)
        self.declare_output('match', self.get_output__match, self.deploy_output__match)
        self.declare_output('entry', self.get_output__entry, self.deploy_output__entry, internal=True)
        self.declare_output('index', self.get_output__index, self.deploy_output__index, internal=True)

    def get_output__match(self, env):
        arr = self.resolve_input('array', env)
        for i in range(len(arr)):
            self.state['current_index'] = i
            self.state['current_entry'] = arr[i]
            if self.resolve_input('matches'):
                return arr[i]
        return None

    def deploy_output__match(self):
        array_var = self.get_input_connection_variable_name('array')
        entry_var = NodeOutputVariableName(self.id, 'entry')
        index_var = NodeOutputVariableName(self.id, 'index')
        match_var = NodeOutputVariableName(self.id, 'match')
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
            self.resolve_input_deploy_function('matches'),
            VariableSetStatement(
                match_var,
                LanguageNone()
            ),
            SimpleLoopStatement(
                i_var,
                LanguageValue(0),
                UtilsArrayLength(array_var),
                LanguageConcat(
                    VariableSetStatement(index_var, i_var),
                    VariableSetStatement(entry_var, ArrayIndex(array_var, i_var)),
                    IfStatement(
                        FunctionCall(self.get_input_connection_function_name('matches')),
                        VariableSetStatement(match_var, entry_var)
                    )
                )
            )
        )

    def get_output__entry(self, env):
        return self.state['current_entry']

    @staticmethod
    def deploy_output__entry():
        return LanguageNoop()

    def get_output__index(self, env):
        return self.state['current_index']

    @staticmethod
    def deploy_output__index():
        return LanguageNoop()
