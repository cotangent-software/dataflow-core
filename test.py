from dataflow.base import *
from dataflow.db import SQLiteQueryNode, SQLiteDatabaseNode
from dataflow.math import AddNode, MultiplyNode, SubtractNode, DivideNode, AbsoluteValueNode, PowerNode, RootNode, \
    LogNode, PiConstantNode, EulerConstantNode, CeilNode, FloorNode, RoundNode, ModulusNode
from dataflow.web import WebServerNode, WebEndpointNode


def basic_test():
    pass_through = PassThroughNode()
    data_node = DataSourceNode(['test'])

    BaseNode.connect(data_node, pass_through, 'data', 'in')

    print('Resolved value:', pass_through.resolve_output('out'))


def type_test():
    print('Type test:')
    # config_node = WebServerNode(8080)
    # endpoint_node = WebEndpointNode('/factorial', config_node)
    index_args_node = IndexNode()
    index_n_node = IndexNode()
    parse_n_node = ParseIntNode()
    type_n_node = TypeNode()
    output_node = PassThroughNode()

    BaseNode.connect(type_n_node, output_node, 'out', 'in')
    BaseNode.connect(parse_n_node, type_n_node, 'out', 'in')
    BaseNode.connect(index_n_node, parse_n_node, 'value', 'in')

    BaseNode.connect(DataSourceNode('args'), index_args_node, 'data', 'index')
    BaseNode.connect(ReadEnvironmentNode(), index_args_node, 'value', 'data')

    BaseNode.connect(DataSourceNode('n'), index_n_node, 'data', 'index')
    BaseNode.connect(index_args_node, index_n_node, 'value', 'data')

    print(output_node.resolve_output('out', {
        'args': {
            'n': '15'
        }
    }))


def loops_test():
    print('Loops test:')

    output_node = PassThroughNode()
    loop_node = LoopNode()
    BaseNode.connect(loop_node, output_node, 'value', 'in')
    invert_node = NotNode()
    BaseNode.connect(invert_node, loop_node, 'out', 'iter')
    check_node = EqualsNode()
    BaseNode.connect(check_node, invert_node, 'equal', 'in')
    BaseNode.connect(DataSourceNode(15), check_node, 'data', 'arg1')
    dummy_node = DummyNode()
    BaseNode.connect(dummy_node, check_node, 'out', 'arg2')
    increment_node = IncrementNode()
    BaseNode.connect(increment_node, dummy_node, 'increment', 'in')
    result_node = VariableNode(1)
    BaseNode.connect(result_node, dummy_node, 'update', 'extra')
    BaseNode.connect(result_node, loop_node, 'value', 'value')
    add_node = MultiplyNode()
    BaseNode.connect(add_node, result_node, 'result', 'value')
    BaseNode.connect(increment_node, add_node, 'value', 'arg1')
    BaseNode.connect(result_node, add_node, 'value', 'arg2')

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
    BaseNode.connect(db_node, query_node, 'conn', 'conn')
    BaseNode.connect(DataSourceNode([]), query_node, 'data', 'variables')

    print(query_node.resolve_output('meta'))

    query_node = SQLiteQueryNode('INSERT INTO test(name, count, optional) VALUES(?, ?, ?)')
    BaseNode.connect(db_node, query_node, 'conn', 'conn')
    BaseNode.connect(DataSourceNode(['Random Name', 4, 'This is some extra random text']), query_node, 'data', 'variables')

    print(query_node.resolve_output('meta'))

    query_node = SQLiteQueryNode('SELECT * FROM test')
    BaseNode.connect(db_node, query_node, 'conn', 'conn')
    BaseNode.connect(DataSourceNode([]), query_node, 'data', 'variables')

    print(query_node.resolve_output('data'))
    print(query_node.resolve_output('meta'))


