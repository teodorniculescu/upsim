from blocks.LogicalBlock import LogicalBlock
from values.BaseValue import BaseValue, PIN_TYPE_INPUT, PIN_TYPE_OUTPUT


class D_LATCH(LogicalBlock):

    def __init__(self, block_name: str):
        super().__init__(block_name)
        super().add_pin(BaseValue("D", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("C", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("R", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("Q", PIN_TYPE_OUTPUT))

    def calculate(self) -> None:
        raise Exception("not yet calculate d latch")
