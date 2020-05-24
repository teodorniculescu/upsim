from blocks.BasicBlock import *
from blocks.LogicalBlock import *
from blocks.StateBlock import *
from gen.FileSyntaxParser import *
from FileSyntaxErrorListener import *
from BlockHandler import *
from Node import Node
import sys
from Graph import Graph
from typing import Dict, List, Tuple
from DBController import *
from datetime import datetime
from random import random

PROPAGATE_CMD: Final[str] = "prop"
CALCULATE_CMD: Final[str] = "calc"


class Simulation:
    __bh: BlockHandler
    " A list of dictionaries "
    __initial_conditions: List[Dict]
    __number_init_cond: int
    __ic: dict
    __changed_state: bool
    " Output wrapper which is by default stdout but can be replaced by a file "
    __out_fw: type(sys.stdout)
    " The number of times show stage state was called "
    __num_sss: int
    __graph: Graph
    __dbc: DBController
    table_name: str
    # A stack which contains tuples of 1. the block name 2. if the block should calculate its value or propagate it
    __execution_stack: List[Tuple[str, str]]

    def __init__(self):
        self.__execution_stack = []
        self.__bh = BlockHandler()
        self.__initial_conditions = []
        self.__number_init_cond = 0
        self.__ic = {}
        self.__out_fw = sys.stdout
        self.__num_sss = 0
        self.__graph = Graph(self.__bh)
        self.__dbc = DBController()
        self.table_name = \
            "run_" + \
            datetime.now().strftime("%d%m%Y_%H%M%S_") + \
            str(int(random() * 1000000))

    def __read_stage(self) -> None:
        block: LogicalBlock
        for block in self.__bh.get_all_blocks().values():
            input_pin: BaseValue
            for input_pin in block.get_all_pins_with_type(PIN_TYPE_INPUT).values():
                input_vertex: Node =\
                    self.__graph.get_node(block.get_name() + '.' + input_pin.get_name())
                if input_vertex in self.__graph.get_edges():
                    connected_vertex: Node = self.__graph.get_edges()[input_vertex]
                    connected_pin: BaseValue = connected_vertex.get_pin()
                    if connected_pin.is_set():
                        input_pin.set_value(connected_pin.get_value())
                        if input_pin.changed_state_from_last_time_step():
                            self.__changed_state = True
                else:
                    # todo create exception for when a input vertex is not connected
                    raise Exception(str(input_vertex) + " is not connected.")

    def __calculate_stage(self) -> None:
        block: LogicalBlock
        for block in self.__bh.get_logical_blocks().values():
            block.calculate()
            if block.output_changed_state():
                self.__changed_state = True

    def __init_stage(self) -> None:
        if self.__finished_all_init_cond():
            raise Exception("Exceeded length of __initial_conditions.")
        ic_curr: dict = self.__initial_conditions[self.__number_init_cond]
        self.__ic = {**self.__ic, **ic_curr}
        " now __ic contains the initial conditions of this current time frame "
        block: BasicBlock
        for block in self.__bh.get_all_blocks().values():
            block.reset()
        vertex_name: str
        vertex_value_str: str
        for vertex_name, vertex_value_str in self.__ic.items():
            vertex_value: int = int(vertex_value_str)
            # todo exception if the vertex value is invalid
            self.__graph.set_vertex_value(vertex_name, vertex_value)
        " continue to the next initial condition "
        self.__number_init_cond += 1

    def __finished_all_init_cond(self) -> bool:
        if self.__number_init_cond >= len(self.__initial_conditions):
            return True
        return False

    def __has_simulation_changed_state(self) -> bool:
        return self.__changed_state

    def get_run_table_description(self) -> TableDescription:
        column_list: List[Column] = [
            Column("ICN", "INT"),
            Column("SSN", "INT")
        ]
        column_list += self.__graph.get_vertex_column_descriptions()
        return TableDescription(column_list)

    def get_run_line(self) -> Row:
        row: Row = Row()
        row.append(str(self.__number_init_cond))
        row.append(str(self.__num_sss))
        row += self.__graph.get_vertex_values()
        return row


    def __setup_run(self) -> None:
        self.__dbc.create_table(
            self.table_name,
            self.get_run_table_description()
        )
        # reset all values - set as 0 and uninitialised
        block: BasicBlock
        for block in self.__bh.get_all_blocks().values():
            block.reset()

    def __setup_init_cond(self) -> None:
        # Get current initial condition
        current_init_cont: dict = self.__initial_conditions[self.__number_init_cond]
        # setup the values of the respective pins according to the initial conditions
        vertex_name: str
        vertex_value_str: str
        for vertex_name, vertex_value_str in current_init_cont.items():
            # obtains the integer value from the stored string
            vertex_value: int = int(vertex_value_str)
            # TODO exception if the vertex value is invalid
            # sets the value to the appropriate pin
            self.__graph.set_vertex_value(vertex_name, vertex_value)
            # set new stack value
            stack_value: Tuple[str, str] = \
                (self.__graph.get_node(vertex_name).get_block().get_name(),
                 PROPAGATE_CMD)
            # setup execution stack
            self.__execution_stack.append(stack_value)

        # increment initial condition counter
        self.__number_init_cond += 1
        # Used for showing the number of times the stage state was displayed
        self.__num_sss = 0
        # Shows the state after initializing with the initial conditions
        self.__dbc.insert_row(self.table_name, self.get_run_line())

    def __execution_stack_is_empty(self) -> bool:
        return len(self.__execution_stack) == 0

    def __propagate(self, block_name: str) -> None:
        propagated_blocks_list: List[str] = self.__graph.propagate_values_block(block_name)
        for prop_name in propagated_blocks_list:
            self.__execution_stack.append((prop_name, CALCULATE_CMD))

    def __calculate(self, block_name: str) -> None:
        self.__graph.calculate_values_block(block_name)

    def run(self) -> None:
        """
        Creates a CSV with the following fields:
        - Initial Condition Number - ICN
        - State Stage Num - SSN
        - The names of each pin from the schematic
        :return: None
        """

        self.__setup_run()
        while not self.__finished_all_init_cond():
            self.__setup_init_cond()
            while not self.__execution_stack_is_empty():
                # increment the number of steps the initial conditions took to completion
                self.__num_sss += 1
                # pop execution stack
                (block, cmd) = self.__execution_stack.pop()
                # TODO propagate or calculate
                if cmd == PROPAGATE_CMD:
                    self.__propagate(block)
                elif cmd == CALCULATE_CMD:
                    self.__calculate(block)
                else:
                    # TODO Create exception for undefined cmd from execution stack
                    raise Exception("UNDEFINED")
                # TODO push execution stack
                # show circuit state, which means inserting a value in the table
                self.__dbc.insert_row(self.table_name, self.get_run_line())
        self.__dbc.commit()

    def display(self, description: Tuple[str], values: List[Tuple]) -> None:
        self.write(str(description) + "\n")
        for line in values:
            self.write(str(line) + "\n")

    def show_run_select_all(self) -> None:
        description = self.__dbc.describe_table(self.table_name)
        names: Tuple[str] = tuple()
        for line in description:
            names += (line[0], )
        values = self.__dbc.select_all_from_table(self.table_name)
        self.display(names, values)

    def show_run_select_some(self, columns: List[str]) -> None:
        values = self.__dbc.select_some_from_table(
            self.table_name,
            columns
        )
        self.display(tuple(columns), values)

    def add_block(self, block: BasicBlock) -> None:
        self.__bh.add_block(block)
        self.__graph.add_nodes(block)

    def add_edge(self, node0_name: str, node1_name: str) -> None:
        self.__graph.add_edge(node0_name, node1_name)

    def add_condition(self, conditions: dict) -> None:
        """
        Adds to the list of initial conditions a new dictionary of conditions
        :param conditions: A dictionary containing {key - the vertex name :
        value - the vertex value}
        :return: None
        """
        node_name: str
        value: str
        for node_name, value in conditions.items():
            if (not isinstance(self.__graph.get_node(node_name).get_block(),
                               StateBlock)):
                raise Exception(ERROR_INIT_COND_NOT_STATE_BLOCK % node_name)
            x: int = int(value)
            if x != HIGH and x != LOW:
                raise Exception(ERROR_INVALID_PIN_VALUE % (value, HIGH, LOW))

        self.__initial_conditions.append(conditions)

    def add_output_wrapper(self, out_fw: type(sys.stdout)) -> None:
        """
        Adds the wrapper that handles the output to the file or sys.stdout
        to write to console output
        :param out_fw: The IO Wrapper used for outputting string to the file
        :return: None
        """
        self.__out_fw = out_fw

    def write(self, string: str) -> None:
        """
        Writes to the saved output wrapper
        :param string: The string that will be written
        :return: None
        """
        self.__out_fw.write(string)

    def show_all_blocks(self) -> None:
        self.write(self.__bh.get_all_blocks_csv())

    def show_all_edges(self) -> None:
        self.write(self.__graph.get_all_edges_csv())

    def show_all_init_cond(self) -> None:
        result: str = ""
        init_cond: dict
        merged_dict: dict = {}
        if self.__initial_conditions:
            # Check if the list is empty
            for init_cond in self.__initial_conditions:
                merged_dict = {**merged_dict, **init_cond}
            keys = merged_dict.keys()
            key: str
            for key in keys:
                result += key + ','
            result = result[:-1] + '\n'
            for init_cond in self.__initial_conditions:
                node: str
                value: str
                for key in keys:
                    if key in init_cond:
                        result += init_cond[key]
                    result += ','
                result = result[:-1] + '\n'
            self.write(result)
