from values.BaseValue import *
from antlr.FileSyntaxErrorListener import *
from typing import Dict
from database.DBController import Column, Row
from typing import List, Tuple

from user_interface.PanelHandler import CODE
from user_interface.DataStructure import ParamGridElem, ParamGridRow, ParamGrid, ParamElem


class BasicBlock:
    """
    This is the base class which MUST be used by any saved block. Its an
    interface which implements all the basic methods which will be used for
    analysing the circuit behaviour.
    """
    __input_pins: Dict[str, BaseValue]
    __output_pins: Dict[str, BaseValue]
    __io_pins: Dict[str, BaseValue]
    __name: str
    __position: Tuple[int, int]
    __position_is_set: bool

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise Exception(ERROR_INVALID_BLOCK_NAME %
                            (str(name), str(type(name))))
        self.__input_pins = {}
        self.__output_pins = {}
        self.__io_pins = {}
        self.__name = name
        self.__position_is_set = False

    def get_gui_grid(self) -> ParamGrid:
        result: ParamGrid = ParamGrid([])
        height_pins = max(len(self.__input_pins), len(self.__output_pins))
        num_rows = height_pins * 2 + 1
        num_cols = 5
        for row_index in range(num_rows):
            row: ParamGridRow = ParamGridRow([])
            for col_index in range(num_cols):
                row.append(ParamGridElem(("", ParamElem({}))))
            result.append(row)
        # configure the top and bottom rows
        result[0][1] = (CODE.BORDER_LEFT_UP, [])
        result[0][2] = (CODE.BORDER_UP, [])
        result[0][3] = (CODE.BORDER_RIGHT_UP, [])
        result[num_rows-1][1] = (CODE.BORDER_LEFT_DOWN, [])
        result[num_rows-1][2] = (CODE.BORDER_DOWN, [])
        result[num_rows-1][3] = (CODE.BORDER_RIGHT_DOWN, [])
        # configure first and last columns (input and output pins)
        self.__add_gui_pins_grid(result, self.__input_pins, 0, CODE.WIRE_RIGHT)
        self.__add_gui_pins_grid(result, self.__output_pins, 4, CODE.WIRE_LEFT)
        # add left and wight borders
        row_index: int = 1
        while row_index < num_rows - 1:
            result[row_index][1] = (CODE.BORDER_LEFT, [])
            result[row_index][3] = (CODE.BORDER_RIGHT, [])
            row_index += 1
        return result

    # used by get_gui_grid to add input pins and output pins
    def __add_gui_pins_grid(
            self,
            grid: ParamGrid,
            pins_dict: Dict[str, BaseValue],
            column: int,
            cell_type: str
    ):
        row_index: int = 1
        for pin in pins_dict.values():
            cell_param = ParamElem({"name": pin.get_name()})
            grid[row_index][column] = \
                ParamGridElem((cell_type, cell_param))
            row_index += 2

    def set_position(self, position: Tuple[int, int]) -> None:
        self.__position_is_set = True
        self.__position = position

    def get_position(self) -> Tuple[int, int]:
        if not self.__position_is_set:
            raise Exception(ERROR_POSITION_NOT_SET % self.__name)
        return self.__position

    def is_positionable(self) -> bool:
        return self.__position_is_set

    def get_output_values(self) -> Dict[str, str]:
        result: Dict[str, str] = {}
        pin: BaseValue
        for pin in self.__output_pins.values():
            stored_value: str
            if not pin.get_value_is_set():
                stored_value = str(None)
            else:
                stored_value = str(pin.get_value())
            result[pin.get_name()] = stored_value
        return result

    def add_pin(self, pin: BaseValue) -> None:
        # Check if the parameters are correct
        if not isinstance(pin, BaseValue):
            raise Exception("pin is type " + str(type(pin))
                            + " instead of BaseValue")
        pin_type: int = pin.get_pin_type()
        if not isinstance(pin_type, int):
            raise Exception("pin_type is type " + str(type(pin_type))
                            + " instead of int")
        if pin.get_name() in self.get_all_pins():
            raise Exception(ERROR_PIN_ALREADY_EXISTS
                            % (pin.get_name(), self.get_name()))
        # Check all types of pins
        if pin_type == PIN_TYPE_INPUT:
            self.__input_pins[pin.get_name()] = pin
        elif pin_type == PIN_TYPE_OUTPUT:
            self.__output_pins[pin.get_name()] = pin
        elif pin_type == PIN_TYPE_IO:
            self.__io_pins[pin.get_name()] = pin
        else:
            raise Exception(ERROR_INVALID_PIN_TYPE % pin_type)

    def get_all_pins_with_type(self, pin_type: int) -> Dict[str, BaseValue]:
        # Check if the parameters are correct
        if not isinstance(pin_type, int):
            raise Exception("pin_type is type " + str(type(pin_type))
                            + " instead of int")

        # Check all types of pins
        if pin_type == PIN_TYPE_INPUT:
            return self.__input_pins
        elif pin_type == PIN_TYPE_OUTPUT:
            return self.__output_pins
        elif pin_type == PIN_TYPE_IO:
            return self.__io_pins
        else:
            raise Exception(ERROR_INVALID_PIN_TYPE % pin_type)

    def get_name(self) -> str:
        return self.__name

    def get_pin_with_name(self, pin_name: str) -> BaseValue:
        all_pins: dict = self.get_all_pins()
        if pin_name in all_pins:
            return all_pins[pin_name]
        raise Exception(ERROR_PIN_DOESNT_EXIST % pin_name)

    def calculate(self) -> None:
        """
        Specifies the internal behaviour of the block, how the inputs are used
        in order to obtain the outputs
        This function must be implemented by each newly added logical block in
        order for the simulation to function correctly,
        :return: None
        """
        raise Exception(type(self), ' ', __name__, ' is not implemented')

    def show_state(self) -> str:
        pin: BaseValue
        state_string: str = self.__name + "("
        for pin in self.get_all_pins().values():
            state_string += pin.get_pin_state() + ", "
        state_string = state_string[:-2]
        state_string += ");\n"
        return state_string

    def get_all_pins(self) -> Dict[str, BaseValue]:
        return {**self.__input_pins, **self.__output_pins,
                **self.__io_pins}

    def reset(self) -> None:
        for pin in self.get_all_pins().values():
            pin.reset()

    def output_changed_state(self) -> bool:
        for pin in self.__output_pins.values():
            if pin.changed_state_from_last_time_step():
                return True
        return False

    def get_vertex_column_descriptions(self) -> List[Column]:
        result: List[Column] = []
        for pin in self.get_all_pins().values():
            result.append(
                Column(
                    self.__name + "." + pin.get_name(),
                    "CHAR(1)"
                )
            )
        return result

    def get_vertex_values(self) -> Row:
        result: Row = Row()
        pin: BaseValue
        pin_value: str
        for pin in self.get_all_pins().values():
            if pin.is_set():
                pin_value = str(pin.get_value())
            else:
                pin_value = "N"
            result.append(pin_value)
        return result

    def get_pins_csv(self, pin_type: int) -> str:
        result: str = ''
        if pin_type == PIN_TYPE_INPUT:
            pin_list = self.__input_pins.keys()
        elif pin_type == PIN_TYPE_OUTPUT:
            pin_list = self.__output_pins.keys()
        elif pin_type == PIN_TYPE_IO:
            pin_list = self.__io_pins.keys()
        else:
            raise Exception(ERROR_INVALID_PIN_TYPE % pin_type)
        for pin in pin_list:
            result += pin + ' '
        result = result[:-1]
        return result
