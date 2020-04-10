from FileInterpreter import FileInterpreter
from Simulation import Simulation

TEST_FOLDER_PATH: str = "tests/"
TEST_FILE_TYPE: str = ".test"
RESULT_FILE_TYPE: str = ".result"
ANSWER_FILE_TYPE: str = ".answer"

TEST_LIST: list = [
    "2_and_gates",
    "insert_block_errors",
    "insert_edge_errors",
    "insert_init_cond_errors"
]


def main():
    output_file_type: str
    print("What would you like to generate: answers / results")
    # input1 = input()
    input1 = "results"
    if input1 == "answers":
        print("Are you sure? This will override all previous answers! Type: \"Yes I am sure!\"")
        input1 = input()
        if input1 == "Yes I am sure!":
            output_file_type = ANSWER_FILE_TYPE
        else:
            print("Abort!")
            return
    elif input1 == "results":
        output_file_type = RESULT_FILE_TYPE
    else:
        raise Exception("Invalid cmd")

    for test_path in TEST_LIST:
        # Run every test in the "tests" folder
        file_path: str = TEST_FOLDER_PATH
        file_path += test_path
        file_in = file_path + TEST_FILE_TYPE
        file_out = file_path + output_file_type
        FileInterpreter(file_in, file_out, Simulation()).parse()

    if output_file_type == RESULT_FILE_TYPE:
        print("Comparing files!")
        import difflib
        for test_path in TEST_LIST:
            # Run every test in the "tests" folder
            file_path: str = TEST_FOLDER_PATH
            file_path += test_path
            result_file = file_path + RESULT_FILE_TYPE
            answer_file = file_path + ANSWER_FILE_TYPE

            result: str = ""
            result += test_path + "\n"
            t1 = open(result_file).readlines()
            t2 = open(answer_file).readlines()
            for line in difflib.unified_diff(t1, t2):
                result += line
            print(result)


if __name__ == "__main__":
    main()