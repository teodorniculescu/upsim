from blocks.BasicBlock import BasicBlock
from values.BaseValue import *
from Node import Node
from BlockHandler import BlockHandler
from FileSyntaxErrorListener import *
from DBController import Column, Row
from typing import List, Dict


class Graph:
    __bh: BlockHandler
    " A dictionary of str:Node where the string is block_name.pin_name "
    __nodes: Dict[str, Node]
    " A dictionary of Node:Node "
    __edges: Dict[str, str]

    def __init__(self, bh):
        self.__bh = bh
        self.__nodes = {}
        self.__edges = {}

    def add_nodes(self, block: BasicBlock) -> None:
        pin: BaseValue
        for pin in block.get_all_pins().values():
            name: str = block.get_name() + '.' + pin.get_name()
            if name in self.__nodes:
                # todo exception for when a node exists multiple times
                raise Exception("wot")
            self.__nodes[name] = Node(name, self.__bh)

    def get_node(self, node_name: str) -> Node:
        if node_name in self.__nodes:
            return self.__nodes[node_name]
        raise Exception(ERROR_NODE_DOESNT_EXIST % node_name)

    def get_edges(self) -> Dict[str, str]:
        return self.__edges

    def get_node_connected_to_node(self, node_name: str) -> Node:
        connected_node_name = self.__edges[node_name]
        return self.__nodes[connected_node_name]

    def add_edge(self, node0_name: str, node1_name: str) -> None:
        """
        Adds a new edge comprised of two vertices / nodes
        Nodes must be of format 'block name' + '.' + 'pin name'
        :param node0_name: First vertex
        :param node1_name: Second vertex
        :return: None
        """
        if node0_name == node1_name:
            raise Exception(ERROR_EDGE_BETWEEN_SAME_VERTICES % node0)
        # Get pin types
        node0_type: int = self.get_node(node0_name).get_pin().get_pin_type()
        node1_type: int = self.get_node(node1_name).get_pin().get_pin_type()
        if node0_type == PIN_TYPE_INPUT:
            if node1_type == PIN_TYPE_INPUT:
                raise Exception(ERROR_EDGE_BETWEEN_INPUTS % (node0_name, node1_name))
            if node0_name in self.__edges:
                raise Exception(ERROR_INPUT_VERTEX_EXISTS
                                % (node0_name, node1_name, self.__edges[node0_name]))
            self.__edges[node1_name] = node0_name
        elif node1_type == PIN_TYPE_INPUT:
            if node1_name in self.__edges:
                raise Exception(ERROR_INPUT_VERTEX_EXISTS
                                % (node1_name, node0_name, self.__edges[node1_name]))
            self.__edges[node0_name] = node1_name
        else:
            raise Exception(ERROR_NO_INPUT_VERTEX % (node0_name, node1_name))
            print("Created edge between " + node0_name + " and " + node1_name)

    def get_all_edges_csv(self) -> str:
        result: str = "From,From Type,To,To Type\n"
        from_vertex_name: str
        to_vertex_name: str
        for from_vertex_name, to_vertex_name in self.__edges.items():
            from_type: str = self.get_node(from_vertex_name).get_pin().get_pin_type_str()
            to_type: str = self._get_node(to_vertex_name).get_pin().get_pin_type_str()
            result += (from_vertex_name + ',' + from_type + ',' +
                       to_vertex_name + ',' + to_type + '\n')
        return result

    def set_vertex_value(self, vertex_name: str, vertex_value: int) -> None:
        self.get_node(vertex_name).get_pin().set_value(vertex_value)

    def calculate_values_block(self, block_name: str) -> None:
        self.__bh.get_block_with_name(block_name).calculate()

    def propagate_values_block(self, block_name: str) -> List[str]:
        result: List[str] = []
        pin: BaseValue
        for pin in self.__bh.get_block_with_name(block_name).get_all_pins_with_type(PIN_TYPE_OUTPUT).values():
            # obtain the node name
            node_name: str = block_name + "." + pin.get_name()
            # get the node connected to this one
            connected_node: Node = self.get_node_connected_to_node(node_name)
            # get the value that must be propagated
            pin_value = pin.get_value()
            # change the value of the connected node with the one that is propagated
            connected_node.get_pin().set_value(pin_value)
            result.append(connected_node.get_block().get_name())
        return result

    def get_vertex_column_descriptions(self) -> List[Column]:
        result: List[Column] = []
        block: BasicBlock
        for block in self.__bh.get_all_blocks().values():
            result += block.get_vertex_column_descriptions()
        return result

    def get_vertex_values(self) -> Row:
        result: Row = Row()
        block: BasicBlock
        for block in self.__bh.get_all_blocks().values():
            result += block.get_vertex_values()
        return result

