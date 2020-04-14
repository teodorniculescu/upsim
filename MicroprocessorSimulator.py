from unit_test.UnitTestUPSIM import *


def main():
    test = "simple_logic_gates_n"
    FileInterpreter(
        "unit_test/%s/test" % test,
        #"unit_test/%s/answer" % test,
        "",
        Simulation()
    ).parse()


if __name__ == "__main__":
    main()
