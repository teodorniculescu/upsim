import sys
from antlr4 import *
from gen.FileSyntaxLexer import FileSyntaxLexer
from gen.FileSyntaxParser import FileSyntaxParser
from WrapperFileSyntaxListener import WrapperFileSyntaxListener
from Simulation import Simulation


class FileInterpreter:
    __input_file_path: str
    __output_file_path: str
    __sim: Simulation
    __output: type(sys.stdout)

    def __init__(self, input_file_path: str, output_file_path: str, sim: Simulation):
        self.__input_file_path = input_file_path

        # If the output file path is not specified, write to stdout
        if output_file_path == "":
            self.__output = sys.stdout
        else:
            self.__output = open(output_file_path)

        self.__output_file_path = output_file_path
        self.__sim = sim

    def parse(self):
        input_stream = FileStream(self.__input_file_path)
        lexer = FileSyntaxLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = FileSyntaxParser(stream)

        # Set the root node of the tree as the 'filesyntax' rule.
        tree = parser.filesyntax()

        # Set the wrapper which will utilise the behaviour desired in the instructions.
        wrapper_file_syntax = WrapperFileSyntaxListener(self.__sim, self.__output)
        walker = ParseTreeWalker()
        walker.walk(wrapper_file_syntax, tree)

        # If the output was written to a file, close the file at the end of the execution.
        if self.__output != sys.stdout:
            self.__output.close()

