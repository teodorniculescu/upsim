from FileInterpreter import FileInterpreter
from Simulation import Simulation


def main():
    test1_fp: str = "test1"
    test_eib_fp: str = "test_error_insert_block"
    file_path: str = "tests/"
    file_path += test1_fp
    file_in = file_path + ".test"
    file_out = file_path + ".result"
    FileInterpreter(file_in, file_out, Simulation()).parse()


if __name__ == "__main__":
    main()