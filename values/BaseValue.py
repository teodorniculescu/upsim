from antlr.FileSyntaxErrorListener import *
from typing import List, Tuple, Dict
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


RIGHT: int = 0
LEFT: int = 1
UP: int = 2
DOWN: int = 3

direction_dict: Dict[str, int] = {
    'RIGHT': RIGHT,
    'LEFT': LEFT,
    'UP': UP,
    'DOWN': DOWN
}


def _get_direction(string: str) -> int:
    if string in direction_dict:
        return direction_dict[string]
    raise Exception(ERROR_INVALID_DIRECTION_STRING % string)


class BaseValue:
    # How the pin is identified among other pins on the block
    __name: str
    # What is the current value of the pin
    __value: int
    # Check if the current value has been previously set or not
    __value_is_set: bool
    # What was the previous value of the pin
    __prev_value: int
    __prev_value_is_set: bool
    __direction_list: List[int]

    __original_position: Tuple[int, int]
    __original_position_is_set: bool

    def __init__(self, name: str, pin_type: int):
        self.__set_name(name)
        self.__set_pin_type(pin_type)
        self.__value_is_set = False
        self.__prev_value_is_set = False
        self.__direction_list = []
        self.__original_position_is_set = False

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

    def toggle(self) -> None:
        if self.is_high():
            self.set_low()
        elif self.is_low():
            self.set_high()

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

    def set_previous_value(self):
        self.__prev_value_is_set = True
        self.__prev_value = self.__value

    def get_value(self) -> int:
        return self.__value

    def get_value_is_set(self) -> bool:
        return self.__value_is_set

    def set_low(self) -> None:
        self.set_value(LOW)

    def set_high(self) -> None:
        self.set_value(HIGH)

    def is_posedge(self) -> bool:
        return self.__prev_value_is_set and self.__prev_value == LOW and self.__value == HIGH

    def is_negedge(self) -> bool:
        return self.__prev_value_is_set and self.__prev_value == HIGH and self.__value == LOW

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
        self.__value = LOW

    def is_set(self):
        return self.__value_is_set

    def set_high_impedance(self) -> None:
        self.__value_is_set = False
        self.__prev_value_is_set = False
        self.__value = LOW
        self.__prev_value = LOW

    def set_is_state(self, value_is_set: bool) -> None:
        self.__value_is_set = value_is_set

    def add_directions_list(self, direction_list: List[str]) -> None:
        for direction in direction_list:
            self.__direction_list.append(_get_direction(direction))

    def get_directions_list(self) -> List[int]:
        return self.__direction_list

    def set_original_position(self, original_position: Tuple[int, int]) -> None:
        self.__original_position_is_set = True
        self.__original_position = original_position

    def original_position_is_set(self) -> bool:
        return self.__original_position_is_set

    def get_original_position(self) -> Tuple[int, int]:
        if self.__original_position_is_set:
            return self.__original_position
        raise Exception(ERROR_PIN_INVALID_ORIGINAL_POSITION % self.__name)



