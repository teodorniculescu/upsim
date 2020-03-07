class InitialConditions:
    def __init__(self):
        pass


class TimePeriod:
    def __init__(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')

    def read(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')

    def calculate(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')

    def write(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')
