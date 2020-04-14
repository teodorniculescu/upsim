from blocks.BasicBlock import *
from blocks.LogicalBlock import *
from values.BaseValue import *
from typing import List, Tuple


class LogicGate2Inputs1Output(LogicalBlock):
    def __init__(self, block_name: str, input_names: List[str],
                 output_names: List[str]):
        if len(input_names) != 2:
            raise Exception(ERROR_REQUIRE_CERTAIN_NUM_PINS
                            % (2, "INPUT", len(input_names)))
        if len(output_names) != 1:
            raise Exception(ERROR_REQUIRE_CERTAIN_NUM_PINS
                            % (1, "OUTPUT", len(output_names)))
        input0 = BaseValue(input_names[0], PIN_TYPE_INPUT)
        input1 = BaseValue(input_names[1], PIN_TYPE_INPUT)
        output0 = BaseValue(output_names[0], PIN_TYPE_OUTPUT)
        super().__init__(block_name)
        super().add_pin(input0)
        super().add_pin(input1)
        super().add_pin(output0)

    def get_calculate_pins(self) -> Tuple[BaseValue, BaseValue, BaseValue]:
        i0: BaseValue
        i1: BaseValue
        o0: BaseValue
        [i0, i1] = self.get_all_pins_with_type(PIN_TYPE_INPUT).values()
        [o0] = self.get_all_pins_with_type(PIN_TYPE_OUTPUT).values()
        return i0, i1, o0


class AND2(LogicGate2Inputs1Output):
    def __init__(self, block_name: str, input_names: List[str],
                 output_names: List[str]):
        super().__init__(block_name, input_names, output_names)

    def calculate(self):
        (i0, i1, o0) = self.get_calculate_pins()
        if i0.is_high() and i1.is_high():
            o0.set_value(HIGH)
        elif i0.is_low() or i1.is_low():
            o0.set_value(LOW)


class XNOR2(LogicGate2Inputs1Output):
    def __init__(self, block_name: str, input_names: List[str],
                 output_names: List[str]):
        super().__init__(block_name, input_names, output_names)

    def calculate(self):
        (i0, i1, o0) = self.get_calculate_pins()
        if (i0.is_low() and i1.is_low()) or (i0.is_high() and i1.is_high()):
            o0.set_value(HIGH)
        if (i0.is_low() and i1.is_high()) or (i0.is_high() and i1.is_low()):
            o0.set_value(LOW)


class XOR2(LogicGate2Inputs1Output):
    def __init__(self, block_name: str, input_names: List[str],
                 output_names: List[str]):
        super().__init__(block_name, input_names, output_names)

    def calculate(self):
        (i0, i1, o0) = self.get_calculate_pins()
        if (i0.is_low() and i1.is_low()) or (i0.is_high() and i1.is_high()):
            o0.set_value(LOW)
        if (i0.is_low() and i1.is_high()) or (i0.is_high() and i1.is_low()):
            o0.set_value(HIGH)


class NOR2(LogicGate2Inputs1Output):
    def __init__(self, block_name: str, input_names: List[str],
                 output_names: List[str]):
        super().__init__(block_name, input_names, output_names)

    def calculate(self):
        (i0, i1, o0) = self.get_calculate_pins()
        if i0.is_high() or i1.is_high():
            o0.set_value(LOW)
        elif i0.is_low() and i1.is_low():
            o0.set_value(HIGH)


class NAND2(LogicGate2Inputs1Output):
    def __init__(self, block_name: str, input_names: List[str],
                 output_names: List[str]):
        super().__init__(block_name, input_names, output_names)

    def calculate(self):
        (i0, i1, o0) = self.get_calculate_pins()
        if i0.is_high() and i1.is_high():
            o0.set_value(LOW)
        elif i0.is_low() or i1.is_low():
            o0.set_value(HIGH)


class OR2(LogicGate2Inputs1Output):
    def __init__(self, block_name: str, input_names: List[str],
                 output_names: List[str]):
        super().__init__(block_name, input_names, output_names)

    def calculate(self):
        (i0, i1, o0) = self.get_calculate_pins()
        if i0.is_high() or i1.is_high():
            o0.set_value(HIGH)
        elif i0.is_low() and i1.is_low():
            o0.set_value(LOW)


class LogicGateNInputs1Output(LogicalBlock):
    def __init__(self, block_name: str, input_names: List[str],
                 output_names: List[str]):
        if len(input_names) == 0:
            raise Exception(ERROR_REQUIRE_AT_LEAST_NUM_PINS
                            % (1, "INPUT", len(input_names)))
        if len(output_names) != 1:
            raise Exception(ERROR_REQUIRE_CERTAIN_NUM_PINS
                            % (1, "OUTPUT", len(output_names)))
        super().__init__(block_name)
        for name in input_names:
            super().add_pin(BaseValue(name, PIN_TYPE_INPUT))
        output0 = BaseValue(output_names[0], PIN_TYPE_OUTPUT)
        super().add_pin(output0)


