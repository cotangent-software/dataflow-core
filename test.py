from graph import *

pass_through = PassThroughNode()
data_node = DataSourceNode(['test'])

BaseNode.connect(Connection(data_node, pass_through, 'data', 'in'))

print('Resolved value:', pass_through.resolve_output('out'))

print('Webserver test:')

config_node = WebConfigNode(8080)
endpoint_node = WebEndpointNode('/', config_node)
index_args_node = ReadIndexNode()
index_test_node = ReadIndexNode()

BaseNode.connect(Connection(index_test_node, endpoint_node, 'value', 'data'))

BaseNode.connect(Connection(DataSourceNode('args'), index_args_node, 'data', 'index'))
BaseNode.connect(Connection(ReadEnvironmentNode(), index_args_node, 'value', 'data'))

BaseNode.connect(Connection(DataSourceNode('test'), index_test_node, 'data', 'index'))
BaseNode.connect(Connection(index_args_node, index_test_node, 'value', 'data'))
