HIGH = 1
LOW = 0


class LogicalValue:
    value = None

    def __init__(self, value):
        self.set_value(value)

    def set_value(self, value):
        if value != HIGH and value != LOW:
            raise Exception('the value must be either HIGH:{:d} or LOW:{:d}'.format(HIGH, LOW));
        self.value = value

    def get_value(self):
        return self.value
