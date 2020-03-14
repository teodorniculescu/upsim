from blocks.LogicalBlock import LogicalBlock
from values.LogicalValue import LogicalValue


class AND2(LogicalBlock):
    def __init__(self, block_name: str, input_names: list, output_names: list):
        input0 = LogicalValue(input_names[0])
        input1 = LogicalValue(input_names[1])
        output0 = LogicalValue(output_names[0])
        super().__init__(block_name)
        super().add_input_pin(input0)
        super().add_input_pin(input1)
        super().add_output_pin(output0)

