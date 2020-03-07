from blocks.LogicalBlock import LogicalBlock
from blocks.BasicBlock import BasicBlock
from values import LogicalValue


class Logical(LogicalBlock):
    def __init__(self, block_name: str, input_names: list, output_names: list):
        input0 = LogicalValue.LogicalValue(input_names[0])
        input1 = LogicalValue.LogicalValue(input_names[1])
        output0 = LogicalValue.LogicalValue(output_names[0])
        super().__init__(block_name)
        super().add_input_pin(input0)
        super().add_input_pin(input1)
        super().add_output_pin(output0)

    def __calculate_output_pins(self) -> int:
        # TODO
        pass

    def calculate(self) -> None:
        self.output_pins[0].set_value(self.__calculate_output_pins())
