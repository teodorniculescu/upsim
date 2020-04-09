from blocks.BasicBlock import BasicBlock
from values.BaseValue import *
from Node import Node
from BlockHandler import BlockHandler
from FileSyntaxErrorListener import *


class Graph:
    __bh: BlockHandler
    " A dictionary of str:Node where the string is block_name.pin_name "
    __nodes: dict
    " A dictionary of Node:Node "
    __edges: dict

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

    def get_node(self, name: str) -> Node:
        if name in self.__nodes:
            return self.__nodes[name]
        block_name: str
        pin_name: str
        [block_name, pin_name] = name.split('.')
        self.__bh.get_block_with_name(block_name).get_pin_with_name(pin_name)
        raise Exception(ERROR_NODE_DOESNT_EXIST % name)

    def get_edges(self) -> dict:
        return self.__edges

    def add_edge(self, node0_name: str, node1_name: str) -> None:
        """
        Adds a new edge comprised of two vertices / nodes
        Nodes must be of format 'block name' + '.' + 'pin name'
        :param node0_name: First vertex
        :param node1_name: Second vertex
        :return: None
        """
        node0: Node = self.get_node(node0_name)
        node1: Node = self.get_node(node1_name)
        if node0 == node1:
            raise Exception(ERROR_EDGE_BETWEEN_SAME_VERTICES % node0)
        # Get pin types
        node0_type: int = node0.get_pin().get_pin_type()
        node1_type: int = node1.get_pin().get_pin_type()
        if node0_type == PIN_TYPE_INPUT:
            if node1_type == PIN_TYPE_INPUT:
                raise Exception(ERROR_EDGE_BETWEEN_INPUTS % (node0, node1))
            if node0 in self.__edges:
                raise Exception(ERROR_INPUT_VERTEX_EXISTS
                                % (node0, node1, self.__edges[node0]))
            self.__edges[node0] = node1
        elif node1_type == PIN_TYPE_INPUT:
            if node1 in self.__edges:
                raise Exception(ERROR_INPUT_VERTEX_EXISTS
                                % (node1, node0, self.__edges[node1]))
            self.__edges[node1] = node0
        else:
            raise Exception(ERROR_NO_INPUT_VERTEX % (node0, node1))

    def get_all_edges_csv(self) -> str:
        result: str = "From,From Type,To,To Type\n"
        from_vertex: Node
        to_vertex: Node
        for from_vertex, to_vertex in self.__edges.items():
            from_type: str = from_vertex.get_pin().get_pin_type_str()
            to_type: str = to_vertex.get_pin().get_pin_type_str()
            result += (str(from_vertex) + ',' + from_type + ',' +
                       str(to_vertex) + ',' + to_type + '\n')
        return result

    def set_vertex_value(self, vertex_name: str, vertex_value: int) -> None:
        self.get_node(vertex_name).get_pin().set_value(vertex_value)

    def get_all_vertex_names_csv(self) -> str:
        result: str = ""
        block: BasicBlock
        for block in self.__bh.get_all_blocks().values():
            result += block.get_vertex_names_csv()
        return result

    def get_all_vertex_values_csv(self) -> str:
        result: str = ""
        block: BasicBlock
        for block in self.__bh.get_all_blocks().values():
            result += block.get_vertex_values_csv()
        return result


