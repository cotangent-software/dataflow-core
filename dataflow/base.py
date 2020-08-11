import uuid
from collections.abc import Iterable
from enum import Enum

from dataflow.gen import *

Types = Enum('Types', 'STRING INT FLOAT ARRAY MIXED')


def array_find(arr, fun):
    for i in arr:
        if fun(i):
            return i
    return None


class GraphError(Exception):
    pass


class Connection:
    def __init__(self, output_node: 'BaseNode', input_node: 'BaseNode', output_name, input_name):
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


class BaseNode:
    """
    Base class which every node must extend

    Inputs
    ------
    None

    Outputs
    -------
    None
    """
    NodeRegistry = []

    def __init__(self):
        self.id = uuid.uuid4().hex
        self.connections = []
        self.declared_inputs = []
        self.input_internal = {}
        self.declared_outputs = []
        self.output_handlers = {}
        self.output_internal = {}
        self.output_cache = {}
        self.deploy_handlers = {}
        self.state = {}

    def declare_input(self, name, internal=False):
        self.declared_inputs.append(name)
        self.input_internal[name] = internal

    def declare_output(self, name, handler, deploy_handler=None, internal=False):
        self.declared_outputs.append(name)
        self.output_handlers[name] = handler
        self.output_internal[name] = internal
        if deploy_handler is not None:
            self.deploy_handlers[name] = deploy_handler

    def get_input_connection(self, input_name) -> Connection:
        conn = array_find(self.connections, lambda x: x.input_name == input_name and x.input == self)
        if conn is not None:
            return conn
        else:
            raise GraphError('Could not find input connection with name \'%s\'' % input_name)

    def resolve_input(self, name, environment=None, allow_unconnected=False):
        if environment is None:
            environment = {}
        conn = array_find(self.connections, lambda x: x.input_name == name and x.input == self)
        if conn is not None:
            return conn.output.resolve_output(conn.output_name, environment)
        else:
            if allow_unconnected:
                return None
            else:
                raise GraphError('Unconnected input \'%s\' is depended upon' % name)

    def resolve_output(self, name, environment=None):
        print(self)
        if environment is None:
            environment = {}
        return self.output_handlers[name](environment)

    def resolve_deploy(self, name):
        return self.deploy_handlers[name]()

    def cache_output(self, name, value):
        self.output_cache[name] = value

    def clear_cache(self, name=None):
        if name is None:
            self.output_cache = {}
        else:
            del self.output_cache[name]

    def reset_state(self):
        self.state = {}

    def remove_connection(self, conn):
        self.connections.remove(conn)

    def to_object(self, state=True, io=True):
        inputs = []
        outputs = []
        if io:
            for declared_input in self.declared_inputs:
                inputs.append({
                    'name': declared_input,
                    'internal': self.input_internal[declared_input]
                })
            for declared_output in self.declared_outputs:
                outputs.append({
                    'name': declared_output,
                    'internal': self.output_internal[declared_output]
                })
        out = {
            'id': self.id,
            'type': BaseNode.NodeRegistry.index(self.__class__)
        }
        if io:
            out['inputs'] = inputs
            out['outputs'] = outputs
        if state:
            out['state'] = self.state
            out['output_cache'] = self.output_cache
        return out

    @staticmethod
    def connect(output_node: 'BaseNode', input_node: 'BaseNode', output_name, input_name):
        connection = Connection(output_node, input_node, output_name, input_name)
        if connection in connection.input.connections:
            raise GraphError('Connection already contained in input node')
        if connection in connection.output.connections:
            raise GraphError('Connection already contained in output node')
        if connection.input_name not in connection.input.declared_inputs:
            raise GraphError('Input connection contains no \'%s\' input' % connection.input_name)
        if connection.output_name not in connection.output.declared_outputs:
            raise GraphError('Output connection contains no \'%s\' output' % connection.output_name)
        connection.input.connections.append(connection)
        connection.output.connections.append(connection)

        return connection

    @staticmethod
    def disconnect(connection):
        connection.output.remove_connection(connection)
        connection.input.remove_connection(connection)


