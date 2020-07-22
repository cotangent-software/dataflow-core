from dataflow.base import *
from dataflow.db import SQLiteQueryNode, SQLiteDatabaseNode
from dataflow.web import WebServerNode, WebEndpointNode


def basic_test():
    pass_through = PassThroughNode()
    data_node = DataSourceNode(['test'])

    BaseNode.connect(Connection(data_node, pass_through, 'data', 'in'))

    print('Resolved value:', pass_through.resolve_output('out'))


def type_test():
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


def loops_test():
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


def sqlite_test():
    create_test_table = """
    CREATE TABLE IF NOT EXISTS test (
        id integer PRIMARY KEY,
        name text NOT NULL,
        count integer NOT NULL,
        optional text
    );
    """

    print('SQLite test:')
    db_node = SQLiteDatabaseNode(':memory:')
    query_node = SQLiteQueryNode(create_test_table)
    BaseNode.connect(Connection(db_node, query_node, 'conn', 'conn'))
    BaseNode.connect(Connection(DataSourceNode([]), query_node, 'data', 'variables'))

    print(query_node.resolve_output('meta'))

    query_node = SQLiteQueryNode('INSERT INTO test(name, count, optional) VALUES(?, ?, ?)')
    BaseNode.connect(Connection(db_node, query_node, 'conn', 'conn'))
    BaseNode.connect(
        Connection(
            DataSourceNode(['Random Name', 4, 'This is some extra random text']), query_node, 'data', 'variables'))

    print(query_node.resolve_output('meta'))

    query_node = SQLiteQueryNode('SELECT * FROM test')
    BaseNode.connect(Connection(db_node, query_node, 'conn', 'conn'))
    BaseNode.connect(Connection(DataSourceNode([]), query_node, 'data', 'variables'))

    print(query_node.resolve_output('data'))
    print(query_node.resolve_output('meta'))


sqlite_test()
