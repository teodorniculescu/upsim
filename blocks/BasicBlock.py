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
        if name is not str:
            raise Exception("invalid name " + str(name))
        self.__input_pins = []
        self.__output_pins = []
        self.__io_pins = []
        self.__name = name
        print(self.__name + "created!")

    """Specifies the internal behaviour of the block, how the inputs are used in order to obtain the outputs."""

    def calculate(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')
