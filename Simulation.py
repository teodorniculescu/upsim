from blocks.BasicBlock import *
from blocks.LogicalBlock import *
from blocks.StateBlock import *
from gen.FileSyntaxParser import *
from FileSyntaxErrorListener import *
from BlockHandler import *
from Node import Node
import sys
from Graph import Graph


class Simulation:
    __bh: BlockHandler
    " A list of dictionaries "
    __initial_conditions: list
    __number_init_cond: int
    __ic: dict
    __changed_state: bool
    " Output wrapper which is by default stdout but can be replaced by a file "
    __out_fw: type(sys.stdout)
    " The number of times show stage state was called "
    __num_sss: int
    __graph: Graph

    def __init__(self):
        self.__bh = BlockHandler()
        self.__initial_conditions = []
        self.__number_init_cond = 0
        self.__ic = {}
        self.__out_fw = sys.stdout
        self.__num_sss = 0
        self.__graph = Graph(self.__bh)

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
                    print(input_pin.get_name())
                    print(input_vertex)
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
        self.__ic.update(ic_curr)
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

    def get_time_step_values_csv(self) -> str:
        return str(self.__number_init_cond) + ',' + str(self.__num_sss)

    def get_time_step_names_csv(self) -> str:
        return "ICN,SSN"

    def get_run_names_csv(self) -> str:
        result: str = ""
        result += self.get_time_step_names_csv()
        result += self.__graph.get_all_vertex_names_csv()
        result += '\n'
        return result

    def get_run_values_cvs(self) -> str:
        result: str = ""
        result += self.get_time_step_values_csv()
        result += self.__graph.get_all_vertex_values_csv()
        result += '\n'
        return result

    def run(self) -> None:
        """
        Creates a CSV with the following fields:
        - Initial Condition Number - ICN
        - State Stage Num - SSN
        - The names of each pin from the schematic
        :return: None
        """
        self.write(self.get_run_names_csv())
        while not self.__finished_all_init_cond():
            self.__init_stage()
            self.__changed_state = True
            # Used for showing the number of times the stage state was displayed
            self.__num_sss = 0
            # Shows the state after initializing with the initial conditions
            self.write(self.get_run_values_cvs())
            while True:
                self.__num_sss += 1
                self.__changed_state = False
                self.__read_stage()
                self.__calculate_stage()
                if self.__has_simulation_changed_state():
                    self.write(self.get_run_values_cvs())
                else:
                    break
        self.write("\n")

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
        line: str = "\n"
        init_cond: dict
        for init_cond in self.__initial_conditions:
            self.write(str(init_cond))
        self.write("\n")
        # TODO implement inital conditions in csv format
