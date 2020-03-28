from FileInterpreter import FileInterpreter
from Simulation import Simulation


def main():
    file_in = "tests/test1"
    file_out = ""
    FileInterpreter(file_in, file_out, Simulation()).parse()


if __name__ == "__main__":
    main()