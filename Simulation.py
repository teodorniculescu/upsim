class Simulation:
    __logical_blocks: list
    __state_blocks: list

    def __init__(self):
        self.__logical_blocks = []
        self.__state_blocks = []

    def run(self) -> None:
        pass

    def add_logical_block(self, block) -> None:
        self.__logical_blocks.append(block)

    def add_state_block(self, block) -> None:
        self.__state_blocks.append(block)