def deploy_test():
    loop_node = LoopNode()
    iter_node = IncrementNode()
    eq_node = EqualsNode()
    not_node = NotNode()
    var_node = VariableNode(0)
    split_node = DummyNode()
    add_node = AddNode()
    out_node = PassThroughNode()
    BaseNode.connect(loop_node, out_node, 'value', 'in')
    BaseNode.connect(split_node, loop_node, 'out', 'iter')
    BaseNode.connect(not_node, split_node, 'out', 'in')
    BaseNode.connect(eq_node, not_node, 'equal', 'in')
    BaseNode.connect(iter_node, eq_node, 'increment', 'arg1')
    BaseNode.connect(DataSourceNode(50000), eq_node, 'data', 'arg2')
    BaseNode.connect(var_node, loop_node, 'value', 'value')

    BaseNode.connect(var_node, split_node, 'update', 'extra')
    BaseNode.connect(add_node, var_node, 'result', 'value')
    BaseNode.connect(iter_node, add_node, 'value', 'arg1')
    BaseNode.connect(var_node, add_node, 'value', 'arg2')

    code = LanguageConcat(
        deploy(out_node, 'out'),
        FunctionCall(VariableName('main'))
    )
    print(code.__es6__(DeployContext()))
    with open('deploy.min.js', 'w') as fh:
        fh.write(code.__es6__(DeployContext()))
    print(out_node.resolve_output('out'))


def math_op_deploy_test():
    out_node = PassThroughNode()
    add_node = AddNode()
    subtract_node = SubtractNode()
    multiply_node = MultiplyNode()
    divide_node = DivideNode()
    abs_node = AbsoluteValueNode()
    power_node = PowerNode()
    root_node = RootNode()
    log_node = LogNode()
    modulus_node = ModulusNode()

    BaseNode.connect(DataSourceNode(1), add_node, 'data', 'arg1')
    BaseNode.connect(DataSourceNode(4), add_node, 'data', 'arg2')
    BaseNode.connect(add_node, subtract_node, 'result', 'arg1')
    BaseNode.connect(DataSourceNode(1), subtract_node, 'data', 'arg2')
    BaseNode.connect(subtract_node, multiply_node, 'result', 'arg1')
    BaseNode.connect(DataSourceNode(4), multiply_node, 'data', 'arg2')
    BaseNode.connect(multiply_node, divide_node, 'result', 'arg1')
    BaseNode.connect(DataSourceNode(-2), divide_node, 'data', 'arg2')
    BaseNode.connect(divide_node, abs_node, 'result', 'in')
    BaseNode.connect(DataSourceNode(2), power_node, 'data', 'base')
    BaseNode.connect(abs_node, power_node, 'result', 'power')
    BaseNode.connect(DataSourceNode(2), root_node, 'data', 'root')
    BaseNode.connect(power_node, root_node, 'result', 'value')
    BaseNode.connect(DataSourceNode(2), log_node, 'data', 'base')
    BaseNode.connect(root_node, log_node, 'result', 'value')
    BaseNode.connect(log_node, modulus_node, 'result', 'arg1')
    BaseNode.connect(DataSourceNode(3), modulus_node, 'data', 'arg2')
    BaseNode.connect(modulus_node, out_node, 'result', 'in')

    print(out_node.resolve_output('out'))
    print(deploy(out_node, 'out', include_utils=False).__es6__(DeployContext()))


def math_const_deploy_test():
    out_node = PassThroughNode()
    d1_node = DummyNode()
    print_node = PrintNode()
    BaseNode.connect(d1_node, out_node, 'out', 'in')
    BaseNode.connect(PiConstantNode(), d1_node, 'value', 'in')
    BaseNode.connect(print_node, d1_node, 'out', 'extra')
    BaseNode.connect(EulerConstantNode(), print_node, 'value', 'in')

    print(out_node.resolve_output('out'))
    print(deploy(out_node, 'out', include_utils=False).__es6__(DeployContext()))


def math_round_deploy_test():
    out_node = PassThroughNode()
    round_node = RoundNode()
    BaseNode.connect(round_node, out_node, 'result', 'in')
    BaseNode.connect(DataSourceNode(5.49), round_node, 'data', 'value')

    print(out_node.resolve_output('out'))
    print(deploy(out_node, 'out', include_utils=False).__es6__(DeployContext()))


math_op_deploy_test()
