from blocks.BasicBlock import *
from blocks.LogicalBlock import *
from values.BaseValue import *


class AND2(LogicalBlock):
    def __init__(self, block_name: str, input_names: list, output_names: list):
        input0 = BaseValue(input_names[0], self)
        input1 = BaseValue(input_names[1], self)
        output0 = BaseValue(output_names[0], self)
        super().__init__(block_name)
        super().add_pin(input0, PIN_TYPE_INPUT)
        super().add_pin(input1, PIN_TYPE_INPUT)
        super().add_pin(output0, PIN_TYPE_OUTPUT)

    def calculate(self):
        i0: BaseValue
        i1: BaseValue
        o0: BaseValue
        [i0, i1] = self.get_all_pins_with_type(PIN_TYPE_INPUT).values()
        [o0] = self.get_all_pins_with_type(PIN_TYPE_OUTPUT).values()
        if i0.is_high() and i1.is_high():
            o0.set_value(HIGH)
        elif i0.is_low() or i1.is_low():
            o0.set_value(LOW)


