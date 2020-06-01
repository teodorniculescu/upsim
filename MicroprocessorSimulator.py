from unit_test.UnitTestUPSIM import *
from user_interface.UI import UI
import sys


def check_python_version():
    if not(sys.version_info.major == 3 and
        sys.version_info.minor == 6):
        raise Exception("The python version not 3.6")

def main():
    check_python_version()
    UI()

def parse_test():
    # used for updating and checking test results
    test = "nand_gate_with_8_inputs"
    FileInterpreter(
        "unit_test/%s/test" % test,
        #"unit_test/%s/answer" % test,
        "",
        Simulation()
    ).parse()


if __name__ == "__main__":
    main()
