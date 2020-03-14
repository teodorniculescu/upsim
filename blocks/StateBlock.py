from blocks.BasicBlock import BasicBlock
from values.LogicalValue import LogicalValue


class StateBlock(BasicBlock):
    def __init__(self, name: str, io_name: str):
        io = LogicalValue(io_name)
        super().__init__(name)
        super().add_io_pin(io)

