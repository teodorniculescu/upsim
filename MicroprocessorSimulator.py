from unit_test.UnitTestUPSIM import *


def main():
    test = "cn1_course3_adder"
    FileInterpreter(
        "unit_test/%s/test" % test,
        "",
        Simulation()
    ).parse()


if __name__ == "__main__":
    main()
