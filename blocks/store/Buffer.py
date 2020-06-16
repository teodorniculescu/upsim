from blocks.LogicalBlock import LogicalBlock
from values.BaseValue import BaseValue, PIN_TYPE_INPUT, PIN_TYPE_OUTPUT


class DIGITAL_TRI_STATE_BUFFER(LogicalBlock):
    def __init__(self, block_name: str):
        super().__init__(block_name)
        super().add_pin(BaseValue("in", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("en", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("out", PIN_TYPE_OUTPUT))

    def calculate(self) -> None:
        input_pin: BaseValue
        enable_pin: BaseValue
        output_pin: BaseValue
        [input_pin, enable_pin] = self.get_all_pins_with_type(PIN_TYPE_INPUT).values()
        [output_pin] = self.get_all_pins_with_type(PIN_TYPE_OUTPUT).values()
        if enable_pin.is_high():
            if input_pin.is_high():
                output_pin.set_high()
            elif input_pin.is_low():
                output_pin.set_low()
        else:
            output_pin.set_high_impedance()


class BUFFER(LogicalBlock):
    def __init__(self, block_name: str):
        super().__init__(block_name)
        super().add_pin(BaseValue("in", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("out", PIN_TYPE_OUTPUT))

    def calculate(self) -> None:
        input_pin: BaseValue
        output_pin: BaseValue
        [input_pin] = self.get_all_pins_with_type(PIN_TYPE_INPUT).values()
        [output_pin] = self.get_all_pins_with_type(PIN_TYPE_OUTPUT).values()
        if input_pin.is_high():
            output_pin.set_high()
        elif input_pin.is_low():
            output_pin.set_low()
