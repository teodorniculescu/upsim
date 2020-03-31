from antlr4.error.ErrorListener import *


class FileSyntaxErrorListener(ErrorListener):
    def __init__(self, output):
        self.output = output

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.output.write(str(line) + ':' + str(column) + ': ' + msg + '\n')