class DataSourceNode(BaseNode):
    """
    Acts as an output-only node which sends a predetermined constant output

    Inputs
    ------
    None

    Outputs
    -------
    data: Predetermined constant output
    """

    def __init__(self, data):
        super().__init__()

        self.data = data

        self.declare_output('data', self.get_output__data, self.deploy_output__data)

    def get_output__data(self, env):
        return self.data

    def deploy_output__data(self):
        return VariableStatement(NodeOutputVariableName(self.id, 'data'), LanguageValue(self.data))


class PassThroughNode(BaseNode):
    """
    Passes data with no variation across a single input and output

    Inputs
    ------
    in: Source of the data to be passed

    Outputs
    -------
    out: Place to pass the input data
    """

    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_output('out', self.get_output__out, self.deploy_output__out)

    def get_output__out(self, env):
        return self.resolve_input('in', env)

    def deploy_output__out(self):
        conn = self.get_input_connection('in')
        return LanguageConcat(
            conn.output.resolve_deploy(conn.output_name),
            VariableStatement(NodeOutputVariableName(self.id, 'out'),
                              NodeOutputVariableName(conn.output.id, conn.output_name))
        )


class PrintNode(BaseNode):
    """
    Acts as a PassThroughNode, but prints the value which is passed through

    Inputs
    ------
    in: Source of the data to be passed

    Outputs
    -------
    out: Place to pass the input data
    """

    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_output('out', self.get_output__out)

    def get_output__out(self, env):
        val = self.resolve_input('in')
        print(val)
        return val


class ParseIntNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_output('out', self.get_output__out)

    def get_output__out(self, env):
        return int(self.resolve_input('in', env))


class ParseFloatNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_output('out', self.get_output__out)

    def get_output__out(self, env):
        return float(self.resolve_input('in', env))


class TypeNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_output('out', self.get_output__out)

    def get_output__out(self, env):
        return self.resolve_input('in', env).__class__.__name__


class SwitchNode(BaseNode):
    """
    Depending on an input value, choose which path to return on the basis of the value's equality with a test

    Inputs
    ------
    value: Value which will be tested for equality

    default: Returned path given that no equality test is satisfied

    test_<n>: Value which equality should be tested for

    return_<n>: Associated return path given that test_<n> is satisfied

    Outputs
    -------
    selected: Outputted value of the selected return path
    """

    def __init__(self, condition_count):
        super().__init__()

        self.condition_count = condition_count

        self.declare_input('value')
        self.declare_input('default')
        for n in range(self.condition_count):
            self.declare_input('test_%d' % n)
            self.declare_input('return_%d' % n)
        self.declare_output('selected', self.get_output__selected)

    def get_output__selected(self, env):
        value = self.resolve_input('value', env)
        for n in range(self.condition_count):
            if self.resolve_input('test_%d' % n, env) == value:
                return self.resolve_input('return_%d' % n, env)
        default_value = self.resolve_input('default', env, allow_unconnected=True)
        return default_value


class VariableNode(BaseNode):
    """
    Stores a given value so long as the state is preserved

    Inputs
    ------
    value: New value for the variable if update is triggered

    Outputs
    -------
    value: Nondestructive current value of the variable

    update: Triggers a variable update and passes the updated variable through this output
    """

    def __init__(self, init_value=0):
        super().__init__()

        self.init_value = init_value
        self.state['value'] = self.init_value

        self.declare_input('value')
        self.declare_output('update', self.get_output__update)
        self.declare_output('value', self.get_output__value)

    def get_output__update(self, env):
        next_value = self.resolve_input('value', env)
        if next_value is not None:
            self.state['value'] = next_value
        return self.get_output__value(env)

    def get_output__value(self, env):
        print(self.state['value'])
        return self.state['value']

    def reset_state(self):
        super().reset_state()
        self.state['value'] = self.init_value


class IncrementNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.state['value'] = 0

        self.declare_output('increment', self.get_output__increment)
        self.declare_output('value', self.get_output__value)

    def get_output__increment(self, env):
        self.state['value'] += 1
        return self.state['value']

    def get_output__value(self, env):
        return self.state['value']


class EqualsNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('arg1')
        self.declare_input('arg2')
        self.declare_output('equal', self.get_output__equal)

    def get_output__equal(self, env):
        return self.resolve_input('arg1', env) == self.resolve_input('arg2', env)


class NotNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_output('out', self.get_output__out)

    def get_output__out(self, env):
        return not self.resolve_input('in', env)


class AddNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('arg1')
        self.declare_input('arg2')
        self.declare_output('result', self.get_output__result, self.deploy_output__result)

    def get_output__result(self, env):
        op1 = self.resolve_input('arg1', env)
        op2 = self.resolve_input('arg2', env)
        return op1 + op2

    def deploy_output__result(self):
        conn1 = self.get_input_connection('arg1')
        conn2 = self.get_input_connection('arg2')
        return LanguageConcat(
            conn1.output.resolve_deploy(conn1.output_name),
            conn2.output.resolve_deploy(conn2.output_name),
            VariableStatement(
                NodeOutputVariableName(self.id, 'result'),
                LanguageOperation('+',
                                  NodeOutputVariableName(conn1.output.id, conn1.output_name),
                                  NodeOutputVariableName(conn2.output.id, conn2.output_name)
                                  )
            )
        )


class MultiplyNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('arg1')
        self.declare_input('arg2')
        self.declare_output('result', self.get_output__result, self.deploy_output__result)

    def get_output__result(self, env):
        op1 = self.resolve_input('arg1', env)
        op2 = self.resolve_input('arg2', env)
        return op1 * op2

    def deploy_output__result(self):
        conn1 = self.get_input_connection('arg1')
        conn2 = self.get_input_connection('arg2')
        return LanguageConcat(
            conn1.output.resolve_deploy(conn1.output_name),
            conn2.output.resolve_deploy(conn2.output_name),
            VariableStatement(
                NodeOutputVariableName(self.id, 'result'),
                LanguageOperation('*',
                                  NodeOutputVariableName(conn1.output.id, conn1.output_name),
                                  NodeOutputVariableName(conn2.output.id, conn2.output_name)
                                  )
            )
        )


class LoopNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('iter')
        self.declare_input('value')
        self.declare_input('__continue__')
        self.declare_output('value', self.get_output__value)
        self.declare_output('__continue__', self.get_output____continue__)

        BaseNode.connect(self, self, '__continue__', '__continue__')

        self.state['init'] = False

    def get_output__value(self, env):
        if self.resolve_input('iter'):
            return self.resolve_input('__continue__', env)
        else:
            return self.resolve_input('value', env)

    def get_output____continue__(self, env):
        return self.get_output__value(env)


class MapNode(BaseNode):
    """
    Maps an input array to an output array of equal length with each element transformed based on an internal graph

    Inputs
    ------
    array: Input array to be transformed

    value (internal): Result of an elementwise transformation

    Outputs
    -------
    mapped: Output array which has been mapped by a transformation

    entry (internal): Element of the input array to be transformed

    index (internal): Index of the element to be transformed
    """

    def __init__(self):
        super().__init__()

        self.declare_input('array')
        self.declare_input('value', True)
        self.declare_output('mapped', self.get_output__mapped)
        self.declare_output('entry', self.get_ioutput__entry, True)
        self.declare_output('index', self.get_ioutput__index, True)

    def get_output__mapped(self, env):
        arr = self.resolve_input('array', env)
        out_arr = []
        for i in range(len(arr)):
            self.state['current_index'] = i
            self.state['current_entry'] = arr[i]
            out_arr.append(self.resolve_input('value', env))
        return out_arr

    def get_ioutput__entry(self, env):
        return self.state['current_entry']

    def get_ioutput__index(self, env):
        return self.state['current_index']


class ArrayMergeNode(BaseNode):
    """
    Merges arrays or scalar values into an output array

    Inputs
    ------
    in_<n>: Arrays or scalars to be merged into the output array

    Outputs
    -------
    merged: The result of the array merging operation
    """

    def __init__(self, array_count):
        super().__init__()

        self.array_count = array_count

        for n in range(self.array_count):
            self.declare_input('in_%d' % n)
        self.declare_output('merged', self.get_output__merged)

    def get_output__merged(self, env):
        out = []
        for n in range(self.array_count):
            val = self.resolve_input('in_%d' % n, env)
            if isinstance(val, Iterable):
                out.extend(val)
            else:
                out.append(val)
        return out


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

        self.declare_output('object', self.get_output__object)

    def get_output__object(self, env):
        out = {}
        for i in range(self.property_count):
            out[self.resolve_input('key_%d' % i, env)] = self.resolve_input('value_%d' % i, env)
        return out


