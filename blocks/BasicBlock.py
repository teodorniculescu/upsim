from values.BaseValue import *
from antlr.FileSyntaxErrorListener import *
from typing import Dict
from database.DBController import Column, Row
from typing import List


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

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise Exception(ERROR_INVALID_BLOCK_NAME %
                            (str(name), str(type(name))))
        self.__input_pins = {}
        self.__output_pins = {}
        self.__io_pins = {}
        self.__name = name

    def get_output_values(self) -> Dict[str, str]:
        result: Dict[str, str] = {}
        pin: BaseValue
        for pin in self.__output_pins.values():
            stored_value: str
            if pin.get_value_is_set() == False:
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

