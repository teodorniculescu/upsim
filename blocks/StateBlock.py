from blocks.BasicBlock import *
from values.BaseValue import BaseValue


class StateBlock(BasicBlock):
    def __init__(self, name: str, pin_type: int, pin_name: str = "val"):
        super().__init__(name)
        super().add_pin(BaseValue(pin_name, pin_type))


class GroundBlock(StateBlock):
    def __init__(self, name: str,
                 pin_name: str = "val"):
        pin_type: int = PIN_TYPE_OUTPUT
        super().__init__(name=name, pin_type=pin_type, pin_name=pin_name)

