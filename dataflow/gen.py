import base64
from typing import Union


class LanguageValue:
    def __init__(self, value):
        self.value = value

    def __es6__(self):
        t = type(self.value)
        if t == str:
            return f'Buffer.from(\'{base64.b64encode(self.value.encode("utf-8")).decode("utf-8")}\', \'base64' \
                   f'\').toString()'
        if issubclass(t, LanguageValue):
            return self.value.__es6__()
        else:
            return self.value


class LanguageNone(LanguageValue):
    def __init__(self):
        super().__init__(None)

    def __es6__(self):
        return 'null'


class LanguageOperation(LanguageValue):
    def __init__(self, op, left: Union[LanguageValue, type(None)], right: Union[LanguageValue, type(None)]):
        super().__init__(None)
        self.op = op
        self.left = left
        self.right = right

    def __es6__(self):
        blank = ''
        left_val = self.left.__es6__() if self.left is not None else blank
        right_val = self.right.__es6__() if self.right is not None else blank
        return f'({left_val}{self.op.__es6__()}{right_val}) '


class BooleanNotSymbol:
    @staticmethod
    def __es6__():
        return '!'


class AddSymbol:
    @staticmethod
    def __es6__():
        return '+'


class MultiplySymbol:
    @staticmethod
    def __es6__():
        return '*'


class CompareEqualsSymbol:
    @staticmethod
    def __es6__():
        return '==='


class VariableName(LanguageValue):
    def __init__(self, name: str):
        super().__init__(name)

    def __es6__(self):
        return self.value


class NodeOutputVariableName(VariableName):
    def __init__(self, node_id, output_name):
        super().__init__(f'v__{node_id}_{output_name}')


class NodeOutputFunctionName(VariableName):
    def __init__(self, node_id, output_name):
        super().__init__(f'f__{node_id}_{output_name}')


class VariableDeclareStatement:
    def __init__(self, variable_name: VariableName, value: LanguageValue):
        self.variable_name = variable_name
        self.value = value

    def __es6__(self):
        return f'let {self.variable_name.__es6__()} = {self.value.__es6__()};'


class VariableUpdateStatement:
    def __init__(self, variable_name: VariableName, value: LanguageValue):
        self.variable_name = variable_name
        self.value = value

    def __es6__(self):
        return f'{self.variable_name.__es6__()} = {self.value.__es6__()};'


class ReturnStatement:
    def __init__(self, value: LanguageValue):
        self.value = value

    def __es6__(self):
        return f'return {self.value.__es6__()};'


class PrintStatement:
    def __init__(self, value: LanguageValue):
        self.value = value

    def __es6__(self):
        return f'console.log({self.value.__es6__()});'


class FunctionDeclaration:
    def __init__(self, name: VariableName, body):
        self.name = name
        self.body = body

    def __es6__(self):
        return f'function {self.name.__es6__()}() {{\n{self.body.__es6__()}\n}}'


class FunctionCall(LanguageValue):
    def __init__(self, name: VariableName, *params):
        super().__init__(None)
        self.name = name
        self.params = params

    def __es6__(self):
        params_str = ', '.join([x.__es6__() for x in self.params])
        return f'{self.name.__es6__()}({params_str})'


class ParseIntCall(LanguageValue):
    def __init__(self, value: LanguageValue):
        super().__init__(value)

    def __es6__(self):
        return f'parseInt({self.value.__es6__()})'


class ParseFloatCall(LanguageValue):
    def __init__(self, value: LanguageValue):
        super().__init__(value)

    def __es6__(self):
        return f'parseFloat({self.value.__es6__()})'


class IfStatement:
    def __init__(self, condition: Union[LanguageValue, type(None)], body, if_type='if'):
        self.condition = condition
        self.body = body
        self.if_type = if_type

    def __es6__(self):
        if_value = 'if'
        if self.if_type == 'elseif':
            if_value = 'else if'
        elif self.if_type == 'else':
            if_value = 'else'
        condition_part = ''
        if self.if_type != 'else':
            condition_part = f'({self.condition.__es6__()})'
        return f'{if_value}{condition_part} {{\n{self.body.__es6__()}\n}}'


class LanguageConcat:
    def __init__(self, *statements):
        self.statements = statements

    def __es6__(self):
        return '\n'.join([x.__es6__() for x in self.statements])


class UtilsBody(LanguageValue):
    def __init__(self):
        super().__init__(None)

    def __es6__(self):
        with open('utils/es6.js', 'r') as fh:
            return fh.read()


def deploy(exposed_node, exposed_output):
    exposed_node.resolve_deploy(exposed_output)
    return LanguageConcat(
        UtilsBody(),
        FunctionDeclaration(
            VariableName('main'),
            LanguageConcat(
                exposed_node.resolve_deploy(exposed_output),
                ReturnStatement(NodeOutputVariableName(exposed_node.id, exposed_output))
            )
        )
    )
