import uuid

from dataflow.base._BaseNode import BaseNode


class Connection:
    def __init__(self, output_node: BaseNode, input_node: BaseNode, output_name, input_name):
        self.id = uuid.uuid4().hex
        self.output = output_node
        self.input = input_node
        self.output_name = output_name
        self.input_name = input_name

    def __eq__(self, other):
        return self.output == other.output and \
               self.input == other.input and \
               self.output_name == other.output_name and \
               self.input_name == other.input_name

    def to_object(self):
        return {
            'id': self.id,
            'output_node': self.output.id,
            'input_node': self.input.id,
            'output_name': self.output_name,
            'input_name': self.input_name
        }
