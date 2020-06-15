from blocks.LogicalBlock import LogicalBlock
from blocks.BasicBlock import BasicBlock
from values.BaseValue import BaseValue
from typing import List, Tuple


class CustomBlockTemplate:
    __name: str
    __blocks: List[BasicBlock]
    __edges: List[Tuple[str, str]]
    __input_pins: List[str]
    __output_pins: List[str]

    def __init__(self, name: str):
        self.__name = name
        self.__blocks = []
        self.__edges = []
        self.__input_pins = []
        self.__output_pins = []

    def get_name(self) -> str:
        return self.__name

    def add_blocks(self, block_list: List[BasicBlock]) -> None:
        self.__blocks += block_list

    def add_edges(self, edge_list: List[Tuple[str, str]]) -> None:
        self.__edges += edge_list

    def add_input_pins(self, pin_list: List[str]) -> None:
        self.__input_pins += pin_list

    def add_output_pins(self, pin_list: List[str]) -> None:
        self.__output_pins += pin_list


class CustomBlock(LogicalBlock):
    def __init__(self, name: str):
        super().__init__(name)

    def calculate(self) -> None:
        pass

