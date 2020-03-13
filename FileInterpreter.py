from antlr4 import *
from gen.FileSyntaxLexer import FileSyntaxLexer
from gen.FileSyntaxParser import FileSyntaxParser
from WrapperFileSyntaxListener import WrapperFileSyntaxListener


class FileInterpreter:
    __file_path: str

    def __init__(self, file_path: str):
        self.__file_path = file_path

    def parse(self):
        input_stream = FileStream(self.__file_path)
        lexer = FileSyntaxLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = FileSyntaxParser(stream)
        # we set the root node of the tree as the 'filesyntax' rule
        tree = parser.filesyntax()

        wrapper_file_syntax = WrapperFileSyntaxListener()
        walker = ParseTreeWalker()
        walker.walk(wrapper_file_syntax, tree)

