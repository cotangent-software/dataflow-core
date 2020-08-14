from dataflow.base import BaseNode
from dataflow.gen import *

op_funcs = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '%': lambda x, y: x % y
}
op_symbols = {
    '+': AddSymbol(),
    '-': SubtractSymbol(),
    '*': MultiplySymbol(),
    '/': DivideSymbol(),
    '%': ModuloSymbol()
}


class OperationNode(BaseNode):
    """
    Generic superclass for basic math operations

    Inputs
    ------
    arg1: First (left-hand) operand of the operation

    arg2: Second (right-hand) operand of the operation

    Outputs
    -------
    result: Resultant of inputs arg1 and arg2 applied to operation
    """
    def __init__(self, op):
        super().__init__()

        self.op_func = op_funcs[op]
        self.op_symbol = op_symbols[op]

        self.declare_input('arg1')
        self.declare_input('arg2')
        self.declare_output('result', self.get_output__result, self.deploy_output__result)

    def get_output__result(self, env):
        op1 = self.resolve_input('arg1', env)
        op2 = self.resolve_input('arg2', env)
        return self.op_func(op1, op2)

    def deploy_output__result(self):
        conn1 = self.get_input_connection('arg1')
        conn2 = self.get_input_connection('arg2')
        return LanguageConcat(
            conn1.output.resolve_deploy(conn1.output_name),
            conn2.output.resolve_deploy(conn2.output_name),
            VariableSetStatement(
                NodeOutputVariableName(self.id, 'result'),
                LanguageOperation(self.op_symbol,
                                  NodeOutputVariableName(conn1.output.id, conn1.output_name),
                                  NodeOutputVariableName(conn2.output.id, conn2.output_name)
                                  )
            )
        )
