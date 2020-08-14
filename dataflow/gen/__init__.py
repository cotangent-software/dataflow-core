import base64
from typing import Union


class LanguageBase:
    def __es6__(self, c: 'DeployContext'):
        pass


class LanguageValue(LanguageBase):
    def __init__(self, value):
        self.value = value

    def __es6__(self, c):
        t = type(self.value)
        if t == str:
            return f'Buffer.from(\'{base64.b64encode(self.value.encode("utf-8")).decode("utf-8")}\', \'base64' \
                   f'\').toString()'
        if issubclass(t, LanguageBase):
            return self.value.__es6__(c)
        else:
            return self.value


class LanguageNone(LanguageValue):
    def __init__(self):
        super().__init__(None)

    def __es6__(self, c):
        return 'null'


class LanguageUndefined(LanguageValue):
    def __init__(self):
        super().__init__(None)

    def __es6__(self, c):
        return 'undefined'


class LanguageNoop(LanguageBase):
    def __es6__(self, c):
        return ''


class LanguageOperation(LanguageValue):
    def __init__(self, op, left: Union[LanguageValue, type(None)], right: Union[LanguageValue, type(None)]):
        super().__init__(None)
        self.op = op
        self.left = left
        self.right = right

    def __es6__(self, c):
        blank = ''
        left_val = self.left.__es6__(c) if self.left is not None else blank
        right_val = self.right.__es6__(c) if self.right is not None else blank
        return f'({left_val}{self.op.__es6__(c)}{right_val}) '


class BooleanNotSymbol(LanguageBase):
    def __es6__(self, c):
        return '!'


class AddSymbol(LanguageBase):
    def __es6__(self, c):
        return '+'


class SubtractSymbol(LanguageBase):
    def __es6__(self, c: 'DeployContext'):
        return '-'


class MultiplySymbol(LanguageBase):
    def __es6__(self, c):
        return '*'


class DivideSymbol(LanguageBase):
    def __es6__(self, c: 'DeployContext'):
        return '/'


class ModuloSymbol(LanguageBase):
    def __es6__(self, c: 'DeployContext'):
        return '%'


class CompareEqualsSymbol(LanguageBase):
    def __es6__(self, c):
        return '==='


class LessThanSymbol(LanguageBase):
    def __es6__(self, c):
        return '<'


class GreaterThanSymbol(LanguageBase):
    def __es6__(self, c):
        return '>'


class LessThanOrEqualSymbol(LanguageBase):
    def __es6__(self, c):
        return '<='


class GreaterThanOrEqualSymbol(LanguageBase):
    def __es6__(self, c):
        return '>='


class EmptyArraySymbol(LanguageBase):
    def __es6__(self, c):
        return '[]'


class EmptyDictSymbol(LanguageBase):
    def __es6__(self, c):
        return '{}'


class VariableName(LanguageValue):
    def __init__(self, name: Union[str, type(None)]):
        super().__init__(name)

    def __es6__(self, c):
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return self.value if self.value is not None else ''


class ArrayIndex(VariableName):
    def __init__(self, array: LanguageValue, index: LanguageValue):
        super().__init__(None)
        self.array = array
        self.index = index

    def __es6__(self, c):
        return f'{self.array.__es6__(c)}[{self.index.__es6__(c)}]'


class NodeOutputVariableName(VariableName):
    def __init__(self, node_id, output_name):
        super().__init__(f'v__{node_id}_{output_name}')


class NodePrivateVariableName(VariableName):
    def __init__(self, node_id, internal_name):
        super().__init__(f'vi__{node_id}_{internal_name}')


class NodeOutputFunctionName(VariableName):
    def __init__(self, node_id, output_name):
        super().__init__(f'f__{node_id}_{output_name}')


class LanguageStatement(LanguageBase):
    def __init__(self, value):
        self.value = value

    def __es6__(self, c):
        return f'{self.value.__es6__(c)};'


class VariableSet(LanguageBase):
    def __init__(self, variable_name: VariableName, value: LanguageValue, function_parameter=False, dictionary_set=False):
        self.variable_name = variable_name
        self.value = value
        self.function_parameter = function_parameter
        self.dictionary_set = dictionary_set

    def __es6__(self, c):
        has_variable = c.has_symbol(self.variable_name)
        declare = '' if has_variable or self.function_parameter or self.dictionary_set else 'let '
        if not has_variable:
            c.add_variable(self.variable_name)
        return f'{declare}{self.variable_name.__es6__(c)} = {self.value.__es6__(c)}'


class VariableSetStatement(VariableSet):
    def __init__(self, variable_name: VariableName, value: LanguageValue, dictionary_set=False):
        super().__init__(variable_name, value, dictionary_set=dictionary_set)

    def __es6__(self, c):
        return f'{super().__es6__(c)};'


class ReturnStatement(LanguageBase):
    def __init__(self, value: LanguageValue):
        self.value = value

    def __es6__(self, c):
        return f'return {self.value.__es6__(c)};'


class PrintStatement(LanguageBase):
    def __init__(self, value: LanguageValue):
        self.value = value

    def __es6__(self, c):
        return f'console.log({self.value.__es6__(c)});'


