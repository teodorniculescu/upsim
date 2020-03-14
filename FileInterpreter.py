from antlr4 import *
from gen.FileSyntaxLexer import FileSyntaxLexer
from gen.FileSyntaxParser import FileSyntaxParser
from WrapperFileSyntaxListener import WrapperFileSyntaxListener
from Simulation import Simulation


class FileInterpreter:
    __file_path: str
    __sim: Simulation

    def __init__(self, file_path: str, sim: Simulation):
        self.__file_path = file_path
        self.__sim = sim

    def parse(self):
        input_stream = FileStream(self.__file_path)
        lexer = FileSyntaxLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = FileSyntaxParser(stream)
        # we set the root node of the tree as the 'filesyntax' rule
        tree = parser.filesyntax()

        wrapper_file_syntax = WrapperFileSyntaxListener(self.__sim)
        walker = ParseTreeWalker()
        walker.walk(wrapper_file_syntax, tree)

