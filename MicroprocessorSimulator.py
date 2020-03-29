from FileInterpreter import FileInterpreter
from Simulation import Simulation


def main():
    file_in = "tests/test1.test"
    file_out = "tests/test1.result"
    FileInterpreter(file_in, file_out, Simulation()).parse()


if __name__ == "__main__":
    main()