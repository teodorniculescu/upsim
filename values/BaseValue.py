from FileSyntaxErrorListener import *
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
    __name: str
    __value: int
    __value_is_set: bool
    __changed_state: bool

    def __init__(self, name: str, pin_type: int):
        self.__set_name(name)
        self.__set_pin_type(pin_type)
        self.__value_is_set = False
        self.__changed_state = False

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
        if (not self.__value_is_set) or (self.__value != value):
            self.__changed_state = True
        else:
            self.__changed_state = False
        self.__value_is_set = True
        self.__value = value

    def get_value(self) -> int:
        if not self.__value_is_set:
            raise Exception("The pin has no set value.")
        return self.__value

    def is_low(self) -> bool:
        if self.__value_is_set and self.__value == LOW:
            return True
        return False

    def is_high(self) -> bool:
        if self.__value_is_set and self.__value == HIGH:
            return True
        return False

    def get_pin_state(self) -> str:
        if self.__value_is_set:
            value_str = str(self.__value)
        else:
            value_str = "None"
        return self.__name + "=" + value_str

    def reset(self) -> None:
        #self.__value_is_set = False
        self.__changed_state = False

    def is_set(self):
        return self.__value_is_set

    def changed_state_from_last_time_step(self) -> bool:
        return self.__changed_state
