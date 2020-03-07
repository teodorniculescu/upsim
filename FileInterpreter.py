from blocks.StateBlock import StateBlock

FI_INSERT = "INSERT"
FI_BLOCKS = "BLOCKS"
FI_EDGES = "EDGES"
FI_INIT_COND = "INITIAL_CONDITIONS"
FI_STATE = "STATE"
FI_AND2 = "AND2"


class FileInterpreter:
    __file_path: str
    __file_line: str
    __line_word_list: list
    __line_word: str
    __line_num: int
    __cmd_tokens_list: list
    __token_num: int
    __token_word: str

    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__line_num = 0

    def __parse_state_block(self) -> None:
        self.__next_cmd_token()
        name = self.__token_word
        self.__next_cmd_token()
        pin_name = self.__token_word
        block = StateBlock(name)

    def __parse_and2_block(self) -> None:
        self.__next_cmd_token()
        name = self.__token_word
        self.__next_cmd_token()
        input_pin0_name = self.__token_word
        self.__next_cmd_token()
        input_pin1_name = self.__token_word
        self.__next_cmd_token()
        output_pin_name = self.__token_word

    def __insert_blocks(self) -> None:
        """Parse each Block from the insert"""
        while not self.__end_cmd_tokens():
            self.__next_cmd_token()
            switcher = {
                FI_STATE: self.__parse_state_block,
                FI_AND2: self.__parse_and2_block
            }
            self.__switch_call(switcher)

    def __insert_edges(self) -> None:
        #TODO
        raise Exception("TODO")

    def __insert_init_cond(self) -> None:
        #TODO
        raise Exception("TODO")

    def __insert_data(self) -> None:
        self.__next_cmd_token()
        switcher = {
            FI_BLOCKS: self.__insert_blocks,
            FI_EDGES: self.__insert_edges,
            FI_INIT_COND: self.__insert_init_cond
        }
        self.__switch_call(switcher)

    def __switch_call(self, switcher: dict) -> None:
        func = switcher.get(self.__token_word, None)
        if not callable(func):
            raise Exception("line " + str(self.__line_num) + ": " + "invalid parse " + self.__token_word)
        func()

    def __execute_cmd(self) -> None:
        self.__init_cmd_tokens()
        switcher = {
            FI_INSERT: self.__insert_data
        }
        self.__switch_call(switcher)

    def __end_cmd_tokens(self) -> bool:
        if self.__token_num == len(self.__cmd_tokens_list):
            return True
        return False

    def __init_cmd_tokens(self) -> None:
        self.__token_num = 0
        if len(self.__cmd_tokens_list) == 0:
            raise Exception("token list is empty")
        self.__token_word = self.__cmd_tokens_list[self.__token_num]

    def __next_cmd_token(self) -> None:
        self.__token_num += 1
        if len(self.__cmd_tokens_list) < self.__token_num:
            raise Exception("out of bounds token list")
        self.__token_word = self.__cmd_tokens_list[self.__token_num]

    def parse(self) -> None:
        execute_cmd = False
        f = open(self.__file_path, "r")
        for self.__file_line in f:
            self.__line_word_list = self.__file_line.split()
            for self.__line_word in self.__line_word_list:
                if self.__line_word[-1] == ";":
                    self.__line_word = self.__line_word[:-1]
                    execute_cmd = True
                self.__cmd_tokens_list.append(self.__line_word)
                if execute_cmd is True:
                    self.__execute_cmd()
                    self.__cmd_tokens_list = []
            self.__line_num = self.__line_num + 1