class FunctionDeclaration(LanguageBase):
    def __init__(self, name: VariableName, body, *params):
        self.name = name
        self.body = body
        self.params = params

    def __es6__(self, c):
        if not c.has_function(self.name):
            c.add_function(self.name)
            c.push_scope()
            params_str = ', '.join([x.__es6__(c) for x in self.params])
            out = f'function {self.name.__es6__(c)}({params_str}) {{\n{self.body.__es6__(c)}\n}}'
            c.pop_scope()
            return out
        else:
            return LanguageNoop().__es6__(c)


class FunctionCall(LanguageValue):
    def __init__(self, name: VariableName, *params):
        super().__init__(None)
        self.name = name
        self.params = params

    def __es6__(self, c):
        params_str = ', '.join([x.__es6__(c) for x in self.params])
        return f'{self.name.__es6__(c)}({params_str})'


class ParseIntCall(LanguageValue):
    def __init__(self, value: LanguageValue):
        super().__init__(value)

    def __es6__(self, c):
        return f'parseInt({self.value.__es6__(c)})'


class ParseFloatCall(LanguageValue):
    def __init__(self, value: LanguageValue):
        super().__init__(value)

    def __es6__(self, c):
        return f'parseFloat({self.value.__es6__(c)})'


class IfStatement(LanguageBase):
    def __init__(self, condition: Union[LanguageValue, type(None)], body, if_type='if'):
        self.condition = condition
        self.body = body
        self.if_type = if_type

    def __es6__(self, c):
        if_value = 'if'
        if self.if_type == 'elseif':
            if_value = 'else if'
        elif self.if_type == 'else':
            if_value = 'else'
        condition_part = ''
        if self.if_type != 'else':
            condition_part = f'({self.condition.__es6__(c)})'
        c.push_scope()
        out = f'{if_value}{condition_part} {{\n{self.body.__es6__(c)}\n}}'
        c.pop_scope()
        return out


class SimpleLoopStatement(LanguageBase):
    def __init__(self, variable_name: VariableName, start: LanguageValue, end: LanguageValue, body):
        self.variable_name = variable_name
        self.start = start
        self.end = end
        self.body = body

    def __es6__(self, c):
        init = VariableSetStatement(self.variable_name, self.start)
        condition = LanguageStatement(LanguageOperation(LessThanSymbol(), self.variable_name, self.end))
        update = VariableSet(
            self.variable_name,
            LanguageOperation(AddSymbol(), self.variable_name, LanguageValue(1))
        )
        c.push_scope()
        out = f'for({init.__es6__(c)} {condition.__es6__(c)} {update.__es6__(c)}) {{\n{self.body.__es6__(c)}\n}}'
        c.pop_scope()
        return out


class ConditionalLoopStatement(LanguageBase):
    def __init__(self, condition: LanguageValue, body: LanguageBase):
        self.condition = condition
        self.body = body

    def __es6__(self, c: 'DeployContext'):
        c.push_scope()
        out = f'while({self.condition.__es6__(c)}) {{\n{self.body.__es6__(c)}\n}}'
        c.pop_scope()
        return out


class LanguageConcat:
    def __init__(self, *statements):
        self.statements = statements

    def __es6__(self, c):
        return '\n'.join([x.__es6__(c) for x in self.statements if x is not None])


class UtilsBody(LanguageValue):
    def __init__(self):
        super().__init__(None)

    def __es6__(self, c):
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


class DeployContext:
    def __init__(self):
        self.variables = [[]]
        self.functions = [[]]

    def push_scope(self):
        self.variables.append([])
        self.functions.append([])

    def pop_scope(self):
        self.variables.pop()
        self.functions.pop()

    def add_variable(self, variable_name):
        self.variables[-1].append(variable_name)

    def add_function(self, function_name):
        self.functions[-1].append(function_name)

    def get_variables(self):
        return [y for x in self.variables for y in x]

    def get_functions(self):
        return [y for x in self.functions for y in x]

    def get_symbols(self):
        out = []
        out.extend(self.get_variables())
        out.extend(self.get_functions())
        return out

    def has_variable(self, variable_name):
        return variable_name in self.get_variables()

    def has_function(self, function_name):
        return function_name in self.get_functions()

    def has_symbol(self, symbol_name):
        return self.has_variable(symbol_name) or self.has_function(symbol_name)


def deploy(exposed_node, exposed_output, include_utils=True):
    exposed_node.resolve_deploy(exposed_output)
    return LanguageConcat(
        UtilsBody() if include_utils else LanguageNoop(),
        FunctionDeclaration(
            VariableName('main'),
            LanguageConcat(
                exposed_node.resolve_deploy(exposed_output),
                ReturnStatement(NodeOutputVariableName(exposed_node.id, exposed_output))
            ),
            VariableSet(
                VariableName('env'),
                LanguageValue(EmptyDictSymbol()),
                function_parameter=True
            ),
            VariableSet(
                VariableName('state'),
                LanguageValue(EmptyDictSymbol()),
                function_parameter=True
            )
        )
    )
