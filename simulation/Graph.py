from blocks.BasicBlock import BasicBlock
from blocks.StateBlock import StateBlock
from values.BaseValue import *
from simulation.Node import Node
from blocks.BlockHandler import BlockHandler
from antlr.FileSyntaxErrorListener import *
from database.DBController import Column, Row
from typing import List, Dict, Tuple



class Graph:
    __bh: BlockHandler
    " A dictionary of str:Node where the string is block_name.pin_name "
    __nodes: Dict[str, Node]
    " A dictionary of Node:Node "
    __edges: Dict[str, Dict[str, None]]

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
            # store the new node in the nodes dictionary
            self.__nodes[name] = Node(name, self.__bh)
            # add an empty dictionary for the edges connected to this node
            self.__edges[name] = {}

    def get_node(self, node_name: str) -> Node:
        if node_name in self.__nodes:
            return self.__nodes[node_name]
        [block_name, pin_name] = node_name.split(".")
        # tries to get the block name and the pin name
        # if it succeeds, it means that the block and pin exist
        self.__bh.get_block_with_name(block_name).get_pin_with_name(pin_name)
        # which means the node has not been declared
        raise Exception(ERROR_NODE_DOESNT_EXIST % node_name)

    def get_edges(self) -> Dict[str, Dict[str, None]]:
        return self.__edges

    def add_edge(self, node0_name: str, node1_name: str) -> None:
        """
        Adds a new edge comprised of two vertices / nodes
        Nodes must be of format 'block name' + '.' + 'pin name'
        :param node0_name: First vertex
        :param node1_name: Second vertex
        :return: None
        """
        if node0_name == node1_name:
            raise Exception(ERROR_EDGE_BETWEEN_SAME_VERTICES % node0_name)
        # Get pin types
        node0_type: int = self.get_node(node0_name).get_pin().get_pin_type()
        node1_type: int = self.get_node(node1_name).get_pin().get_pin_type()
        if node0_type == PIN_TYPE_INPUT and node1_type == PIN_TYPE_INPUT:
            raise Exception(ERROR_EDGE_BETWEEN_INPUTS % (node0_name, node1_name))
        if node0_type == PIN_TYPE_OUTPUT and node1_type == PIN_TYPE_OUTPUT:
            raise Exception(ERROR_EDGE_BETWEEN_OUTPUTS % (node0_name, node1_name))
        if node0_name in self.__edges[node1_name] or node1_name in self.__edges[node0_name]:
            raise Exception(ERROR_INPUT_VERTEX_EXISTS
                            % (node0_name, node1_name, self.__edges[node0_name]))
        self.__edges[node0_name][node1_name] = None
        self.__edges[node1_name][node0_name] = None

    def get_all_edges_csv(self) -> str:
        result: str = "From,From Type,To,To Type\n"
        from_vertex_name: str
        to_vertex_name: str
        to_vertex_dict: Dict[str, None]
        unique_vertex_dict: Dict[Tuple[str, str], None] = {}
        for from_vertex_name, to_vertex_dict in self.__edges.items():
            for to_vertex_name in to_vertex_dict.keys():
                if from_vertex_name < to_vertex_name:
                    small_string: str = from_vertex_name
                    big_string: str = to_vertex_name
                else:
                    big_string: str = from_vertex_name
                    small_string: str = to_vertex_name
                key = (small_string, big_string)
                unique_vertex_dict[key] = None

        for (from_vertex_name, to_vertex_name) in unique_vertex_dict.keys():
            from_type: str = self.get_node(from_vertex_name).get_pin().get_pin_type_str()
            to_type: str = self.get_node(to_vertex_name).get_pin().get_pin_type_str()
            result += (from_vertex_name + ',' + from_type + ',' +
                       to_vertex_name + ',' + to_type + '\n')
        return result

    def set_vertex_value(self, vertex_name: str, vertex_value: int) -> None:
        self.get_node(vertex_name).get_pin().set_value(vertex_value)

    def calculate_values_block(self, block_name: str) -> List[str]:
        result: List[str] = []
        block: BasicBlock = self.__bh.get_block_with_name(block_name)
        old_outputs: Dict[str, str] = block.get_output_values()
        block.calculate()
        new_outputs: Dict[str, str] = block.get_output_values()
        key: str
        value: str
        for key, value in old_outputs.items():
            # only push to stack if the newly calculate value is different
            # from the previous one
            if new_outputs[key] != value:
                node_name = block_name + "." + key
                result.append(node_name)
        return result


    def propagate_values_block(self, node_name: str) -> List[str]:
        result: List[str] = []
        # get the node that propagates
        this_node = self.get_node(node_name)
        # get the value that must be propagated
        pin_value = this_node.get_pin().get_value()
        connected_node_name: str
        for connected_node_name in self.__edges[node_name].keys():
            # get the node connected to this one
            connected_node: Node = self.__nodes[connected_node_name]
            # get the old value
            if connected_node.get_pin().get_value_is_set() == False:
                old_value = None
            else:
                old_value = connected_node.get_pin().get_value()
            # change the value of the connected node with the one that is propagated
            connected_node.get_pin().set_value(pin_value)
            # add the block to the execution stack if the value is new
            if type(connected_node.get_block()) != StateBlock and pin_value != old_value:
                # the block is added instead of the node because the it
                # will be executed in the following step
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

