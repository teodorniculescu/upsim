from antlr4.error.ErrorListener import *

ERROR_BLOCK_ALREADY_EXISTS: str = \
    "There already exists a block called \"%s\"."
ERROR_INVALID_PIN_TYPE: str = \
    "The pin type with this value \"%d\" is not allowed."
ERROR_PIN_ALREADY_EXISTS: str = \
    "The pin \"%s\" already exists in block \"%s\"."
ERROR_EDGE_BETWEEN_SAME_VERTICES: str = \
    "Cannot create edge between that starts and ends in the same vertex \"%s\"."
ERROR_EDGE_BETWEEN_INPUTS: str = \
    "Cannot create edge \"%s - %s\" between two input pins."
ERROR_INPUT_VERTEX_EXISTS: str = \
    "Cannot connect input vertex \"%s\" to specified vertex \"%s\", because " \
    "it is already connected to \"%s\"."
ERROR_NO_INPUT_VERTEX: str = \
    "Cannot create edge \"%s - %s\" without an input vertex."


class FileSyntaxErrorListener(ErrorListener):
    def __init__(self, output):
        self.output = output

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.output.write(str(line) + ':' + str(column) + " "
                          "ERROR: " + msg + '\n\n')
