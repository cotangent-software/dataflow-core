from dataflow.base._BaseNode import BaseNode
from dataflow.base._DataSourceNode import DataSourceNode
from dataflow.gen import LanguageConcat, VariableSetStatement, NodeOutputVariableName


class ExtendedNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.extended_inputs = {}
        self.extended_outputs = {}

    def declare_extended_input(self, name, input_node: BaseNode, input_name: str):
        super().declare_input(name)
        source_node = DataSourceNode(None)
        BaseNode.connect(source_node, input_node, 'data', input_name)
        self.extended_inputs[name] = [input_node, input_name, source_node]

    def declare_extended_output(self, name, output_node: BaseNode, output_name: str):
        super().declare_output(name, None)
        self.extended_outputs[name] = [output_node, output_name]

    def resolve_output(self, name, environment=None):
        node_entry = self.extended_outputs[name]
        for input_name in self.extended_inputs:
            self.extended_inputs[input_name][2].data = self.resolve_input(input_name, environment)
        return node_entry[0].resolve_output(node_entry[1])

    def resolve_deploy(self, name):
        node_entry = self.extended_outputs[name]
        previous_deploys = []
        for input_name in self.extended_inputs:
            self.extended_inputs[input_name][2].data = self.get_input_connection_variable_name(input_name)
            previous_deploys.append(self.resolve_input_deploy(input_name))
        return LanguageConcat(
            *previous_deploys,
            node_entry[0].resolve_deploy(node_entry[1]),
            VariableSetStatement(
                NodeOutputVariableName(self.id, name),
                NodeOutputVariableName(node_entry[0].id, node_entry[1])
            )
        )
