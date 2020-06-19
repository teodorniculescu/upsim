from antlr4.error.ErrorListener import *

ERROR_BLOCK_ALREADY_EXISTS: [str] = \
    "1:There already exists a block called \"%s\"."
ERROR_INVALID_PIN_TYPE: [str] = \
    "2:The pin type with this value \"%d\" is not allowed."
ERROR_PIN_ALREADY_EXISTS: [str] = \
    "3:The pin \"%s\" already exists in block \"%s\"."
ERROR_EDGE_BETWEEN_SAME_VERTICES: [str] = \
    "4:Cannot create edge between that starts and ends in the same " \
    "vertex \"%s\"."
ERROR_EDGE_BETWEEN_INPUTS: [str] = \
    "5:Cannot create edge \"%s - %s\" between two input pins."
ERROR_INPUT_VERTEX_EXISTS: [str] = \
    "6:Cannot connect input vertex \"%s\" to specified vertex \"%s\", " \
    "because it is already connected to \"%s\"."
ERROR_NO_INPUT_VERTEX: [str] = \
    "7:Cannot create edge \"%s - %s\" without an input vertex."
ERROR_NO_EXPECTED_ERROR: [str] = \
    "8:Did not receive the expected error %d previously provided."
ERROR_BLOCK_DOESNT_EXIST: [str] = \
    "9:Block \"%s\" does not exist."
ERROR_PIN_DOESNT_EXIST: [str] = \
    "10:Pin \"%s\" does not exist."
ERROR_NODE_DOESNT_EXIST: [str] = \
    "11:Node \"%s\" does not exist."
ERROR_INIT_COND_NOT_STATE_BLOCK: [str] = \
    "12:Initial condition block must be a state block for \"%s\"."
ERROR_INVALID_PIN_VALUE: [str] = \
    "13:Pin cannot have value \"%s\". Pin must have either HIGH \"%d\" or " \
    "LOW \"%d\" values."
ERROR_REQUIRE_CERTAIN_NUM_PINS: [str] = \
    "14:Must have exactly \"%d\" %s pins. Received instead \"%d\" pins."
ERROR_INVALID_BLOCK_NAME: [str] = \
    "15:The block must have a valid name. Name \"%s\" is invalid because its " \
    "type is \"%s\" instead of str."
ERROR_EMPTY_TABLE_DESCRIPTION: [str] = \
    "16:Cannot create a table without at least one column."
ERROR_REQUIRE_AT_LEAST_NUM_PINS: [str] = \
    "17:Must have at least \"%\" %s pins. Received instead \"%d\" pins."
ERROR_POSITION_NOT_SET: [str] = \
    "18:The block position for \"%s\" is not set."
ERROR_CUSTOM_TEMPLATE_DOES_NOT_EXIST: [str] = \
    "19:The template \"%s\" has not been created."
ERROR_EDGE_BETWEEN_OUTPUTS: [str] = \
    "20:Cannot create edge \"%s - %s\" between two output pins."
ERROR_PIN_INVALID_ORIGINAL_POSITION: [str] = \
    "21:The original position for the pin \"%s\" is not set!"
ERROR_INVALID_DIRECTION_STRING: [str] = \
    "22: The provided direction string: \"%s\" is invalid!"
ERROR_GRID_OUT_OF_BOUNDS: [str] = \
    "23: Cannot move node \"%s\" in the \"%s\" direction to because it is " \
    "in the position \"%s\"!"


class FileSyntaxErrorListener(ErrorListener):
    def __init__(self, output):
        self.output = output

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.output.write(msg + '\n\n')
