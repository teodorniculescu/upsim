from blocks.BasicBlock import *
from blocks.LogicalBlock import *


class Simulation:
    __logical_blocks: dict
    __state_blocks: dict
    __initial_conditions: list
    __edges: dict

    def __init__(self):
        self.__logical_blocks = {}
        self.__state_blocks = {}
        self.__initial_conditions = []
        self.__edges = {}

    def __read_stage(self):
        block: LogicalBlock
        input_pin: BaseValue
        connected_pin: BaseValue
        input_vertex: str
        connected_vertex: str
        for block in self.__logical_blocks.values():
            for input_pin in block.get_all_pins(PIN_TYPE_INPUT):
                input_vertex = block.get_name() + '.' + input_pin.get_name()
                if input_vertex in self.__edges:
                    connected_vertex = self.__edges[input_vertex]
                    [connected_block_name, connected_pin_name] = connected_vertex.split('.')
                    connected_pin = self.get_block_with_name(connected_block_name).get_pin_with_name(connected_pin_name)
                    connected_pin_value = connected_pin.get_value()
                    if connected_pin_value is not None:
                        input_pin.set_value(connected_pin_value)
                else:
                    print(self.__edges)
                    raise Exception(input_vertex + " is not connected.")

    def __calculate_stage(self):
        block: LogicalBlock
        for block in self.__logical_blocks.values():
            block.calculate()

    def run(self) -> None:
        self.__read_stage()
        self.__calculate_stage()

    def add_logical_block(self, block: BasicBlock) -> None:
        self.__logical_blocks[block.get_name()] = block

    def add_state_block(self, block: BasicBlock) -> None:
        self.__state_blocks[block.get_name()] = block

    def get_block_with_name(self, block_name: str) -> BasicBlock:
        block: BasicBlock
        for block in self.__logical_blocks.values():
            if block.get_name() == block_name:
                return block
        for block in self.__state_blocks.values():
            if block.get_name() == block_name:
                return block
        raise Exception("Block " + block_name + " does not exist.")

    # nodes are of format 'block_name' + '.' + 'pin_name'
    def add_edge(self, node0: str, node1: str) -> None:
        if node0 in self.__edges:
            raise Exception(node0 + " already connected to a pin")
        if node1 in self.__edges:
            raise Exception(node1 + " already connected to a pin")
        self.__edges[node0] = node1
        self.__edges[node1] = node0

    # Adds to a list, a list of tuples (node, value) both of type string
    def add_condition(self, conditions: list):
        self.__initial_conditions.append(conditions)
