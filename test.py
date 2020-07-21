from graph.base import *
from graph.web import WebServerNode, WebEndpointNode

pass_through = PassThroughNode()
data_node = DataSourceNode(['test'])

BaseNode.connect(Connection(data_node, pass_through, 'data', 'in'))

print('Resolved value:', pass_through.resolve_output('out'))

print('Type test:')

# config_node = WebServerNode(8080)
# endpoint_node = WebEndpointNode('/factorial', config_node)
index_args_node = ReadIndexNode()
index_n_node = ReadIndexNode()
parse_n_node = ParseIntNode()
type_n_node = TypeNode()
output_node = PassThroughNode()

BaseNode.connect(Connection(type_n_node, output_node, 'out', 'in'))
BaseNode.connect(Connection(parse_n_node, type_n_node, 'out', 'in'))
BaseNode.connect(Connection(index_n_node, parse_n_node, 'value', 'in'))

BaseNode.connect(Connection(DataSourceNode('args'), index_args_node, 'data', 'index'))
BaseNode.connect(Connection(ReadEnvironmentNode(), index_args_node, 'value', 'data'))

BaseNode.connect(Connection(DataSourceNode('n'), index_n_node, 'data', 'index'))
BaseNode.connect(Connection(index_args_node, index_n_node, 'value', 'data'))


print(output_node.resolve_output('out', {
    'args': {
        'n': '15'
    }
}))


print()
print('Loops test:')

output_node = PassThroughNode()
loop_node = LoopNode()
BaseNode.connect(Connection(loop_node, output_node, 'value', 'in'))
invert_node = NotNode()
BaseNode.connect(Connection(invert_node, loop_node, 'out', 'iter'))
check_node = EqualsNode()
BaseNode.connect(Connection(check_node, invert_node, 'equal', 'in'))
BaseNode.connect(Connection(DataSourceNode(15), check_node, 'data', 'arg1'))
dummy_node = DummyNode()
BaseNode.connect(Connection(dummy_node, check_node, 'out', 'arg2'))
increment_node = IncrementNode()
BaseNode.connect(Connection(increment_node, dummy_node, 'increment', 'in'))
result_node = VariableNode(1)
BaseNode.connect(Connection(result_node, dummy_node, 'update', 'extra'))
BaseNode.connect(Connection(result_node, loop_node, 'value', 'value'))
add_node = MultiplyNode()
BaseNode.connect(Connection(add_node, result_node, 'result', 'value'))
BaseNode.connect(Connection(increment_node, add_node, 'value', 'arg1'))
BaseNode.connect(Connection(result_node, add_node, 'value', 'arg2'))


print(output_node.resolve_output('out'))
print(result_node.state)
