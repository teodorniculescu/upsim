from antlr.FileSyntaxErrorListener import *
HIGH: int = 1
LOW: int = 0

PIN_TYPE_INPUT: int = 0
PIN_TYPE_OUTPUT: int = 1
PIN_TYPE_IO: int = 2
PIN_TYPE_ERROR: int = 3

pin_switcher: dict = {
    PIN_TYPE_INPUT: "IN",
    PIN_TYPE_OUTPUT: "OUT",
    PIN_TYPE_IO: "IO"
}


class BaseValue:
    # How the pin is identified among other pins on the block
    __name: str
    # What is the current value of the pin
    __value: int
    # Check if the current value has been previously set or not
    __value_is_set: bool

    def __init__(self, name: str, pin_type: int):
        self.__set_name(name)
        self.__set_pin_type(pin_type)
        self.__value_is_set = False

    @staticmethod
    def __check_pin_type(pin_type: int) -> None:
        if pin_type not in pin_switcher:
            raise Exception(ERROR_INVALID_PIN_TYPE % pin_type)

    def __set_pin_type(self, pin_type: int) -> None:
        BaseValue.__check_pin_type(pin_type)
        self.__pin_type = pin_type

    def get_pin_type_str(self) -> str:
        if self.__pin_type in pin_switcher:
            return pin_switcher[self.__pin_type]
        raise Exception(ERROR_INVALID_PIN_TYPE % self.__pin_type)

    def get_pin_type(self):
        if self.__pin_type in pin_switcher:
            return self.__pin_type
        raise Exception(ERROR_INVALID_PIN_TYPE % self.__pin_type)

    def __set_name(self, name: str) -> None:
        if name is None:
            raise Exception('name must not be None')
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_value(self, value: int) -> None:
        if value != HIGH and value != LOW:
            raise Exception('the value must be either HIGH:{:d} or'
                            'LOW:{:d}.'.format(HIGH, LOW)
                            + "Received value: " + str(value) + ".")
        self.__value_is_set = True
        self.__value = value

    def get_value(self) -> int:
        return self.__value

    def get_value_is_set(self) -> bool:
        return self.__value_is_set

    def is_low(self) -> bool:
        if self.__value == LOW:
            return True
        return False

    def is_high(self) -> bool:
        if self.__value == HIGH:
            return True
        return False

    def get_pin_state(self) -> str:
        value_str = str(self.__value)
        return self.__name + "=" + value_str

    def reset(self) -> None:
        self.__value_is_set = False
        self.__value = LOW;

    def is_set(self):
        return self.__value_is_set
