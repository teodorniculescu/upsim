from FileInterpreter import FileInterpreter
from Simulation import Simulation

TEST_FOLDER_PATH: str = "tests/"
TEST_FILE_TYPE: str = ".test"
RESULT_FILE_TYPE: str = ".result"

TEST1: str = "test1"
TEST_ERRORS1: str = "test_errors1"
TEST_ERRORS2: str = "test_errors2"


def main():
    file_path: str = TEST_FOLDER_PATH
    file_path += TEST_ERRORS2
    file_in = file_path + TEST_FILE_TYPE
    file_out = file_path + RESULT_FILE_TYPE
    FileInterpreter(file_in, file_out, Simulation()).parse()


if __name__ == "__main__":
    main()