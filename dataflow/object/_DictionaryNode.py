from dataflow.base import BaseNode
from dataflow.gen import NodeOutputVariableName, VariableSetStatement, ArrayIndex, LanguageConcat, LanguageValue, \
    EmptyDictSymbol


class DictionaryNode(BaseNode):
    """
    Compacts a variable number of inputs into a single outputted key-value dictionary

    Inputs
    ------
    key_<n>: Key for element number n, starting at 0

    value_<n>: Value for element number n, starting at 0

    Outputs
    -------
    object: Resulting dictionary object
    """

    def __init__(self, property_count):
        super().__init__()

        self.property_count = property_count
        for i in range(self.property_count):
            self.declare_input('key_%d' % i)
            self.declare_input('value_%d' % i)

        self.declare_output('object', self.get_output__object, self.deploy_output__object)

    def get_output__object(self, env):
        out = {}
        for i in range(self.property_count):
            out[self.resolve_input('key_%d' % i, env)] = self.resolve_input('value_%d' % i, env)
        return out

    def deploy_output__object(self):
        object_var = NodeOutputVariableName(self.id, 'object')
        input_deploys = []
        input_sets = []
        for n in range(self.property_count):
            input_deploys.append(self.resolve_input_deploy('key_%d' % n))
            input_deploys.append(self.resolve_input_deploy('value_%d' % n))
            input_sets.append(
                VariableSetStatement(
                    ArrayIndex(
                        object_var,
                        self.get_input_connection_variable_name('key_%d' % n)
                    ),
                    self.get_input_connection_variable_name('value_%d' % n)
                )
            )
        return LanguageConcat(
            *input_deploys,
            VariableSetStatement(
                object_var,
                LanguageValue(EmptyDictSymbol())
            ),
            *input_sets
        )
