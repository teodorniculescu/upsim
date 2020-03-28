from values.BaseValue import BaseValue
import itertools

PIN_TYPE_INPUT = 0
PIN_TYPE_OUTPUT = 1
PIN_TYPE_IO = 2


"""
This is the base class which MUST be used by any saved block. Its an interface which implements all the basic methods
which will be used for analysing the circuit behaviour.
"""


class BasicBlock:
    __input_pins: list # of BaseValues
    __output_pins: list # of BaseValues
    __io_pins: list # of BaseValues
    __name: str

    def __init__(self, name: str):
        if type(name) is not str:
            raise Exception("invalid name \'" + str(name) + "\' is type " + str(type(name))
                            + " instead of str")
        self.__input_pins = []
        self.__output_pins = []
        self.__io_pins = []
        self.__name = name
        print(self.__name + " created!")

    def add_pin(self, pin: BaseValue, pin_type: int) -> None:
        # Check if the parameters are correct
        if not isinstance(pin, BaseValue):
            raise Exception("pin is type " + str(type(pin)) + " instead of BaseValue")
        if not isinstance(pin_type, int):
            raise Exception("pin_type is type " + str(type(pin_type)) + " instead of int")

        # Check all types of pins
        if pin_type == PIN_TYPE_INPUT:
            self.__input_pins.append(pin)
        elif pin_type == PIN_TYPE_OUTPUT:
            self.__output_pins.append(pin)
        elif pin_type == PIN_TYPE_IO:
            self.__io_pins.append(pin)
        else:
            raise Exception("Unknown pin type " + str(pin_type))

    def get_all_pins_with_type(self, pin_type: int) -> list:
        # Check if the parameters are correct
        if not isinstance(pin_type, int):
            raise Exception("pin_type is type " + str(type(pin_type)) + " instead of int")

        # Check all types of pins
        if pin_type == PIN_TYPE_INPUT:
            result = self.__input_pins
        elif pin_type == PIN_TYPE_OUTPUT:
            result = self.__output_pins
        elif pin_type == PIN_TYPE_IO:
            result = self.__io_pins
        else:
            raise Exception("Unknown pin type " + str(pin_type))
        return result

    def get_name(self) -> str:
        return self.__name

    def get_pin(self, index: int, pin_type: int) -> BaseValue:
        return self.get_all_pins_with_type(pin_type)[index]

    def get_pin_with_name(self, pin_name: str) -> BaseValue:
        pin: BaseValue
        for pin in self.__input_pins:
            if pin.get_name() == pin_name:
                return pin
        for pin in self.__output_pins:
            if pin.get_name() == pin_name:
                return pin
        for pin in self.__io_pins:
            if pin.get_name() == pin_name:
                return pin
        raise Exception("Pin " + pin_name + " does not exist.")

    """Specifies the internal behaviour of the block, how the inputs are used in order to obtain the outputs."""

    def calculate(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')

    def read_stage(self):
        input_pin: BaseValue
        connected_pin: BaseValue
        for input_pin in self.__input_pins:
            connected_pin = input_pin.get_connected_pin()
            value = connected_pin.get_value()
            input_pin.set_value(value)

    def show_state(self):
        pin: BaseValue
        for pin in self.__input_pins:
            print(self.__name + "::" + "input" + "::" + pin.get_pin_state())
        for pin in self.__output_pins:
            print(self.__name + "::" + "output" + "::" + pin.get_pin_state())
        for pin in self.__io_pins:
            print(self.__name + "::" + "io" + "::" + pin.get_pin_state())

    def get_all_pins(self):
        return list(itertools.chain(self.__input_pins, self.__output_pins, self.__io_pins))

    def reset(self):
        pin: BaseValue
        for pin in self.get_all_pins():
            pin.reset()

    def output_changed_state(self):
        pin: BaseValue
        for pin in self.__output_pins:
            if pin.changed_state_from_last_time_step():
                return True
        return False
