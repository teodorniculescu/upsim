from blocks.LogicalBlock import LogicalBlock
from blocks.BasicBlock import BasicBlock
from blocks.StateBlock import StateBlock
from values.BaseValue import BaseValue, PIN_TYPE_INPUT, PIN_TYPE_OUTPUT, PIN_TYPE_IO
from typing import List, Tuple, Dict
import simulation.Simulation
import copy


class CustomBlock(LogicalBlock):
    __INPUT_PINS: str = "IN"
    __OUTPUT_PINS: str = "OUT"
    __IO_PINS: str = "IO"
    # contains two dictionaries at the keys specified by __INPUT_PINS and __OUTPUT_PINS
    __pin_block_dict: Dict[str, Dict[str, StateBlock]]

    def __init__(self,
                 block_name: str,
                 input_names: List[str],
                 output_names: List[str],
                 io_names: List[str],
                 original_blocks: List[BasicBlock],
                 original_edges: List[Tuple[str, str]]
                 ):
        super().__init__(name=block_name)
        for input_name in input_names:
            self.add_pin(BaseValue(input_name, PIN_TYPE_INPUT))
        for output_name in output_names:
            self.add_pin(BaseValue(output_name, PIN_TYPE_OUTPUT))
        for io_name in io_names:
            self.add_pin(BaseValue(io_name, PIN_TYPE_IO))
        self.__sim = simulation.Simulation.Simulation(use_db=False)

        # initialize the pin block dictionary
        self.__pin_block_dict = {
            self.__INPUT_PINS: {},
            self.__OUTPUT_PINS: {},
            self.__IO_PINS: {}
        }

        # add state blocks that link to pins
        self.__add_to_pin_block_dict(input_names, PIN_TYPE_OUTPUT, self.__INPUT_PINS)
        self.__add_to_pin_block_dict(output_names, PIN_TYPE_INPUT, self.__OUTPUT_PINS)
        self.__add_to_pin_block_dict(io_names, PIN_TYPE_IO, self.__IO_PINS)

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
        to_pin.set_is_state(from_pin.is_set())

    def __load_input_pins(self) -> None:
        in_and_io_pins = {
            **self.get_all_pins_with_type(PIN_TYPE_INPUT),
            **self.get_all_pins_with_type(PIN_TYPE_IO)
        }
        # create the initial condition
        cond_dict: Dict[str, str] = {}
        for pin in in_and_io_pins.values():
            # get the state block
            pin_name = pin.get_name()
            if pin_name in self.__pin_block_dict[self.__INPUT_PINS]:
                dict_pin_name = self.__pin_block_dict[self.__INPUT_PINS]
            elif pin_name in self.__pin_block_dict[self.__IO_PINS]:
                dict_pin_name = self.__pin_block_dict[self.__IO_PINS]
            else:
                # TODO create an exception with error code
                raise Exception("pin does not exist")
            state_block: StateBlock = dict_pin_name[pin_name]
            # get the val pin of the state block
            state_block_pin: BaseValue = state_block.get_pin_with_name("val")
            # generate the node name by merging the block and pin names
            node_name: str = state_block.get_name() + "." + state_block_pin.get_name()
            # generate the value of the val pin from the shell not the the interior
            node_value_str: str = str(pin.get_value())
            # store in the dictionary of initial conditions
            cond_dict[node_name] = node_value_str
        # add the initial condition
        self.__sim.add_condition(cond_dict)

    def __store_output_pins(self) -> None:
        io_and_out_pins = {
            **self.get_all_pins_with_type(PIN_TYPE_OUTPUT),
            **self.get_all_pins_with_type(PIN_TYPE_IO)
        }
        for pin in io_and_out_pins.values():
            # get the state block
            pin_name = pin.get_name()
            if pin_name in self.__pin_block_dict[self.__OUTPUT_PINS]:
                dict_pin_name = self.__pin_block_dict[self.__OUTPUT_PINS]
            elif pin_name in self.__pin_block_dict[self.__IO_PINS]:
                dict_pin_name = self.__pin_block_dict[self.__IO_PINS]
            else:
                # TODO create an exception with error code
                raise Exception("pin does not exist")
            from_pin = dict_pin_name[pin_name].get_pin_with_name("val")
            self.__transfer_pin(from_pin=from_pin, to_pin=pin)

    def calculate(self) -> None:
        # load values from the INPUT pins to the state blocks from the simulation
        self.__load_input_pins()
        # run the simulation for the specified initial conditions
        self.__sim.progress_run()
        # load the values form the OUTPUT pins to the
        self.__store_output_pins()
        # remove the initial condition
        self.__sim.pop_condition()


class CustomBlockTemplate:
    __name: str
    __blocks: List[BasicBlock]
    __edges: List[Tuple[str, str]]
    __input_names: List[str]
    __output_names: List[str]
    __io_names: List[str]

    def __init__(self, name: str):
        self.__name = name
        self.__blocks = []
        self.__edges = []
        self.__input_names = []
        self.__output_names = []
        self.__io_names = []

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

    def add_io_pins(self, pin_list: List[str]) -> None:
        self.__io_names += pin_list

    def generate_custom_block(self, block_name: str) -> CustomBlock:
        return CustomBlock(
            block_name=block_name,
            input_names=self.__input_names,
            output_names=self.__output_names,
            io_names=self.__io_names,
            original_blocks=self.__blocks,
            original_edges=self.__edges
        )
