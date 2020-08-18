import json
import threading
from flask import Flask, request, Response

from dataflow.base import DataSourceNode, BaseNode


class WebServerNode(DataSourceNode):
    """
    Binds a web server to a particular port

    Inputs
        None

    Outputs
        None
    """
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
    """
    Listens for a particular endpoint to be called on a given web server

    Inputs
        data: The data which should be sent upon request

    Outputs
        content: Value passed through from data input and is sent upon request
    """
    def __init__(self, path, server_node: 'WebServerNode', methods='GET', content_type='text/html'):
        super().__init__()

        self.path = path
        self.content_type = content_type

        self.declare_input('data')
        self.declare_output('content', self.get_output__content)

        if isinstance(methods, str):
            methods = [methods]

        app = server_node.resolve_output('data')['app']

        def func():
            return self.endpoint_handler()
        func.__name__ = self.id
        app.route(path, methods=methods)(func)

    def get_output__content(self, env):
        return self.resolve_input('data', env)

    def endpoint_handler(self):
        return Response(self.resolve_output('content', {
            'args': request.args,
            'form': request.form,
            'method': request.method,
            'path': self.path
        }), mimetype=self.content_type)


class JSONStringifyNode(BaseNode):
    """
    Converts a data object into its JSON serialized form

    Inputs
        object: The object to be serialized

    Outputs
        serialized: A string containing the json encoded object
    """
    def __init__(self, indent=None):
        super().__init__()

        self.indent = indent

        self.declare_input('object')
        self.declare_output('serialized', self.get_output__serialized)

    def get_output__serialized(self, env):
        return json.dumps(self.resolve_input('object', env), indent=self.indent)


class JSONParseNode(BaseNode):
    """
    Converts a JSON serialized string into a data object

    Inputs
        serialized: A string containing the json encoded object

    Outputs
        object: The deserialized object
    """

    def __init__(self):
        super().__init__()

        self.declare_input('object')
        self.declare_output('serialized', self.get_output__serialized)

    def get_output__serialized(self, env):
        return json.loads(self.resolve_input('object', env))


BaseNode.NodeRegistry.extend([
    WebServerNode,
    WebEndpointNode,
    JSONStringifyNode,
    JSONParseNode
])
