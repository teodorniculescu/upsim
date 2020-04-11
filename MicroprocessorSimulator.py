from FileInterpreter import FileInterpreter
from Simulation import Simulation

TEST_FOLDER_PATH: str = "unit_test/"
TEST_FILE: str = "test"
RESULT_FILE: str = "result"
ANSWER_FILE: str = "answer"

TEST_LIST: list = [
    "and2_gates",
    "insert_block_errors",
    "insert_edge_errors",
    "insert_init_cond_errors",
    "simple_logic_gates"
]


def main():
    output_file: str
    print("What would you like to generate: answers / test / results")
    # input1 = input()
    input1 = "test"
    if input1 == "answers":
        print("Are you sure? This will override all previous answers! Type: \"Yes I am sure!\"")
        input1 = input()
        if input1 == "Yes I am sure!":
            output_file = ANSWER_FILE
        else:
            print("Abort!")
            return
    elif input1 == "results" or input1 == "test":
        output_file = RESULT_FILE
    else:
        raise Exception("Invalid cmd")

    for test_path in TEST_LIST:
        # Run every test in the "unit_test" folder
        file_path: str = TEST_FOLDER_PATH
        file_path += test_path + '/'
        file_in = file_path + TEST_FILE
        file_out = file_path + output_file
        print("Running " + test_path)
        FileInterpreter(file_in, file_out, Simulation()).parse()

    if input1 == "results":
        print("Comparing files!")
        import difflib
        for test_path in TEST_LIST:
            # Run every test in the "unit_test" folder
            file_path: str = TEST_FOLDER_PATH
            file_path += test_path + '/'
            result_file = file_path + RESULT_FILE
            answer_file = file_path + ANSWER_FILE

            result: str = ""
            t1 = open(result_file).readlines()
            t2 = open(answer_file).readlines()
            for line in difflib.unified_diff(t1, t2):
                result += line
            if result == "":
                result += "OK - "
                result += test_path
            else:
                result = "FAILED - " + test_path + '\n' + result
            print(result)


if __name__ == "__main__":
    main()