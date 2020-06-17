from blocks.BlockHandler import BlockHandler
from blocks.CustomBlock import CustomBlockTemplate
from blocks.LogicalBlock import LogicalBlock
from values.BaseValue import BaseValue, PIN_TYPE_INPUT, HIGH, LOW
from blocks.BasicBlock import BasicBlock
from blocks.StateBlock import StateBlock
from simulation.Node import Node
from simulation.Graph import Graph
from typing import Dict, Tuple
from database.DBController import *
from datetime import datetime
from random import random

PROPAGATE_CMD: [str] = "prop"
CALCULATE_CMD: [str] = "calc"


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

    def __init__(self,
                 use_db: bool = True):
        self.__execution_stack = []
        self.__bh = BlockHandler()
        self.__initial_conditions = []
        self.__number_init_cond = 0
        self.__ic = {}
        self.__num_sss = 0
        self.__graph = Graph(self.__bh)
        self.__use_db = use_db
        if use_db:
            self.__out_fw = sys.stdout
            self.__dbc = DBController()
            self.table_name = \
                "run_" + \
                datetime.now().strftime("%d%m%Y_%H%M%S_") + \
                str(int(random() * 1000000))

    def get_positionable_blocks(self):
        return self.__bh.get_positionable_blocks()

    def add_block_position(self, block_name: str, block_position: Tuple[int, int]) -> None:
        self.__bh.get_block_with_name(block_name).set_position(block_position)

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

    def setup_run(self) -> None:
        if self.__use_db:
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
            if self.__graph.get_vertex_value(vertex_name) == vertex_value_str:
                continue
            # obtains the integer value from the stored string
            vertex_value: int = int(vertex_value_str)
            # TODO exception if the vertex value is invalid
            # sets the value to the appropriate pin
            self.__graph.set_vertex_value(vertex_name, vertex_value)
            # set new stack value
            stack_value: Tuple[str, str] = \
                (self.__graph.get_node(vertex_name).__str__(),
                 PROPAGATE_CMD)
            # setup execution stack
            self.__insert_execution(stack_value)

        # increment initial condition counter
        self.__number_init_cond += 1
        # Used for showing the number of times the stage state was displayed
        self.__num_sss = 0
        if self.__use_db:
            # Shows the state after initializing with the initial conditions
            self.__dbc.insert_row(self.table_name, self.get_run_line())

    def __insert_execution(self, stack_value: Tuple[str, str]) -> None:
        self.__execution_stack.append(stack_value)

    def __remove_execution(self) -> Tuple[str, str]:
        stack_value: Tuple[str, str]
        stack_value = self.__execution_stack.pop()
        return stack_value

    def __execution_stack_is_empty(self) -> bool:
        return len(self.__execution_stack) == 0

    def __propagate(self, node_name: str) -> List[str]:
        calculate_blocks_list: List[str] = self.__graph.propagate_values_block(node_name)
        return calculate_blocks_list


    def __calculate(self, block_name: str) -> List[str]:
        propagate_blocks_list: List[str] = self.__graph.calculate_values_block(block_name)
        return propagate_blocks_list

    def set_previous_value_all_blocks(self) -> None:
        block: BasicBlock
        pin: BaseValue
        for block in self.__bh.get_all_blocks().values():
            for pin in block.get_all_pins().values():
                pin.set_previous_value()

    def progress_run(self) -> None:
        self.__setup_init_cond()
        print(self.__number_init_cond)
        while not self.__execution_stack_is_empty():
            print(self.__execution_stack)
            self.show_all_blocks_current_values()
            # increment the number of steps the initial conditions took to completion
            self.__num_sss += 1
            # pop execution stack
            (block, cmd) = self.__remove_execution()
            new_stack_elements: List[str]
            new_cmd: str
            # propagate or calculate
            if cmd == PROPAGATE_CMD:
                new_stack_elements = self.__propagate(block)
                new_cmd = CALCULATE_CMD
            elif cmd == CALCULATE_CMD:
                new_stack_elements = self.__calculate(block)
                new_cmd = PROPAGATE_CMD
            else:
                # Create exception for undefined cmd from execution stack
                raise Exception("UNDEFINED")
            # push execution stack
            for new_element in new_stack_elements:
                self.__insert_execution((new_element, new_cmd))
            if self.__use_db:
                # show circuit state, which means inserting a value in the table
                self.__dbc.insert_row(self.table_name, self.get_run_line())
        self.set_previous_value_all_blocks()

    def run(self) -> None:
        """
        Creates a CSV with the following fields:
        - Initial Condition Number - ICN
        - State Stage Num - SSN
        - The names of each pin from the schematic
        :return: None
        """

        self.setup_run()
        while not self.__finished_all_init_cond():
            self.progress_run()
        if self.__use_db:
            self.__dbc.commit()

    def display(self, description: Tuple[str], values: List[Tuple]) -> None:
        self.write(str(description) + "\n")
        for line in values:
            self.write(str(line) + "\n")

    def show_run_select_all(self) -> None:
        if not self.__use_db:
            # TODO create exception with proper error code
            raise Exception("There is no database controler")
        description = self.__dbc.describe_table(self.table_name)
        names: Tuple[str] = tuple()
        for line in description:
            names += (line[0], )
        values = self.__dbc.select_all_from_table(self.table_name)
        self.display(names, values)

    def show_run_select_some(self, columns: List[str]) -> None:
        if not self.__use_db:
            # TODO create exception with proper error code
            raise Exception("There is no database controler")
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

    def pop_condition(self) -> None:
        # remove the first element
        self.__initial_conditions.pop()
        # decrement the counter
        self.__number_init_cond -= 1

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

    def create_custom_block_template(self, custom_template: CustomBlockTemplate) -> None:
        self.__bh.create_custom_block_template(custom_template)

    def create_custom_block(self, template_name: str, block_name: str) -> BasicBlock:
        return self.__bh.create_custom_block(template_name, block_name)

    def show_all_blocks_current_values(self) -> None:
        self.__bh.show_all_blocks_current_values()

    def show_last_condition(self) -> None:
        print("dimensiune " + str(len(self.__initial_conditions)))
        print(self.__initial_conditions[-1])
