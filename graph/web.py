import threading
from flask import Flask, request

from graph.base import DataSourceNode, BaseNode


class WebServerNode(DataSourceNode):
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
    def __init__(self, path, config_node: 'WebServerNode'):
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
