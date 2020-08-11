import base64


class LanguageValue:
    def __init__(self, value):
        self.value = value

    def __es6__(self):
        t = type(self.value)
        if t == str:
            return f'Buffer.from(\'{base64.b64encode(self.value.encode("utf-8")).decode("utf-8")}\', \'base64' \
                   f'\').toString()'
        else:
            return self.value


class VariableName(LanguageValue):
    def __init__(self, name: str):
        super().__init__(name)

    def __es6__(self):
        return self.value


class NodeOutputVariableName(VariableName):
    def __init__(self, node_id, output_name):
        super().__init__(f'v__{node_id}_{output_name}')


class VariableStatement:
    def __init__(self, variable_name: VariableName, value: LanguageValue):
        self.variable_name = variable_name
        self.value = value

    def __es6__(self):
        return f'let {self.variable_name.__es6__()} = {self.value.__es6__()};'


class ReturnStatement:
    def __init__(self, value: LanguageValue):
        self.value = value

    def __es6__(self):
        return f'return {self.value.__es6__()};'


class FunctionDeclaration:
    def __init__(self, name: VariableName, body):
        self.name = name
        self.body = body

    def __es6__(self):
        return f'function {self.name.__es6__()}() {{\n{self.body.__es6__()}\n}}'


class FunctionCall:
    def __init__(self, name: VariableName, *params):
        self.name = name
        self.params = params

    def __es6__(self):
        params_str = ', '.join([x.__es6__() for x in self.params])
        return f'{self.name.__es6__()}({params_str})'


class LanguageConcat:
    def __init__(self, *statements):
        self.statements = statements

    def __es6__(self):
        return '\n'.join([x.__es6__() for x in self.statements])


def deploy(exposed_node, exposed_output):
    exposed_node.resolve_deploy(exposed_output)
    return FunctionDeclaration(
        VariableName('main'),
        LanguageConcat(
            exposed_node.resolve_deploy(exposed_output),
            ReturnStatement(NodeOutputVariableName(exposed_node.id, exposed_output))
        )
    )
