from blocks.LogicalBlock import LogicalBlock
from blocks.BasicBlock import BasicBlock
from values.BaseValue import BaseValue, PIN_TYPE_INPUT, PIN_TYPE_OUTPUT
from typing import List, Tuple
import simulation.Simulation


class CustomBlock(LogicalBlock):
    def __init__(self,
                 block_name: str,
                 input_names: List[str],
                 output_names: List[str],
                 ):
        super().__init__(name=block_name)
        for input_name in input_names:
            self.add_pin(BaseValue(input_name, PIN_TYPE_INPUT))
        for output_name in output_names:
            self.add_pin(BaseValue(output_name, PIN_TYPE_OUTPUT))


    def calculate(self) -> None:
        pass


class CustomBlockTemplate:
    __name: str
    __blocks: List[BasicBlock]
    __edges: List[Tuple[str, str]]
    __input_names: List[str]
    __output_names: List[str]

    def __init__(self, name: str):
        self.__name = name
        self.__blocks = []
        self.__edges = []
        self.__input_names = []
        self.__output_names = []

    def get_name(self) -> str:
        return self.__name

    def add_blocks(self, block_list: List[BasicBlock]) -> None:
        self.__blocks += block_list

    def add_edges(self, edge_list: List[Tuple[str, str]]) -> None:
        self.__edges += edge_list

    def add_input_pins(self, pin_list: List[str]) -> None:
        self.__input_names += pin_list

    def add_output_pins(self, pin_list: List[str]) -> None:
        self.__output_names += pin_list

    def generate_custom_function(self, block_name: str) -> CustomBlock:
        return CustomBlock(
            block_name=block_name,
            input_names=self.__input_names,
            output_names=self.__output_names,
            original_blocks=self.__blocks,
            original_edges=self.__edges
        )
