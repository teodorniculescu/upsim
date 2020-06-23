from blocks.LogicalBlock import LogicalBlock
from values.BaseValue import BaseValue, PIN_TYPE_INPUT, PIN_TYPE_OUTPUT, PIN_TYPE_IO
from user_interface.PanelHandler import CODE
from user_interface.DataStructure import ParamGridElem, ParamGridRow, ParamGrid, ParamElem
from typing import List, Dict


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


class BUS(BUFFER):
    _bus_height: int

    def __init__(self, block_name: str):
        super().__init__(block_name)

    def set_bus_height(self, value: int):
        self._bus_height = value

    def get_gui_grid(self) -> ParamGrid:
        result: ParamGrid = ParamGrid([])
        if self._bus_height is None:
            raise Exception("bus height not declared")
        num_rows = self._bus_height
        for row_index in range(num_rows):
            row: ParamGridRow = ParamGridRow([])
            row.append(ParamGridElem(("", ParamElem({}))))
            result.append(row)
            if row_index == 0:
                result_value = (CODE.BORDER_LEFT_RIGHT_UP, {"name": self.get_name()})
            elif row_index == num_rows - 1:
                result_value = (CODE.BORDER_LEFT_RIGHT_DOWN, {})
            else:
                result_value = (CODE.BORDER_LEFT_RIGHT, {})
            result[row_index][0] = result_value
        return result


class BUS_TRANSMITTER_RECEIVER(LogicalBlock):
    def __init__(self, block_name: str):
        super().__init__(block_name)
        super().add_pin(BaseValue("ENatob", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("ENbtoa", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("a", PIN_TYPE_IO))
        super().add_pin(BaseValue("b", PIN_TYPE_IO))

    def calculate(self) -> None:
        a: BaseValue
        b: BaseValue
        enable_atob: BaseValue
        enable_btoa: BaseValue
        [enable_atob, enable_btoa] = self.get_all_pins_with_type(PIN_TYPE_INPUT).values()
        [a, b] = self.get_all_pins_with_type(PIN_TYPE_IO).values()
        if enable_atob.is_high() and enable_btoa.is_high():
            a.set_high_impedance()
            b.set_high_impedance()
        else:
            if enable_atob.is_high() and a.is_set():
                b.set_value(a.get_value())
            elif enable_btoa.is_high() and b.is_set():
                a.set_value(b.get_value())

class ROM(LogicalBlock):
    def __init__(self,
                 block_name: str,
                 num_addr: int,
                 num_data: int,
                 content: Dict[int, List[int]]
                 ):
        super().__init__(block_name)
        self._num_addr = num_addr
        self._num_data = num_data
        # the first list contains the address in memory
        # the list inside of it has the data
        self._content= content
        for addr in range(num_addr):
            super().add_pin(BaseValue("A" + str(addr), PIN_TYPE_INPUT))
        for data in range(num_data):
            super().add_pin(BaseValue("D" + str(data), PIN_TYPE_OUTPUT))

    def calculate(self) -> None:
        binary_string: str = ''
        for addr in range(self._num_addr):
            pin_name = 'A' + str(addr)
            pin = self.get_pin_with_name(pin_name)
            """
            if not pin.is_set():
                return
            """
            binary_string += str(pin.get_value())
        binary_string = '0b' + binary_string[::-1]
        list_addr = int(binary_string, 2)
        if list_addr in self._content:
            val_list = self._content[list_addr]
        else:
            val_list = [0] * self._num_data
        for data in range(self._num_data):
            pin = self.get_pin_with_name('D' + str(data))
            pin.set_value(val_list[data])




