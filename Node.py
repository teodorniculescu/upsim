from blocks.BasicBlock import BasicBlock
from values.BaseValue import BaseValue
from BlockHandler import BlockHandler


class Node:
    block_name: str
    pin_name: str
    __bh: BlockHandler

    def __init__(self, node: str, bh: BlockHandler):
        [block_name, pin_name] = node.split('.')
        # TODO raise exception if block name or pin name is empty
        self.block_name = block_name
        self.pin_name = pin_name
        self.__bh = bh

    def get_block(self) -> BasicBlock:
        return self.__bh.get_block_with_name(self.block_name)

    def get_pin(self) -> BaseValue:
        return self.get_block().get_pin_with_name(self.pin_name)

    def __eq__(self, other) -> bool:
        return (self.block_name == other.block_name and
                self.pin_name == other.pin_name)

    def __str__(self) -> str:
        return self.block_name + '.' + self.pin_name

    def __hash__(self) -> int:
        return hash(self.__str__())
