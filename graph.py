import threading
from enum import Enum
from flask import Flask, request
Types = Enum('Types', 'STRING INT FLOAT ARRAY MIXED')


def array_find(arr, fun):
    for i in arr:
        if fun(i):
            return i
    return None


class GraphError(Exception):
    pass


class ExecutionEnvironment:
    def __init__(self):
        self.properties = {}


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
    def __init__(self):
        self.connections = []
        self.declared_inputs = []
        self.declared_outputs = []
        self.output_handlers = {}

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

    @staticmethod
    def connect(connection: 'Connection'):
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
    def __init__(self, data):
        super().__init__()

        self.data = data

        self.declare_output('data', self.get_output__data)

    def get_output__data(self, env):
        return self.data


class PassThroughNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('in')
        self.declare_output('out', self.get_output__out)

    def get_output__out(self, env):
        return self.resolve_input('in', env)


class WebConfigNode(DataSourceNode):
    def __init__(self, port):
        self.port = port
        self.app = Flask(__name__)
        self.app.use_reloader = False

        threading.Thread(target=self.start_app).start()

        super().__init__({
            'app': self.app
        })

    def start_app(self):
        self.app.run(host='0.0.0.0', port=self.port)


class WebEndpointNode(BaseNode):
    def __init__(self, path, config_node: 'WebConfigNode'):
        super().__init__()

        self.declare_input('data')
        self.declare_output('content', self.get_output__content)

        app = config_node.resolve_output('data')['app']
        app.route(path)(self.endpoint_handler)

    def get_output__content(self, env):
        return self.resolve_input('data', env)

    def endpoint_handler(self):
        return self.resolve_output('content', {
            'args': request.args
        })


class ReadIndexNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('data')
        self.declare_input('index')
        self.declare_output('value', self.get_output__value)

    def get_output__value(self, env):
        return self.resolve_input('data', env)[self.resolve_input('index', env)]


class ReadEnvironmentNode(ReadIndexNode):
    def __init__(self):
        super().__init__()

        self.declare_output('value', self.get_output__value)

    def get_output__value(self, env):
        return env