class XNOR(LogicGateNInputs1Output):
    def __init__(self, block_name: str, input_names: List[str],
                 output_names: List[str]):
        super().__init__(block_name, input_names, output_names)

    def calculate(self):
        input_pin: BaseValue
        output_pin: BaseValue
        [output_pin] = self.get_all_pins_with_type(PIN_TYPE_OUTPUT).values()
        num_high_inputs: int = 0
        for input_pin in self.get_all_pins_with_type(PIN_TYPE_INPUT).values():
            if input_pin.is_high():
                num_high_inputs += 1
            elif not input_pin.is_set():
                # not all pins are set which means we don't know exactly
                # how many high inputs are there
                return
        if num_high_inputs % 2 == 1:
            output_pin.set_value(LOW)
        else:
            output_pin.set_value(HIGH)


class XOR(LogicGateNInputs1Output):
    def __init__(self, block_name: str, input_names: List[str],
                 output_names: List[str]):
        super().__init__(block_name, input_names, output_names)

    def calculate(self):
        input_pin: BaseValue
        output_pin: BaseValue
        [output_pin] = self.get_all_pins_with_type(PIN_TYPE_OUTPUT).values()
        num_high_inputs: int = 0
        for input_pin in self.get_all_pins_with_type(PIN_TYPE_INPUT).values():
            if input_pin.is_high():
                num_high_inputs += 1
            elif not input_pin.is_set():
                # not all pins are set which means we don't know exactly
                # how many high inputs are there
                return
        if num_high_inputs % 2 == 1:
            output_pin.set_value(HIGH)
        else:
            output_pin.set_value(LOW)





class NOR(LogicGateNInputs1Output):
    def __init__(self, block_name: str, input_names: List[str],
                 output_names: List[str]):
        super().__init__(block_name, input_names, output_names)

    def calculate(self):
        input_pin: BaseValue
        output_pin: BaseValue
        [output_pin] = self.get_all_pins_with_type(PIN_TYPE_OUTPUT).values()
        all_pins_are_low: bool = True
        for input_pin in self.get_all_pins_with_type(PIN_TYPE_INPUT).values():
            if input_pin.is_high():
                output_pin.set_value(LOW)
                return
            if not input_pin.is_low():
                all_pins_are_low = False
        if all_pins_are_low:
            output_pin.set_value(HIGH)


class OR(LogicGateNInputs1Output):
    def __init__(self, block_name: str, input_names: List[str],
                 output_names: List[str]):
        super().__init__(block_name, input_names, output_names)

    def calculate(self):
        input_pin: BaseValue
        output_pin: BaseValue
        [output_pin] = self.get_all_pins_with_type(PIN_TYPE_OUTPUT).values()
        all_pins_are_low: bool = True
        for input_pin in self.get_all_pins_with_type(PIN_TYPE_INPUT).values():
            if input_pin.is_high():
                output_pin.set_value(HIGH)
                return
            if not input_pin.is_low():
                all_pins_are_low = False
        if all_pins_are_low:
            output_pin.set_value(LOW)


class AND(LogicGateNInputs1Output):
    def __init__(self, block_name: str, input_names: List[str],
                 output_names: List[str]):
        super().__init__(block_name, input_names, output_names)

    def calculate(self):
        input_pin: BaseValue
        output_pin: BaseValue
        [output_pin] = self.get_all_pins_with_type(PIN_TYPE_OUTPUT).values()
        all_pins_are_high: bool = True
        for input_pin in self.get_all_pins_with_type(PIN_TYPE_INPUT).values():
            if input_pin.is_low():
                output_pin.set_value(LOW)
                return
            if not input_pin.is_high():
                all_pins_are_high = False
        if all_pins_are_high:
            output_pin.set_value(HIGH)


class NAND(LogicGateNInputs1Output):
    def __init__(self, block_name: str, input_names: List[str],
                 output_names: List[str]):
        super().__init__(block_name, input_names, output_names)

    def calculate(self):
        input_pin: BaseValue
        output_pin: BaseValue
        [output_pin] = self.get_all_pins_with_type(PIN_TYPE_OUTPUT).values()
        all_pins_are_high: bool = True
        for input_pin in self.get_all_pins_with_type(PIN_TYPE_INPUT).values():
            if input_pin.is_low():
                output_pin.set_value(HIGH)
                return
            if not input_pin.is_high():
                all_pins_are_high = False
        if all_pins_are_high:
            output_pin.set_value(LOW)



