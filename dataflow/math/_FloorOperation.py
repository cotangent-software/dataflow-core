from dataflow.gen import *


class FloorOperation(LanguageValue):
    def __init__(self, value: LanguageValue):
        super().__init__(
            LanguageOperation(
                SubtractSymbol(),
                value,
                LanguageOperation(
                    ModuloSymbol(),
                    value,
                    LanguageValue(1)
                )
            )
        )
