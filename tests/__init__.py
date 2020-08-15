from dataflow.base import BaseNode, DataSourceNode


def node_struct(node, input_values, input_names):
    for input_value, input_name in zip(input_values, input_names):
        BaseNode.connect(DataSourceNode(input_value), node, 'data', input_name)
    return node
