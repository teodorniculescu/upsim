from blocks.LogicalBlock import LogicalBlock
from blocks.BasicBlock import BasicBlock
from blocks.StateBlock import StateBlock
from values.BaseValue import BaseValue, PIN_TYPE_INPUT, PIN_TYPE_OUTPUT
from typing import List, Tuple, Dict
import simulation.Simulation
import copy


class CustomBlock(LogicalBlock):
    __INPUT: str = "IN"
    __OUTPUT: str = "OUT"
    # contains two dictionaries at the keys specified by __INPUT and __OUTPUT
    __pin_block_dict: Dict[str, Dict[str, StateBlock]]

    def __init__(self,
                 block_name: str,
                 input_names: List[str],
                 output_names: List[str],
                 original_blocks: List[BasicBlock],
                 original_edges: List[Tuple[str, str]]
                 ):
        super().__init__(name=block_name)
        for input_name in input_names:
            self.add_pin(BaseValue(input_name, PIN_TYPE_INPUT))
        for output_name in output_names:
            self.add_pin(BaseValue(output_name, PIN_TYPE_OUTPUT))
        self.__sim = simulation.Simulation.Simulation(use_db=False)

        # initialize the pin block dictionary
        self.__pin_block_dict = {self.__INPUT: {}, self.__OUTPUT: {}}

        # add state blocks that link to pins
        self.__add_to_pin_block_dict(input_names, PIN_TYPE_OUTPUT, self.__INPUT)
        self.__add_to_pin_block_dict(output_names, PIN_TYPE_INPUT, self.__OUTPUT)

        # add copies of the original blocks
        for block in original_blocks:
            self.__sim.add_block(copy.deepcopy(block))

        # add the edges
        for (output_node_name, input_node_name) in original_edges:
            onn = self.__transform_THIS_node(output_node_name)
            inn = self.__transform_THIS_node(input_node_name)
            self.__sim.add_edge(onn, inn)

        # setup the internal pins
        self.__sim.setup_run()

        """
        # dbg
        print("blocks")
        self.__sim.show_all_blocks()
        print("edges")
        self.__sim.show_all_edges()
        """

    def __transform_THIS_node(self, node_name: str) -> str:
        [block_name, pin_name] = node_name.split(".")
        if block_name == "THIS":
            return "THIS/" + pin_name + ".val"
        return node_name

    def __add_to_pin_block_dict(
            self,
            name_list: List[str],
            pin_type: int,
            pin_type_dict: str
    ) -> None:
        for name in name_list:
            new_state_block = StateBlock("THIS/" + name, pin_type)
            self.__sim.add_block(new_state_block)
            self.__pin_block_dict[pin_type_dict][name] = new_state_block

    def __transfer_pin(self, from_pin: BaseValue, to_pin: BaseValue) -> None:
        to_pin.set_value(from_pin.get_value())

    def __load_input_pins(self) -> None:
        # create the initial condition
        cond_dict: Dict[str, str] = {}
        for pin in self.get_all_pins_with_type(PIN_TYPE_INPUT).values():
            # get the state block
            state_block: StateBlock = self.__pin_block_dict[self.__OUTPUT][pin.get_name()]
            # get the val pin of the state block
            state_block_pin: BaseValue = state_block.get_pin_with_name("val")
            # generate the node name by merging the block and pin names
            node_name: str = state_block.get_name() + "." + state_block_pin.get_name()
            # generate the value of the val pin
            node_value_str: str = str(state_block_pin.get_value())
            # store in the dictionary of initial conditions
            cond_dict[node_name] = node_value_str
        # add the initial condition
        self.__sim.add_condition(cond_dict)

    def __store_output_pins(self) -> None:
        for pin in self.get_all_pins_with_type(PIN_TYPE_OUTPUT).values():
            from_pin = self.__pin_block_dict[self.__INPUT][pin.get_name()].get_pin_with_name("val")
            self.__transfer_pin(from_pin=from_pin, to_pin=pin)

    def calculate(self) -> None:
        # load values from the INPUT pins to the state blocks from the simulation
        self.__load_input_pins()
        # run the simulation for the specified initial conditions
        self.__sim.progress_run()
        # load the values form the OUTPUT pins to the
        self.__store_output_pins()


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

    def generate_custom_block(self, block_name: str) -> CustomBlock:
        return CustomBlock(
            block_name=block_name,
            input_names=self.__input_names,
            output_names=self.__output_names,
            original_blocks=self.__blocks,
            original_edges=self.__edges
        )
