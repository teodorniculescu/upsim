from blocks.BasicBlock import *
from blocks.LogicalBlock import *
import sys


class Simulation:
    __logical_blocks: dict
    __state_blocks: dict
    " A list of dictionaries "
    __initial_conditions: list
    __number_init_cond: int
    __ic: dict
    __edges: dict
    __changed_state: bool
    " Output wrapper which is by default stdout but can be replaced by a file "
    __out_fw: type(sys.stdout)
    " The number of times show stage state was called "
    __num_sss: int

    def __init__(self):
        self.__logical_blocks = {}
        self.__state_blocks = {}
        self.__initial_conditions = []
        self.__number_init_cond = 0
        self.__ic = {}
        self.__edges = {}
        self.__out_fw = sys.stdout
        self.__num_sss = 0

    def __get_all_blocks(self) -> dict:
        return {**self.__logical_blocks, **self.__state_blocks}

    def __read_stage(self) -> None:
        block: LogicalBlock
        input_pin: BaseValue
        connected_pin: BaseValue
        input_vertex: str
        connected_vertex: str
        for block in self.__get_all_blocks().values():
            for input_pin in block.get_all_pins_with_type(PIN_TYPE_INPUT):
                input_vertex = block.get_name() + '.' + input_pin.get_name()
                if input_vertex in self.__edges:
                    connected_vertex = self.__edges[input_vertex]
                    [connected_block_name, connected_pin_name] =\
                        connected_vertex.split('.')
                    connected_pin =\
                        self.get_block_with_name(connected_block_name)\
                            .get_pin_with_name(connected_pin_name)
                    if connected_pin.is_set():
                        input_pin.set_value(connected_pin.get_value())
                        if input_pin.changed_state_from_last_time_step():
                            self.__changed_state = True
                else:
                    print(input_pin.get_name())
                    print(input_vertex)
                    print(self.__edges)
                    raise Exception(input_vertex + " is not connected.")

    def __calculate_stage(self) -> None:
        block: LogicalBlock
        for block in self.__logical_blocks.values():
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
        for block in self.__get_all_blocks().values():
            block.reset()
        vertex_name: str
        vertex_value_str: str
        block_name: str
        pin_name: str
        for vertex_name, vertex_value_str in self.__ic.items():
            [block_name, pin_name] = vertex_name.split('.')
            vertex_value: int = int(vertex_value_str)
            self.get_block_with_name(block_name).get_pin_with_name(pin_name)\
                .set_value(vertex_value)
        " continue to the next initial condition "
        self.__number_init_cond += 1

    def __finished_all_init_cond(self) -> bool:
        if self.__number_init_cond >= len(self.__initial_conditions):
            return True
        return False

    def __has_simulation_changed_state(self) -> bool:
        return self.__changed_state

    def __get_vertex_names_csv(self) -> str:
        result: str = ""
        block: BasicBlock
        for block in self.__get_all_blocks().values():
            result += block.get_vertex_names_csv()
        result += "\n"
        return result

    def __get_vertex_values_csv(self) -> str:
        result: str = str(self.__number_init_cond) + ',' + str(self.__num_sss)
        block: BasicBlock
        for block in self.__get_all_blocks().values():
            result += block.get_vertex_values_csv()
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
        field_names: str
        field_names = "ICN,SSN"
        field_names += self.__get_vertex_names_csv()
        self.write(field_names)
        while not self.__finished_all_init_cond():
            self.__init_stage()
            self.__changed_state = True
            # Used for showing the number of times the stage state was displayed
            self.__num_sss = 0
            # Shows the state after initializing with the initial conditions
            self.write(self.__get_vertex_values_csv())
            while True:
                self.__num_sss += 1
                self.__changed_state = False
                self.__read_stage()
                self.__calculate_stage()
                if self.__has_simulation_changed_state():
                    self.write(self.__get_vertex_values_csv())
                else:
                    break

    def add_logical_block(self, block: BasicBlock) -> None:
        self.__logical_blocks[block.get_name()] = block

    def add_state_block(self, block: BasicBlock) -> None:
        self.__state_blocks[block.get_name()] = block

    def get_block_with_name(self, block_name: str) -> BasicBlock:
        """
        Searches all types of saved blocks for the one which has the specified
        name
        :param block_name: The name of the block that is searched
        :return: The block with the specified name
        """
        block: BasicBlock
        for block in self.__get_all_blocks().values():
            if block.get_name() == block_name:
                return block
        raise Exception("Block " + block_name + " does not exist.")

    def add_edge(self, node0: str, node1: str) -> None:
        """
        Adds a new edge comprised of two vertices / nodes
        Nodes must be of format 'block name' + '.' + 'pin name'
        :param node0: First vertex
        :param node1: Second vertex
        :return: None
        """
        if node0 in self.__edges:
            raise Exception(node0 + " already connected to a pin")
        if node1 in self.__edges:
            raise Exception(node1 + " already connected to a pin")
        self.__edges[node0] = node1
        self.__edges[node1] = node0

    def add_condition(self, conditions: dict) -> None:
        """
        Adds to the list of initial conditions a new dictionary of conditions
        :param conditions: A dictionary containing {key - the vertex name :
        value - the vertex value}
        :return: None
        """
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
