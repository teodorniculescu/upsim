import blocks.BasicBlock as BB

HIGH: int = 1
LOW: int = 0


class BaseValue:
    __name: str
    __value: int

    def __init__(self, name: str, block, value: int = None):
        self.__set_name(name)
        # The value is not initialized yet but will probably be initialized later.
        if value is None:
            self.__value = None
        else:
            self.set_value(value)

    def __set_name(self, name: str) -> None:
        if name is None:
            raise Exception('name must not be None')
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_value(self, value: int) -> None:
        if value != HIGH and value != LOW:
            raise Exception('the value must be either HIGH:{:d} or LOW:{:d}.'.format(HIGH, LOW) + "Received value: " + str(value) + ".")
        self.__value = value

    def get_value(self) -> int:
        return self.__value

    def is_low(self) -> bool:
        if self.__value is not None and self.__value == LOW:
            return True
        return False

    def is_high(self) -> bool:
        if self.__value is not None and self.__value == HIGH:
            return True
        return False
