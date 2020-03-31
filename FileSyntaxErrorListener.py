from antlr4.error.ErrorListener import *

ERROR_BLOCK_ALREADY_EXISTS: str = \
    "There already exists a block called \"%s\""
ERROR_INVALID_PIN_TYPE: str = \
    "The pin type with this value \"%d\" is not allowed"
ERROR_PIN_ALREADY_EXISTS: str = \
    "The pin \"%s\" already exists in block \"%s\""


class FileSyntaxErrorListener(ErrorListener):
    def __init__(self, output):
        self.output = output

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.output.write(str(line) + ':' + str(column) + " "
                          "ERROR: " + msg + '\n\n')
