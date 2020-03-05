from blocks import LogicalBlock
from values import LogicalValue


class Logical(LogicalBlock):
    def __init__(self, name_input0: str, name_input1: str, name_output0: str):
        input0 = LogicalValue.LogicalValue(name_input0)
        input1 = LogicalValue.LogicalValue(name_input1)
        output0 = LogicalValue.LogicalValue(name_output0)
        self.input_pins = [input0, input1]
        self.output_pins = [output0]
        self.io_pins = None

    def __calculate_output_pins(self) -> int:
        if self.input_pins[0].is_low() or self.input_pins[1].is_low():
            return LogicalValue.LOW
        return LogicalValue.HIGH

    def calculate(self) -> None:
        self.output_pins[0].set_value(self.__calculate_output_pins())
