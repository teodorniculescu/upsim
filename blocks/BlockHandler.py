from blocks.BasicBlock import BasicBlock
from blocks.CustomBlock import CustomBlockTemplate
from blocks.LogicalBlock import LogicalBlock
from blocks.StateBlock import StateBlock
from values.BaseValue import *
from typing import Dict
from antlr.FileSyntaxErrorListener import ERROR_CUSTOM_TEMPLATE_DOES_NOT_EXIST


class BlockHandler:
    __logical_blocks: Dict[str, BasicBlock]
    __state_blocks: Dict[str, BasicBlock]
    __template_dict: Dict[str, CustomBlockTemplate]

    def __init__(self):
        self.__logical_blocks = {}
        self.__state_blocks = {}
        self.__template_dict = {}

    def get_all_blocks(self) -> Dict[str, BasicBlock]:
        return {**self.__logical_blocks, **self.__state_blocks}

    def get_positionable_blocks(self) -> Dict[str, BasicBlock]:
        result: Dict[str, BasicBlock] = {}
        block: BasicBlock
        for name, block in self.get_all_blocks().items():
            if block.is_positionable():
                result[name] = block
        return result

    def get_logical_blocks(self) -> Dict[str, BasicBlock]:
        return self.__logical_blocks

    def get_state_blocks(self) -> Dict[str, BasicBlock]:
        return self.__state_blocks

    def get_block_with_name(self, block_name: str) -> BasicBlock:
        """
        Searches all types of saved blocks for the one which has the specified
        name
        :param block_name: The name of the block that is searched
        :return: The block with the specified name
        """
        block: BasicBlock
        all_blocks: Dict[str, BasicBlock] = self.get_all_blocks()
        if block_name in all_blocks:
            return all_blocks[block_name]
        raise Exception(ERROR_BLOCK_DOESNT_EXIST % block_name)

    def add_block(self, block: BasicBlock) -> None:
        if block.get_name() in self.get_all_blocks():
            raise Exception(ERROR_BLOCK_ALREADY_EXISTS % block.get_name())
        if isinstance(block, LogicalBlock):
            self.__logical_blocks[block.get_name()] = block
        elif isinstance(block, StateBlock):
            self.__state_blocks[block.get_name()] = block
        else:
            # todo exception for invalid block type
            raise Exception("Invalid block_type " + str(type(block)))

    def get_all_blocks_csv(self) -> str:
        result: str = "Name,Type,Input Pins, Output Pins, IO Pins\n"
        block: BasicBlock
        for block in self.get_all_blocks().values():
            line = ""
            line += block.get_name() + ','
            line += str(type(block).__name__) + ','
            line += block.get_pins_csv(PIN_TYPE_INPUT) + ','
            line += block.get_pins_csv(PIN_TYPE_OUTPUT) + ","
            line += block.get_pins_csv(PIN_TYPE_IO)
            line += '\n'
            result += line
        result += '\n'
        return result

    def create_custom_block_template(self, custom_template: CustomBlockTemplate) -> None:
        self.__template_dict[custom_template.get_name()] = custom_template

    def create_custom_block(self, template_name: str, block_name: str) -> BasicBlock:
        if template_name not in self.__template_dict:
            raise Exception(ERROR_CUSTOM_TEMPLATE_DOES_NOT_EXIST % template_name)
        return self.__template_dict[template_name].generate_custom_block(block_name)

    def show_all_blocks_current_values(self) -> None:
        for block in self.get_all_blocks().values():
            print("\t" + block.get_all_block_current_values())
