import os
from gen.FileSyntaxLexer import *
from gen.FileSyntaxParser import *
from WrapperFileSyntaxListener import WrapperFileSyntaxListener
from Simulation import Simulation
from FileSyntaxErrorListener import FileSyntaxErrorListener


class FileInterpreter:
    __input_file_path: str
    __sim: Simulation
    " Output file wrapper - handles writing either to a file or to the console "
    __out_fw: type(sys.stdout)

    def __init__(self, input_file_path: str, output_file_path: str,
                 sim: Simulation):
        if not os.path.isfile(input_file_path):
            raise Exception(input_file_path + " is not a valid INPUT file!")
        self.__input_file_path = input_file_path

        if output_file_path == "":
            self.__out_fw = sys.stdout
        else:
            "the w parameter overwrites the content of the output_file_path"

            self.__out_fw = open(output_file_path, "w")

        self.__sim = sim
        self.__sim.add_output_wrapper(self.__out_fw)

    def parse(self):
        input_stream = FileStream(self.__input_file_path)
        lexer = FileSyntaxLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = FileSyntaxParser(stream)
        " Remove and replace error listeners "
        parser.removeErrorListeners()
        error_listener = FileSyntaxErrorListener(self.__out_fw)
        parser.addErrorListener(error_listener)
        " Set the root node of the tree as the 'filesyntax' rule "
        tree = parser.filesyntax()
        """
        Set the wrapper which will utilise the behaviour desired in the
        instructions
        """
        wrapper_file_syntax = WrapperFileSyntaxListener(self.__sim, self.__out_fw)
        walker = ParseTreeWalker()
        walker.walk(wrapper_file_syntax, tree)
        """
        If the output was written to a file, close the file at the end of
        the execution
        """
        if self.__out_fw != sys.stdout:
            self.__out_fw.close()
