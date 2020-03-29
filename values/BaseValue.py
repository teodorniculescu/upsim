HIGH: int = 1
LOW: int = 0


class BaseValue:
    __name: str
    __value: int
    __value_is_set: bool = False
    __changed_state: bool = False

    def __init__(self, name: str, block, value: int = None):
        self.__set_name(name)
        if value is not None:
            """
            The value is not initialized yet, but will probably be
            initialized later during the read or calculate stages
            """
            self.set_value(value)

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
        self.__value_is_set = False
        self.__changed_state = False

    def is_set(self):
        return self.__value_is_set

    def changed_state_from_last_time_step(self) -> bool:
        return self.__changed_state
