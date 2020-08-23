from dataflow.base import *
from dataflow.bool import NotNode, EqualsNode
from dataflow.db import SQLiteDatabaseAdapter, DatabaseConnectionNode, DatabaseObjectNode, DatabaseObjectFieldNode, \
    DatabaseQuery, DatabaseCondition, DatabaseQueryNode, DatabaseConditionNode
from dataflow.flow import PassThroughNode, LoopNode, DummyNode
from dataflow.gen import LanguageConcat, deploy, FunctionCall, VariableName, DeployContext
from dataflow.math import AddNode, MultiplyNode, SubtractNode, DivideNode, AbsoluteValueNode, PowerNode, RootNode, \
    LogNode, PiConstantNode, EulerConstantNode, CeilNode, FloorNode, RoundNode, ModulusNode
from dataflow.object import IndexNode, FilterNode, ReduceNode
from dataflow.state import IncrementNode, VariableNode
from dataflow.type import ParseIntNode, TypeNode
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
    BaseNode.connect(eq_node, not_node, 'result', 'in')
    BaseNode.connect(iter_node, eq_node, 'increment', 'arg1')
    BaseNode.connect(DataSourceNode(50), eq_node, 'data', 'arg2')
    BaseNode.connect(var_node, loop_node, 'value', 'value')

    BaseNode.connect(var_node, split_node, 'update', 'extra')
    BaseNode.connect(add_node, var_node, 'result', 'value')
    BaseNode.connect(iter_node, add_node, 'value', 'arg1')
    BaseNode.connect(var_node, add_node, 'value', 'arg2')

    code = LanguageConcat(
        deploy(out_node, 'out'),
        FunctionCall(VariableName('main'))
    )
    print(code.__py__(DeployContext()))
    # with open('deploy.min.js', 'w') as fh:
    #     fh.write(code.__es6__(DeployContext()))
    # print(out_node.resolve_output('out'))


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
    print(deploy(out_node, 'out', include_utils=False).__py__(DeployContext()))


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


def not_equals_test():
    out_node = PassThroughNode()
    from dataflow.bool._NotEqualsNode import NotEqualsNode
    not_equals_node = NotEqualsNode()
    BaseNode.connect(not_equals_node, out_node, 'result', 'in')
    BaseNode.connect(DataSourceNode(5.5), not_equals_node, 'data', 'arg1')
    BaseNode.connect(DataSourceNode(5.49), not_equals_node, 'data', 'arg2')

    print(out_node.resolve_output('out'))
    print(deploy(out_node, 'out', include_utils=False).__es6__(DeployContext()))


def filter_node_test():
    filter_node = FilterNode()
    BaseNode.connect(DataSourceNode([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), filter_node, 'data', 'array')
    mod_node = ModulusNode()
    eq_node = EqualsNode()
    BaseNode.connect(filter_node, mod_node, 'entry', 'arg1')
    BaseNode.connect(DataSourceNode(2), mod_node, 'data', 'arg2')
    BaseNode.connect(mod_node, eq_node, 'result', 'arg1')
    BaseNode.connect(DataSourceNode(0), eq_node, 'data', 'arg2')
    BaseNode.connect(eq_node, filter_node, 'result', 'keep')
    print(filter_node.resolve_output('filtered'))
    print(deploy(filter_node, 'filtered').__py__(DeployContext()))


def reduce_node_test():
    reduce_node = ReduceNode()
    BaseNode.connect(DataSourceNode([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), reduce_node, 'data', 'array')
    add_node = AddNode()
    BaseNode.connect(reduce_node, add_node, 'accumulator', 'arg1')
    BaseNode.connect(reduce_node, add_node, 'current', 'arg2')
    BaseNode.connect(add_node, reduce_node, 'result', 'accumulator')
    print(deploy(reduce_node, 'reduced').__py__(DeployContext()))


def database_test():
    adapter = SQLiteDatabaseAdapter('test.db')
    conn_node = DatabaseConnectionNode(adapter)
    obj_node = DatabaseObjectNode(2)
    name_field = DatabaseObjectFieldNode()
    age_field = DatabaseObjectFieldNode()
    BaseNode.connect(DataSourceNode('person'), obj_node, 'data', 'name')

    BaseNode.connect(DataSourceNode('name'), name_field, 'data', 'name')
    BaseNode.connect(DataSourceNode('string'), name_field, 'data', 'type')
    BaseNode.connect(DataSourceNode(True), name_field, 'data', 'required')
    BaseNode.connect(DataSourceNode('age'), age_field, 'data', 'name')
    BaseNode.connect(DataSourceNode('int'), age_field, 'data', 'type')

    BaseNode.connect(name_field, obj_node, 'field', 'field_0')
    BaseNode.connect(age_field, obj_node, 'field', 'field_1')

    object_schema = obj_node.resolve_output('db_object')
    adapter.define_object(object_schema)

    print(adapter.query(DatabaseQuery(
        object_schema,
        [
            DatabaseCondition(age_field.resolve_output('field'), 13, '>')
        ]
    )))
    query_node = DatabaseQueryNode(1)
    BaseNode.connect(obj_node, query_node, 'db_object', 'object')
    BaseNode.connect(DatabaseConnectionNode(adapter), query_node, 'data', 'db')
    cond_node = DatabaseConditionNode('<')
    BaseNode.connect(age_field, cond_node, 'field', 'field')
    BaseNode.connect(DataSourceNode(20.), cond_node, 'data', 'compare')
    BaseNode.connect(cond_node, query_node, 'condition', 'condition_0')
    print(query_node.resolve_output('rows'))


database_test()
