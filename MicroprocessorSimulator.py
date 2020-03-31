from FileInterpreter import FileInterpreter
from Simulation import Simulation

TEST_FOLDER_PATH = "tests/"
TEST1_FP: str = "test1"
TEST_EIB_FB: str = "test_error_insert_block"
TEST_FILE_TYPE = ".test"
RESULT_FILE_TYPE = ".result"


def main():
    file_path: str = TEST_FOLDER_PATH
    file_path += TEST_EIB_FB
    file_in = file_path + TEST_FILE_TYPE
    file_out = file_path + RESULT_FILE_TYPE
    FileInterpreter(file_in, file_out, Simulation()).parse()


if __name__ == "__main__":
    main()