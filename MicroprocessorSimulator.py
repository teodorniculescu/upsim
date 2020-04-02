from FileInterpreter import FileInterpreter
from Simulation import Simulation

TEST_FOLDER_PATH: str = "tests/"
TEST_FILE_TYPE: str = ".test"
RESULT_FILE_TYPE: str = ".result"

TEST_LIST: list = [
    "2_and_gates",
    "insert_block_errors",
    "insert_edge_errors",
    "insert_init_cond_errors"
]


def main():
    for test_path in TEST_LIST:
        # Run every test in the "tests" folder
        file_path: str = TEST_FOLDER_PATH
        file_path += test_path
        file_in = file_path + TEST_FILE_TYPE
        file_out = file_path + RESULT_FILE_TYPE
        FileInterpreter(file_in, file_out, Simulation()).parse()


if __name__ == "__main__":
    main()