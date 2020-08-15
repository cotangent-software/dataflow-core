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