class DummyNode(BaseNode):
    """
    Passes through an input while requiring another input and throwing its value out

    Inputs
    ------
    in: Input value to be passed on to output
    extra: Input value which will be resolved but then thrown out

    Outputs
    -------
    out: Resolved value of the in input
    """

    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_input('extra')
        self.declare_output('out', self.get_output__out)

    def get_output__out(self, env):
        val = self.resolve_input('in', env)
        self.resolve_input('extra', env)
        return val


class IndexNode(BaseNode):
    """
    Dynamically accesses the index of input data

    Inputs
    ------
    data: The data which the index will be applied to

    index: The index to access from the input data

    Outputs
    -------
    value: Result of the indexed operation
    """

    def __init__(self, multiple=False):
        super().__init__()

        self.multiple = multiple

        self.declare_input('data')
        self.declare_input('index')
        self.declare_output('value', self.get_output__value)

    def get_output__value(self, env):
        data = self.resolve_input('data', env)
        idx = self.resolve_input('index', env)
        if self.multiple:
            idx_split = idx.split('.')
            current_val = data
            for current_idx in idx_split:
                if self.is_int_indexed(current_val):
                    current_val = current_val[current_idx]
                else:
                    current_val = getattr(current_val, current_idx)
            return current_val
        else:
            if self.is_int_indexed(data):
                return data[idx]
            else:
                return getattr(data, idx)

    @staticmethod
    def is_int_indexed(obj):
        # return isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, dict)
        return hasattr(obj, '__getitem__')


class IndexOfNode(BaseNode):
    """
    Searches for a value based on equality in a given array

    Inputs
    ------
    array: The array to search through

    search: Value to search for in target array

    Outputs
    -------
    index: The index of the search element in target array. If not found, it is equal to -1
    """

    def __init__(self):
        super().__init__()

        self.declare_input('array')
        self.declare_input('search')
        self.declare_output('index', self.get_output__index)

    def get_output__index(self, env):
        arr = self.resolve_input('array', env)
        search = self.resolve_input('search', env)
        for i in range(len(arr)):
            if arr[i] == search:
                return i
        return -1


class SliceNode(BaseNode):
    """
    Slices an array according to python slice rules

    Inputs
    ------
    array: Array which should be sliced

    slice_start: Starting index of array slice

    slice_end: Ending index of array slice

    slice_step: Step size for slice operation

    Outputs
    -------
    array: Sliced version of input array
    """

    def __init__(self):
        super().__init__()

        self.declare_input('array')
        self.declare_input('slice_start')
        self.declare_input('slice_end')
        self.declare_input('slice_step')
        self.declare_output('array', self.get_output__array)

    def get_output__array(self, env):
        slice_obj = slice(
            self.resolve_input('slice_start', env, allow_unconnected=True),
            self.resolve_input('slice_end', env, allow_unconnected=True),
            self.resolve_input('slice_step', env, allow_unconnected=True)
        )
        return self.resolve_input('array', env)[slice_obj]


class ReadEnvironmentNode(IndexNode):
    """
    Returns the environment state as an object

    Inputs
    ------
    None

    Outputs
    -------
    value: The value of the environment state in object form
    """

    def __init__(self):
        super().__init__()

        self.declare_output('value', self.get_output__value)

    def get_output__value(self, env):
        return env


class EnvironmentContainer:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def get_nodes(self):
        return self.nodes

    def reset_nodes(self):
        for node in self.nodes:
            node.clear_cache()
            node.reset_state()


BaseNode.NodeRegistry.extend([
    DataSourceNode,
    PassThroughNode,
    PrintNode,
    ParseIntNode,
    ParseFloatNode,
    TypeNode,
    SwitchNode,
    VariableNode,
    IncrementNode,
    EqualsNode,
    NotNode,
    AddNode,
    MultiplyNode,
    LoopNode,
    MapNode,
    ArrayMergeNode,
    DictionaryNode,
    DummyNode,
    IndexNode,
    SliceNode,
    ReadEnvironmentNode
])
