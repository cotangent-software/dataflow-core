from enum import Enum
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
        self.output = output_node
        self.input = input_node
        self.output_name = output_name
        self.input_name = input_name

    def __eq__(self, other):
        return self.output == other.output and\
               self.input == other.input and\
               self.output_name == other.output_name and\
               self.input_name == other.input_name


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
        self.connections = []
        self.declared_inputs = []
        self.declared_outputs = []
        self.output_handlers = {}
        self.output_cache = {}
        self.state = {}

    def declare_input(self, name):
        self.declared_inputs.append(name)

    def declare_output(self, name, handler):
        self.declared_outputs.append(name)
        self.output_handlers[name] = handler

    def resolve_input(self, name, environment=None):
        if environment is None:
            environment = {}
        conn = array_find(self.connections, lambda x: x.input_name == name and x.input == self)
        if conn is not None:
            return conn.output.resolve_output(conn.output_name, environment)
        else:
            raise GraphError('Unconnected input \'%s\' is depended upon' % name)

    def resolve_output(self, name, environment=None):
        if environment is None:
            environment = {}
        print(self)
        return self.output_handlers[name](environment)

    def cache_output(self, name, value):
        self.output_cache[name] = value

    def clear_cache(self, name=None):
        if name is None:
            self.output_cache = {}
        else:
            del self.output_cache[name]

    def reset_state(self):
        self.state = {}

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

        self.declare_output('data', self.get_output__data)

    def get_output__data(self, env):
        return self.data


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
        self.declare_output('out', self.get_output__out)

    def get_output__out(self, env):
        return self.resolve_input('in', env)


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


# class VariableNode(BaseNode):
#     def __init__(self):
#         super().__init__()
#
#         self.has_initialized = False
#
#         self.declare_input('init')
#         self.declare_input('update')
#         self.declare_output('value', self.get_output__value)
#
#     def get_output__value(self, env):
#         if not self.has_initialized:
#             self.has_initialized = True
#             return self.resolve_input('init')
#         else:
#             return self.resolve_input('update')


class VariableNode(BaseNode):
    def __init__(self, init_value=0):
        super().__init__()

        self.init_value = init_value
        self.state['value'] = self.init_value

        self.declare_input('value')
        self.declare_output('update', self.get_output__update)
        self.declare_output('value', self.get_output__value)

    def get_output__update(self, env):
        self.state['value'] = self.resolve_input('value', env)
        return self.state['value']

    def get_output__value(self, env):
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
        self.declare_output('result', self.get_output__result)

    def get_output__result(self, env):
        op1 = self.resolve_input('arg1', env)
        op2 = self.resolve_input('arg2', env)
        return op1 + op2


class MultiplyNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('arg1')
        self.declare_input('arg2')
        self.declare_output('result', self.get_output__result)

    def get_output__result(self, env):
        op1 = self.resolve_input('arg1', env)
        op2 = self.resolve_input('arg2', env)
        return op1 * op2


class LoopNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('iter')
        self.declare_input('value')
        self.declare_input('__continue__')
        self.declare_output('value', self.get_output__value)
        self.declare_output('__continue__', self.get_output____continue__)

        BaseNode.connect(Connection(self, self, '__continue__', '__continue__'))

        self.state['init'] = False

    def get_output__value(self, env):
        if self.resolve_input('iter'):
            return self.resolve_input('__continue__', env)
        else:
            return self.resolve_input('value', env)

    def get_output____continue__(self, env):
        return self.get_output__value(env)


class DummyNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_input('extra')
        self.declare_output('out', self.get_output__out)

    def get_output__out(self, env):
        val = self.resolve_input('in', env)
        self.resolve_input('extra', env)
        return val


class ReadIndexNode(BaseNode):
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
    def __init__(self):
        super().__init__()

        self.declare_input('data')
        self.declare_input('index')
        self.declare_output('value', self.get_output__value)

    def get_output__value(self, env):
        return self.resolve_input('data', env)[self.resolve_input('index', env)]


class ReadEnvironmentNode(ReadIndexNode):
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
    ParseIntNode,
    ParseFloatNode,
    TypeNode,
    VariableNode,
    IncrementNode,
    EqualsNode,
    NotNode,
    AddNode,
    MultiplyNode,
    LoopNode,
    DummyNode,
    ReadIndexNode,
    ReadEnvironmentNode
])
