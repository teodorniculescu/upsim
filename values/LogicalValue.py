HIGH: int = 1
LOW: int = 0


class LogicalValue:
    value: int
    name: str

    def __init__(self, name: str, value: int = None):
        self.set_name(name)
        if value is not None:
            self.set_value(value)

    def set_value(self, value: int) -> None:
        if value != HIGH and value != LOW:
            raise Exception('the value must be either HIGH:{:d} or LOW:{:d}'.format(HIGH, LOW))
        self.value = value

    def get_value(self) -> int:
        return self.value

    def set_name(self, name) -> None:
        if name is None:
            raise Exception('name must not be None')
        self.name = name

    def get_name(self) -> str:
        return self.name

    def is_low(self) -> bool:
        if self.value is not None and self.value == LOW:
            return True
        return False

    def is_high(self) -> bool:
        if self.value is not None and self.value == HIGH:
            return True
        return False
