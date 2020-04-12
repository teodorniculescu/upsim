from unit_test.UnitTestUPSIM import *


def main():
    test = "insert_block_errors"
    FileInterpreter(
        "unit_test/%s/test" % test,
        "",
        Simulation()
    ).parse()


if __name__ == "__main__":
    main()
