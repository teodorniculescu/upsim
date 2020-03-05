"""
This is the base class which MUST be used by any saved block. Its an interface which implements all the basic methods
which will be used for analysing the circuit behaviour.
"""


class BasicBlock:
    """Specifies the internal behaviour of the block, how the inputs are used in order to obtain the outputs."""

    def calculate(self):
        raise Exception('The calculate function was not implemented')

