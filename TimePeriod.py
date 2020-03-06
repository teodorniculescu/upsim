from blocks.LogicalBlock import LogicalBlock
from blocks.StateBlock import StateBlock

NONE_MODE: int = 0
NODES_MODE: int = 1
EDGES_MODE: int = 2
INIT_COND_MODE: int = 3

END_STR: str = "end"
NODES_STR: str = "nodes"
EDGES_STR: str = "edges"
INIT_COND_STR: str = "initial_conditions"

STATE_BLOCK_STR: str = "s"
LOGIC_BLOCK_STR: str = "l"

NONE_BLOCK_TYPE: int = 0
STATE_BLOCK_TYPE: int = 1
LOGIC_BLOCK_TYPE: int = 2


class FileInterpreter:
    __block_list: list
    """The number of the line currently read from the file"""
    __line_num: int
    """The word from the line which is currently being parsed"""
    __line_word: str
    __line_word_list: list
    __line_word_num: int
    """The filesystem path to the file"""
    __file_path: str
    """The line from the file which is currently being parsed"""
    __file_line: str
    """Mode of data insert"""
    __mode: int
    __block_type: int

    def __init__(self, file_path: str):
        self.__block_list = []
        self.__line_num = 0
        self.__line_word = ""
        self.__line_word_list = []
        self.__line_word_num = 0
        self.__file_path = file_path
        self.__file_line = ""
        self.__mode = NONE_MODE
        self.__block_type = NONE_BLOCK_TYPE

    def __raise_syntax_exception(self, exception_string: str) -> None:
        raise Exception("line " + str(self.__line_num) + ", word \'" + str(self.__line_word) + "\' " + exception_string)

    def __check_syntax_none_mode(self) -> None:
        switcher: dict = {
            NODES_STR: NODES_MODE,
            EDGES_STR: EDGES_MODE,
            INIT_COND_STR: INIT_COND_MODE
        }
        switcher_result = switcher.get(self.__line_word, None)
        if type(switcher_result) is not int:
            self.__raise_syntax_exception("invalid mode " + self.__line_word)
        self.__mode = switcher_result

    def __check_syntax_nodes_mode(self) -> None:
        if self.__block_type == NONE_BLOCK_TYPE:
            self.__get_block_type()
        else:
            self.__get_block_attributes()

    def __get_state_block_attributes(self) -> None:
        self.__next_word_in_split()
        block = StateBlock(self.__line_word)
        self.__block_list.append(block)

    def __get_logic_block_attributes(self) -> None:
        self.__next_word_in_split()
        block = LogicalBlock(self.__line_word)
        self.__block_list.append(block)

    def __get_block_attributes(self) -> None:
        if self.__block_type == STATE_BLOCK_TYPE:
            self.__get_state_block_attributes()
        elif self.__block_type == LOGIC_BLOCK_TYPE:
            self.__get_logic_block_attributes()
        else:
            self.__raise_syntax_exception("invalid block type " + self.__line_word)

    def __get_block_type(self) -> None:
        if self.__line_word == END_STR:
            self.__mode = NONE_MODE
            return
        switcher: dict = {
            STATE_BLOCK_STR: STATE_BLOCK_TYPE,
            LOGIC_BLOCK_STR: LOGIC_BLOCK_TYPE
        }
        switcher_result = switcher.get(self.__line_word, None)
        if type(switcher_result) is not int:
            self.__raise_syntax_exception("invalid block type " + self.__line_word)
        self.__block_type = switcher_result

    def __check_syntax_edges_mode(self) -> None:
        pass

    def __check_syntax_init_cond_mode(self) -> None:
        pass

    def __init_word_split(self) -> None:
        self.__line_word_list = self.__file_line.split(" ")
        self.__line_word_num = 0
        self.__line_word = self.__line_word_list[0]

    def __next_word_in_split(self) -> None:
        self.__line_word_num += 1
        self.__line_word = self.__line_word_list[self.__line_word_num]

    def __check_syntax(self) -> None:
        self.__init_word_split()
        if type(self.__line_word) is not str:
            self.__raise_syntax_exception("contains non string element")
        elif self.__line_word == "":
            self.__raise_syntax_exception("contains additional whitespaces")
        else:
            switcher: dict = {
                NONE_MODE: self.__check_syntax_none_mode,
                NODES_MODE: self.__check_syntax_nodes_mode,
                EDGES_MODE: self.__check_syntax_edges_mode,
                INIT_COND_MODE: self.__check_syntax_init_cond_mode
            }
            switcher_func = switcher.get(self.__mode, None)
            if not callable(switcher_func):
                self.__raise_syntax_exception("invalid self.mode: " + str(self.__mode))
            switcher_func()

    def parse(self) -> None:
        f = open(self.__file_path, "r")
        self.__line_num = 0
        for self.__file_line in f:
            """Removes newline character from the string end"""
            self.__file_line = self.__file_line[:-1]
            self.__check_syntax()
            self.__line_num = self.__line_num + 1


class InitialConditions:
    def __init__(self):
        pass


class TimePeriod:
    def __init__(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')

    def read(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')

    def calculate(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')

    def write(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')
