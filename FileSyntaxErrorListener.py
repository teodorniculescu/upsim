from antlr4.error.ErrorListener import *

ERROR_BLOCK_ALREADY_EXISTS: str = \
    "1:There already exists a block called \"%s\"."
ERROR_INVALID_PIN_TYPE: str = \
    "2:The pin type with this value \"%d\" is not allowed."
ERROR_PIN_ALREADY_EXISTS: str = \
    "3:The pin \"%s\" already exists in block \"%s\"."
ERROR_EDGE_BETWEEN_SAME_VERTICES: str = \
    "4:Cannot create edge between that starts and ends in the same " \
    "vertex \"%s\"."
ERROR_EDGE_BETWEEN_INPUTS: str = \
    "5:Cannot create edge \"%s - %s\" between two input pins."
ERROR_INPUT_VERTEX_EXISTS: str = \
    "6:Cannot connect input vertex \"%s\" to specified vertex \"%s\", " \
    "because it is already connected to \"%s\"."
ERROR_NO_INPUT_VERTEX: str = \
    "7:Cannot create edge \"%s - %s\" without an input vertex."
ERROR_NO_EXPECTED_ERROR: str = \
    "8:Did not receive the expected error %d previously provided."
ERROR_BLOCK_DOESNT_EXIST: str = \
    "9:Block \"%s\" does not exist."
ERROR_PIN_DOESNT_EXIST: str = \
    "10:Pin \"%s\" does not exist."
ERROR_NODE_DOESNT_EXIST: str = \
    "11:Node \"%s\" does not exist."
ERROR_INIT_COND_NOT_STATE_BLOCK: str = \
    "12:Initial condition block must be a state block for \"%s\"."
ERROR_INVALID_PIN_VALUE: str = \
    "13:Pin cannot have value \"%s\". Pin must have either HIGH \"%d\" or " \
    "LOW \"%d\" values."


class FileSyntaxErrorListener(ErrorListener):
    def __init__(self, output):
        self.output = output

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.output.write(msg + '\n\n')
