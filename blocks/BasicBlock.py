from values.BaseValue import BaseValue

"""
This is the base class which MUST be used by any saved block. Its an interface which implements all the basic methods
which will be used for analysing the circuit behaviour.
"""


class BasicBlock:
    __input_pins: list
    __output_pins: list
    __io_pins: list
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

    def add_input_pin(self, pin: BaseValue) -> None:
        if not isinstance(pin, BaseValue):
            raise Exception(str(type(pin)) + " is not BaseValue")
        self.__input_pins.append(pin)

    def get_input_pin(self, index: int) -> BaseValue:
        return self.__input_pins[index]

    def add_output_pin(self, pin: BaseValue) -> None:
        if not isinstance(pin, BaseValue):
            raise Exception(str(type(pin)) + " is not BaseValue")
        self.__output_pins.append(pin)

    def get_output_pin(self, index: int) -> BaseValue:
        return self.__output_pins[index]

    def add_io_pin(self, pin: BaseValue) -> None:
        if not isinstance(pin, BaseValue):
            raise Exception(str(type(pin)) + " is not BaseValue")
        self.__io_pins.append(pin)

    def get_io_pin(self, index: int) -> BaseValue:
        return self.__io_pins[index]

    """Specifies the internal behaviour of the block, how the inputs are used in order to obtain the outputs."""

    def calculate(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')
