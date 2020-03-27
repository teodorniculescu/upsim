from blocks.BasicBlock import *
from values.BaseValue import BaseValue


class StateBlock(BasicBlock):
    def __init__(self, name: str, io_name: str):
        io = BaseValue(io_name, self)
        super().__init__(name)
        super().add_pin(io, PIN_TYPE_IO)

