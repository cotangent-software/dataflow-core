import uuid
from typing import Union

from ._Connection import Connection
from ._GraphError import GraphError
from ..gen import NodeOutputVariableName, LanguageNone, NodeOutputFunctionName, FunctionDeclaration, LanguageConcat, \
    ReturnStatement, LanguageNoop, VariableName, ArrayIndex, LanguageValue, NodePrivateVariableName, IfStatement, \
    LanguageOperation, CompareEqualsSymbol, LanguageUndefined, VariableSetStatement


def array_find(arr, fun):
    for i in arr:
        if fun(i):
            return i
    return None


class BaseNode:
    """Base class which every node must extend

    Inputs
        None

    Outputs
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

    def get_input_connection(self, input_name, allow_unconnected=False) -> Connection:
        conn = array_find(self.connections, lambda x: x.input_name == input_name and x.input == self)
        if conn is not None or allow_unconnected:
            return conn
        else:
            raise GraphError('Could not find input connection with name \'%s\'' % input_name)

    def get_input_connection_variable_name(self, input_name, allow_unconnected=False) \
            -> Union[VariableName, LanguageNone]:
        conn = self.get_input_connection(input_name, allow_unconnected=allow_unconnected)
        if conn is not None:
            return NodeOutputVariableName(conn.output.id, conn.output_name)
        else:
            return LanguageNone()

    def get_input_connection_function_name(self, input_name) -> NodeOutputFunctionName:
        conn = self.get_input_connection(input_name)
        return NodeOutputFunctionName(conn.output.id, conn.output_name)

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

    def resolve_deploy_function(self, name):
        return FunctionDeclaration(
            NodeOutputFunctionName(self.id, name),
            LanguageConcat(
                self.resolve_deploy(name),
                ReturnStatement(NodeOutputVariableName(self.id, name))
            )
        )

    def resolve_input_deploy(self, input_name, allow_unconnected=False):
        conn = self.get_input_connection(input_name, allow_unconnected=allow_unconnected)
        if conn is not None:
            return conn.output.resolve_deploy(conn.output_name)
        else:
            return LanguageNoop()

    def resolve_input_deploy_function(self, input_name, allow_unconnected=False):
        conn = self.get_input_connection(input_name, allow_unconnected=allow_unconnected)
        if conn is not None:
            return conn.output.resolve_deploy_function(conn.output_name)
        else:
            return LanguageNoop()

    def deploy_state_init(self, name, default):
        state_var = ArrayIndex(
                        VariableName('state'),
                        LanguageValue(NodePrivateVariableName(self.id, name).value)
                    )
        return LanguageConcat(
            IfStatement(
                LanguageOperation(
                    CompareEqualsSymbol(),
                    state_var,
                    LanguageUndefined()
                ),
                VariableSetStatement(state_var, default, dictionary_set=True),
                if_type='if'
            )
        )

    def deploy_state_value(self, name):
        return ArrayIndex(
            VariableName('state'),
            LanguageValue(NodePrivateVariableName(self.id, name).value)
        )

    def deploy_state_update(self, name, value):
        state_var = ArrayIndex(
            VariableName('state'),
            LanguageValue(NodePrivateVariableName(self.id, name).value)
        )
        return VariableSetStatement(
            state_var,
            value,
            dictionary_set=True
        )

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
