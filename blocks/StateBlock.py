from blocks.BasicBlock import *
from values.BaseValue import BaseValue


class StateBlock(BasicBlock):
    def __init__(self, name: str, pin_type: int, pin_name: str = "val"):
        super().__init__(name)
        super().add_pin(BaseValue(pin_name, pin_type))

