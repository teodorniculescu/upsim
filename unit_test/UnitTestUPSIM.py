import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# finding the parent directory automatically
from antlr.FileInterpreter import FileInterpreter
from Simulation import Simulation
from typing import Tuple
import unittest
import difflib
import inspect
import timeout_decorator

TEST_FILE: [str] = "test"
RESULT_FILE: [str] = "result"
ANSWER_FILE: [str] = "answer"


class UnitTestUPSIM(unittest.TestCase):
    @staticmethod
    def get_files(test_path: str) -> Tuple[str, str, str]:
        file_path: str = ""
        file_path += test_path + '/'
        test = file_path + TEST_FILE
        result = file_path + RESULT_FILE
        answer = file_path + ANSWER_FILE
        return test, result, answer

    @timeout_decorator.timeout(2)
    def run_test(self) -> None:
        frame = inspect.currentframe()
        # Get frame of penultimate function
        frame = inspect.getouterframes(frame)[2].frame
        test_name = inspect.getframeinfo(frame).function[5:]

        (test, result, answer) = self.get_files(test_name)
        FileInterpreter(test, result, Simulation()).parse()
        file1 = open(result, 'r')
        file2 = open(answer, 'r')
        text1 = file1.readlines()
        text2 = file2.readlines()
        file1.close()
        file2.close()
        dif_result: str = ""
        for line in difflib.unified_diff(text1, text2):
            dif_result += line
        self.assertEqual(dif_result, "")

    def test_and2_gates(self) -> None:
        self.run_test()

    def test_cn1_course3_adder(self) -> None:
        self.run_test()

    def test_insert_block_errors(self) -> None:
        self.run_test()

    def test_insert_edge_errors(self) -> None:
        self.run_test()

    def test_insert_init_cond_errors(self) -> None:
        self.run_test()

    def test_nand_gate_with_8_inputs(self) -> None:
        self.run_test()

    def test_simple_logic_gates(self) -> None:
        self.run_test()

    """
    def test_sr_flip_flop(self) -> None:
        self.run_test()
    """

    def test_simple_logic_gates_n(self) -> None:
        self.run_test()

    def test_not_gate(self) -> None:
        self.run_test()

    def test_jk_flip_flop(self) -> None:
        self.run_test()

    def test_74LS173(self) -> None:
        self.run_test()
