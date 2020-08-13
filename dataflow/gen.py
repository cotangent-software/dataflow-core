import base64
from typing import Union


class LanguageBase:
    def __es6__(self):
        pass


class LanguageValue(LanguageBase):
    def __init__(self, value):
        self.value = value

    def __es6__(self):
        t = type(self.value)
        if t == str:
            return f'Buffer.from(\'{base64.b64encode(self.value.encode("utf-8")).decode("utf-8")}\', \'base64' \
                   f'\').toString()'
        if issubclass(t, LanguageBase):
            return self.value.__es6__()
        else:
            return self.value


class LanguageNone(LanguageValue):
    def __init__(self):
        super().__init__(None)

    def __es6__(self):
        return 'null'


class LanguageNoop(LanguageBase):
    def __es6__(self):
        return ''


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


class BooleanNotSymbol(LanguageBase):
    def __es6__(self):
        return '!'


class AddSymbol(LanguageBase):
    def __es6__(self):
        return '+'


class MultiplySymbol(LanguageBase):
    def __es6__(self):
        return '*'


class CompareEqualsSymbol(LanguageBase):
    def __es6__(self):
        return '==='


class LessThanSymbol(LanguageBase):
    def __es6__(self):
        return '<'


class GreaterThanSymbol(LanguageBase):
    def __es6__(self):
        return '>'


class LessThanOrEqualSymbol(LanguageBase):
    def __es6__(self):
        return '<='


class GreaterThanOrEqualSymbol(LanguageBase):
    def __es6__(self):
        return '>='


class EmptyArraySymbol(LanguageBase):
    def __es6__(self):
        return '[]'


class EmptyDictSymbol(LanguageBase):
    def __es6__(self):
        return '{}'


class VariableName(LanguageValue):
    def __init__(self, name: Union[str, type(None)]):
        super().__init__(name)

    def __es6__(self):
        return self.value


class ArrayIndex(VariableName):
    def __init__(self, array: LanguageValue, index: LanguageValue):
        super().__init__(None)
        self.array = array
        self.index = index

    def __es6__(self):
        return f'{self.array.__es6__()}[{self.index.__es6__()}]'


class NodeOutputVariableName(VariableName):
    def __init__(self, node_id, output_name):
        super().__init__(f'v__{node_id}_{output_name}')


class NodePrivateVariableName(VariableName):
    def __init__(self, node_id, internal_name):
        super().__init__(f'vi__{node_id}_{internal_name}')


class NodeOutputFunctionName(VariableName):
    def __init__(self, node_id, output_name):
        super().__init__(f'f__{node_id}_{output_name}')


class LanguageStatement:
    def __init__(self, value):
        self.value = value

    def __es6__(self):
        return f'{self.value.__es6__()};'


class VariableDeclare:
    def __init__(self, variable_name: VariableName, value: LanguageValue):
        self.variable_name = variable_name
        self.value = value

    def __es6__(self):
        return f'let {self.variable_name.__es6__()} = {self.value.__es6__()}'


class VariableDeclareStatement(VariableDeclare):
    def __init__(self, variable_name: VariableName, value: LanguageValue):
        super().__init__(variable_name, value)

    def __es6__(self):
        return f'{super().__es6__()};'


class VariableUpdate:
    def __init__(self, variable_name: VariableName, value: LanguageValue):
        self.variable_name = variable_name
        self.value = value

    def __es6__(self):
        return f'{self.variable_name.__es6__()} = {self.value.__es6__()}'


class VariableUpdateStatement(VariableUpdate):
    def __init__(self, variable_name: VariableName, value: LanguageValue):
        super().__init__(variable_name, value)

    def __es6__(self):
        return f'{super().__es6__()};'


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


class SimpleLoopStatement:
    def __init__(self, variable_name: VariableName, start: LanguageValue, end: LanguageValue, body):
        self.variable_name = variable_name
        self.start = start
        self.end = end
        self.body = body

    def __es6__(self):
        init = VariableDeclareStatement(self.variable_name, self.start)
        condition = LanguageStatement(LanguageOperation(LessThanSymbol(), self.variable_name, self.end))
        update = VariableUpdate(
            self.variable_name,
            LanguageOperation(AddSymbol(), self.variable_name, LanguageValue(1))
        )
        return f'for({init.__es6__()} {condition.__es6__()} {update.__es6__()}) {{\n{self.body.__es6__()}\n}}'


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


class UtilsType(FunctionCall):
    def __init__(self, array: LanguageValue):
        super().__init__(VariableName('utils_type'), array)


class UtilsArrayLength(FunctionCall):
    def __init__(self, array: LanguageValue):
        super().__init__(VariableName('utils_array_length'), array)


class UtilsArrayClone(FunctionCall):
    def __init__(self, array: LanguageValue):
        super().__init__(VariableName('utils_array_clone'), array)


class UtilsArrayConcat(FunctionCall):
    def __init__(self, array1: LanguageValue, array2: LanguageValue):
        super().__init__(VariableName('utils_array_concat'), array1, array2)


class UtilsArrayIndexOf(FunctionCall):
    def __init__(self, array: LanguageValue, search: LanguageValue):
        super().__init__(VariableName('utils_array_index_of'), array, search)


class UtilsArraySlice(FunctionCall):
    def __init__(self, array: LanguageValue, slice_start: LanguageValue, slice_end: LanguageValue, slice_step: LanguageValue):
        super().__init__(VariableName('utils_array_slice'), array, slice_start, slice_end, slice_step)


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
