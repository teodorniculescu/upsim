"""
This is the base class which MUST be used by any saved block. Its an interface which implements all the basic methods
which will be used for analysing the circuit behaviour.
"""


class BasicBlock:
    input_pins = []
    output_pins = []
    io_pins = []

    def __init__(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')

    """Specifies the internal behaviour of the block, how the inputs are used in order to obtain the outputs."""

    def calculate(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')
