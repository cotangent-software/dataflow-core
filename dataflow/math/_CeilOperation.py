from dataflow.gen import *


class CeilOperation(LanguageValue):
    def __init__(self, value: LanguageValue):
        super().__init__(
            LanguageOperation(
                SubtractSymbol(),
                LanguageOperation(
                    AddSymbol(),
                    value,
                    LanguageValue(1)
                ),
                LanguageOperation(
                    ModuloSymbol(),
                    value,
                    LanguageValue(1)
                )
            )
        )
