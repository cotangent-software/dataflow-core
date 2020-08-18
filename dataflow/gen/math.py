from dataflow.gen import FunctionCall, LanguageValue, VariableName, LanguageOperation, DivideSymbol


class MathPowerCall(LanguageValue):
    def __init__(self, base: LanguageValue, power: LanguageValue):
        super().__init__(None)
        self.base = base
        self.power = power

    def __es6__(self, c):
        return FunctionCall(VariableName('Math.pow'), self.base, self.power).__es6__(c)

    def __py__(self, c):
        return FunctionCall(VariableName('math.pow'), self.base, self.power).__py__(c)


class MathRootCall(LanguageValue):
    def __init__(self, value: LanguageValue, root: LanguageValue):
        super().__init__(None)
        self.value = value
        self.root = root

    def __es6__(self, c):
        return FunctionCall(
            VariableName('Math.pow'),
            self.value,
            LanguageOperation(DivideSymbol(), LanguageValue(1), self.root)
        ).__es6__(c)

    def __py__(self, c):
        return FunctionCall(
            VariableName('math.pow'),
            self.value,
            LanguageOperation(DivideSymbol(), LanguageValue(1), self.root)
        ).__py__(c)


class MathLogCall(LanguageValue):
    def __init__(self, value: LanguageValue, base: LanguageValue):
        super().__init__(None)
        self.value = value
        self.base = base

    def __es6__(self, c):
        return LanguageOperation(
            DivideSymbol(),
            FunctionCall(
                VariableName('Math.log'),
                self.value
            ),
            FunctionCall(
                VariableName('Math.log'),
                self.base
            )
        ).__es6__(c)

    def __py__(self, c):
        return FunctionCall(VariableName('math.log'), self.value, self.base).__py__(c)


class MathAbsoluteValueCall(LanguageValue):
    def __init__(self, value: LanguageValue):
        super().__init__(value)

    def __es6__(self, c):
        return FunctionCall(VariableName('Math.abs'), self.value).__es6__(c)

    def __py__(self, c):
        return FunctionCall(VariableName('abs'), self.value).__py__(c)
