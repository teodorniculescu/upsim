from blocks.StateBlock import StateBlock, GroundBlock, VCCBlock
from gen.FileSyntaxListener import FileSyntaxListener
from gen.FileSyntaxParser import FileSyntaxParser
from simulation.Simulation import Simulation
from blocks.store.LogicGates import *
from blocks.store.Latch import D_LATCH, JK_LATCH
from blocks.store.Buffer import DIGITAL_TRI_STATE_BUFFER, BUS_TRANSMITTER_RECEIVER, BUFFER, BUS, ROM
from blocks.CustomBlock import CustomBlockTemplate
from antlr4.Token import *


class WrapperFileSyntaxListener(FileSyntaxListener):
    __sim: Simulation
    __output: type(sys.stdout)
    """
     Specifies if an error has occurred in some block which renders the block
     execution useless. In other words, signals if an error has occurred
     somewhere along the execution.
     It resets each time a new instruction starts."
    """
    __error_occ: bool
    __error_message: str
    __expecting_error: bool
    __error_number: int

    def __init__(self, sim: Simulation, output: type(sys.stdout)):
        self.__sim = sim
        self.__output = output
        self.__error_occ = False
        self.__error_message = ""
        self.__expecting_error = False

    def __set_error(self, ctx, e: Exception) -> None:
        token: CommonToken
        token = ctx.start
        err_msg: str = str(token.line) + ':' + str(token.column) + ' ' +\
                       "ERROR " + e.args[0]
        if (self.__expecting_error and
                self.__error_number == int(e.args[0].split(':')[0])):
            self.__expecting_error = False
            self.__error_occ = True
            self.__error_message = err_msg
            ctx.parser.notifyErrorListeners(err_msg, token)
        else:
            raise Exception(err_msg + \
                            " with expecting error " + str(self.__expecting_error) + \
                            " with error expected error number " + str(self.__error_number))

    def clear_error(self) -> None:
        self.__error_occ = False
        self.__error_message = ""

    def error_is_set(self) -> bool:
        return self.__error_occ

    def enterCommand(self, ctx: FileSyntaxParser.CommandContext):
        self.clear_error()

    def exitCommand(self, ctx: FileSyntaxParser.CommandContext):
        if self.__expecting_error:
            raise Exception(ERROR_NO_EXPECTED_ERROR % self.__error_number)
        if self.error_is_set():
            return

    def exitExpect(self, ctx: FileSyntaxParser.ExpectContext):
        self.__expecting_error = True
        self.__error_number = int(str(ctx.UINT()))

    def exitLogic_gate_types(self, ctx:FileSyntaxParser.Logic_gate_typesContext):
        ctx.text = str(ctx.getText())

    def exitLogic_gate_types_n(self, ctx:FileSyntaxParser.Logic_gate_typesContext):
        ctx.text = str(ctx.getText())

    lg2i = {
        "AND2": AND2,
        "OR2": OR2,
        "NOR2": NOR2,
        "NAND2": NAND2,
        "XOR2": XOR2,
        "XNOR2": XNOR2
    }

    def exitCreate_logic_gate_2_inputs(self, ctx:FileSyntaxParser.Create_logic_gate_2_inputsContext):
        if self.error_is_set():
            return
        block_type: str = ctx.logic_gate_types().text
        block_name = ctx.block_name().text
        input0_name = ctx.input_pin_name(0).text
        input1_name = ctx.input_pin_name(1).text
        output_name = ctx.output_pin_name().text
        try:
            func = self.lg2i.get(block_type)
            ctx.block = func(block_name, [input0_name, input1_name], [output_name])
        except Exception as e:
            self.__set_error(ctx, e)

    def exitCreate_state_block(self, ctx: FileSyntaxParser
                               .Create_state_blockContext):
        if self.error_is_set():
            return
        pin_type = ctx.pin_type().pin_type
        block_name = ctx.block_name().text
        if ctx.io_pin_name() is None:
            io_name = "val"
        else:
            io_name = ctx.io_pin_name().text
        try:
            ctx.block = StateBlock(block_name, pin_type, io_name)
        except Exception as e:
            self.__set_error(ctx, e)

    def exitBlock_name(self, ctx: FileSyntaxParser
                       .Block_nameContext):
        ctx.text = str(ctx.NAME())

    def exitCustom_block_keyword(self, ctx:FileSyntaxParser.Custom_block_keywordContext):
        ctx.text = str(ctx.NAME())

    def exitInput_pin_name(self, ctx: FileSyntaxParser
                           .Input_pin_nameContext):
        ctx.text = str(ctx.NAME())

    def exitOutput_pin_name(self, ctx: FileSyntaxParser
                            .Output_pin_nameContext):
        ctx.text = str(ctx.NAME())

    def enterIo_pin_name(self, ctx: FileSyntaxParser.Io_pin_nameContext):
        ctx.text = ""

    def exitIo_pin_name(self, ctx: FileSyntaxParser
                        .Io_pin_nameContext):
        ctx.text = str(ctx.NAME())

    def exitPin_name(self, ctx: FileSyntaxParser
                     .Pin_nameContext):
        ctx.text = str(ctx.NAME())

    def exitNode(self, ctx: FileSyntaxParser
                 .NodeContext):
        block_name = ctx.block_name().text
        pin_name = ctx.pin_name().text
        ctx.text = block_name + "." + pin_name

    def exitOne_or_multiple_nodes(self, ctx:FileSyntaxParser.One_or_multiple_nodesContext):
        input_nodes: List[str] = []
        for node in ctx.node():
            input_nodes.append(node.text)
        ctx.input_nodes = input_nodes

    def exitCreate_edge(self, ctx: FileSyntaxParser
                        .Create_edgeContext):
        output_node: str = ctx.node().text
        input_nodes: List[str] = ctx.one_or_multiple_nodes().input_nodes
        ctx.edges_list = []
        for input_node in input_nodes:
            ctx.edges_list.append((output_node, input_node))

    def exitNode_value(self, ctx: FileSyntaxParser
                       .Node_valueContext):
        ctx.number = str(ctx.UINT())

    def exitCondition(self, ctx: FileSyntaxParser
                      .ConditionContext):
        ctx.node = ctx.node().text
        ctx.number = ctx.node_value().number

    def exitInitial_condition(self, ctx: FileSyntaxParser
                              .Initial_conditionContext):
        conditions: dict
        conditions = {}
        for cond in ctx.condition():
            conditions[cond.node] = cond.number
        ctx.conditions_dict = conditions

    def exitRun(self, ctx: FileSyntaxParser.RunContext):
        self.__sim.run()

    def exitPin_type(self, ctx: FileSyntaxParser.Pin_typeContext):
        if ctx.getText() == str(ctx.INPUT_KWD()):
            ctx.pin_type = PIN_TYPE_INPUT
        elif ctx.getText() == str(ctx.OUTPUT_KWD()):
            ctx.pin_type = PIN_TYPE_OUTPUT
        elif ctx.getText() == str(ctx.INPUT_OUTPUT_KWD()):
            ctx.pin_type = PIN_TYPE_IO
        else:
            ctx.pin_type = PIN_TYPE_ERROR

    def exitShow_blocks(self, ctx: FileSyntaxParser.Show_blocksContext):
        self.__sim.show_all_blocks()

    def exitShow_edges(self, ctx: FileSyntaxParser.Show_edgesContext):
        self.__sim.show_all_edges()

    def exitShow_initial_conditions(self,
                                    ctx: FileSyntaxParser.
                                    Show_initial_conditionsContext):
        self.__sim.show_all_init_cond()

    def exitShow_run_all(self, ctx:FileSyntaxParser.Show_run_allContext):
        self.__sim.show_run_select_all()

    def exitShow_run_selection(
            self,
            ctx:FileSyntaxParser.Show_run_selectionContext
    ):
        nodes: List[str] = []
        for node in ctx.node():
            nodes.append(node.text)
        self.__sim.show_run_select_some(nodes)

    lgNi = {
        "XOR": XOR,
        "XNOR": XNOR,
        "NOR": NOR,
        "OR": OR,
        "AND": AND,
        "NAND": NAND
    }

    def exitCreate_logic_gate_n_inputs(
            self,
            ctx:FileSyntaxParser.Create_logic_gate_n_inputsContext
    ):
        if self.error_is_set():
            return
        block_type: str = ctx.logic_gate_types_n().text
        block_name = ctx.block_name().text
        input_names: List[str] = []
        for input_pin in ctx.input_pin_name():
            input_names.append(input_pin.text)
        output_name = ctx.output_pin_name().text
        try:
            func = self.lgNi.get(block_type)
            ctx.block = func(block_name, input_names, [output_name])
        except Exception as e:
            self.__set_error(ctx, e)

    def exitCreate_not_gate(
            self,
            ctx: FileSyntaxParser.Create_not_gateContext
    ):
        if self.error_is_set():
            return
        block_name = ctx.block_name().text
        input_name = ctx.input_pin_name().text
        output_name = ctx.output_pin_name().text
        try:
            ctx.block = NOT(block_name, [input_name], [output_name])
        except Exception as e:
            self.__set_error(ctx, e)

    def exitDisplay(self, ctx: FileSyntaxParser.DisplayContext):
        animate = False if (ctx.ANIMATE_KWD() is None) else True
        if ctx.block_position() is None:
            ul_corner = (0, 0)
        else:
            ul_corner = ctx.block_position().val
        import user_interface.UI
        user_interface.UI.UI(simulation=self.__sim,
                             animate=animate,
                             ul_corner=ul_corner).run()

    def exitBlock_position(self, ctx:FileSyntaxParser.Block_positionContext):
        index_line = int(str(ctx.UINT(0)))
        index_column = int(str(ctx.UINT(1)))
        ctx.val = (index_line, index_column)

    def exitDraw_one_block(self, ctx:FileSyntaxParser.Draw_one_blockContext):
        name = ctx.block_name().text
        pos = ctx.block_position().val
        if ctx.MIRROR_KWD() is not None:
            mirror = True
        else:
            mirror = False
        self.__sim.add_block_position(name, pos, mirror)

    def exitCreate_jk_latch(self, ctx:FileSyntaxParser.Create_d_latchContext):
        if self.error_is_set():
            return
        block_name = ctx.block_name().text
        try:
            ctx.block = JK_LATCH(block_name)
        except Exception as e:
            self.__set_error(ctx, e)

    def exitCreate_d_latch(self, ctx:FileSyntaxParser.Create_d_latchContext):
        if self.error_is_set():
            return
        block_name = ctx.block_name().text
        try:
            ctx.block = D_LATCH(block_name)
        except Exception as e:
            self.__set_error(ctx, e)

    def exitCreate_block(self, ctx:FileSyntaxParser.Create_blockContext):
        if self.error_is_set():
            return
        ctx.block_list = []
        # the create block method always has one children because it
        # has to choose between the types of blocks that were created
        # which means that it always returns a list with one element
        # inside
        for context in ctx.children:
            ctx.block_list.append(context.block)

    def exitInsert_blocks(self, ctx: FileSyntaxParser.Insert_blocksContext):
        if self.error_is_set():
            return
        ctx.all_blocks_list = []
        for context in ctx.create_block():
            ctx.all_blocks_list += context.block_list

    def exitInsert(self, ctx:FileSyntaxParser.InsertContext):
        if self.error_is_set():
            return
        # insert blocks
        if ctx.insert_blocks() is not None:
            for block in ctx.insert_blocks().all_blocks_list:
                try:
                    self.__sim.add_block(block)
                except Exception as e:
                    # in this case we set the error and stop
                    # the execution in order to prevent the
                    # addition of further problematic blocks
                    self.__set_error(ctx, e)
                    return
        # insert edges
        elif ctx.insert_edges() is not None:
            for (output_node, input_node) in ctx.insert_edges().all_edges_list:
                try:
                    self.__sim.add_edge(output_node, input_node)
                except Exception as e:
                    self.__set_error(ctx, e)
                    return
        # insert initial conditions
        elif ctx.insert_initial_conditions() is not None:
            for conditions_dict in ctx.insert_initial_conditions().all_init_cond_dict_list:
                try:
                    self.__sim.add_condition(conditions_dict)
                except Exception as e:
                    self.__set_error(ctx, e)
                    return
        else:
            # TODO add proper exception
            raise Exception("insert rule impossible")

    def exitInsert_edges(self, ctx:FileSyntaxParser.Insert_edgesContext):
        if self.error_is_set():
            return
        ctx.all_edges_list = []
        for context in ctx.create_edge():
            ctx.all_edges_list += context.edges_list

    def exitInsert_initial_conditions(self, ctx: FileSyntaxParser.Insert_initial_conditionsContext):
        if self.error_is_set():
            return
        ctx.all_init_cond_dict_list = []
        for context in ctx.initial_condition():
            ctx.all_init_cond_dict_list.append(context.conditions_dict)

    def exitDefine(self, ctx:FileSyntaxParser.DefineContext):
        if self.error_is_set():
            return
        template_name = ctx.custom_block_keyword().text
        try:
            # create the custom block
            custom_block_template = CustomBlockTemplate(template_name)
            # add all pins
            if ctx.define_input_pins() is not None:
                custom_block_template.add_input_pins(ctx.define_input_pins().pin_list)
            if ctx.define_output_pins() is not None:
                custom_block_template.add_output_pins(ctx.define_output_pins().pin_list)
            if ctx.define_io_pins() is not None:
                custom_block_template.add_io_pins(ctx.define_io_pins().pin_list)
            # add all blocks
            if ctx.insert_blocks() is not None:
                for context in ctx.insert_blocks():
                    custom_block_template.add_blocks(context.all_blocks_list)
            # add all edges
            if ctx.insert_edges() is not None:
                for context in ctx.insert_edges():
                    custom_block_template.add_edges(context.all_edges_list)
            # add the custom block template
            self.__sim.create_custom_block_template(custom_block_template)
        except Exception as e:
            self.__set_error(ctx, e)

    def exitDefine_input_pins(self, ctx:FileSyntaxParser.Define_input_pinsContext):
        ctx.pin_list = []
        for context in ctx.input_pin_name():
            ctx.pin_list.append(context.text)

    def exitDefine_output_pins(self, ctx:FileSyntaxParser.Define_output_pinsContext):
        ctx.pin_list = []
        for context in ctx.output_pin_name():
            ctx.pin_list.append(context.text)

    def exitDefine_io_pins(self, ctx:FileSyntaxParser.Define_io_pinsContext):
        ctx.pin_list = []
        for context in ctx.io_pin_name():
            ctx.pin_list.append(context.text)

    def exitCreate_buffer(self, ctx:FileSyntaxParser.Create_bufferContext):
        if self.error_is_set():
            return
        block_name = ctx.block_name().text
        try:
            ctx.block = BUFFER(block_name)
        except Exception as e:
            self.__set_error(ctx, e)

    def exitCreate_bus_line(self, ctx:FileSyntaxParser.Create_bus_lineContext):
        if self.error_is_set():
            return
        block_name = ctx.block_name().text
        value = int(str(ctx.UINT()))
        try:
            ctx.block = BUS(block_name)
            ctx.block.set_bus_height(value)
        except Exception as e:
            self.__set_error(ctx, e)

    def exitCreate_digital_tri_state_buffer(self, ctx:FileSyntaxParser.Create_digital_tri_state_bufferContext):
        if self.error_is_set():
            return
        block_name = ctx.block_name().text
        try:
            ctx.block = DIGITAL_TRI_STATE_BUFFER(block_name)
        except Exception as e:
            self.__set_error(ctx, e)

    def exitCreate_custom_block(self, ctx:FileSyntaxParser.Create_custom_blockContext):
        template_name = ctx.custom_block_keyword().text
        block_name = ctx.block_name().text
        try:
            ctx.block = self.__sim.create_custom_block(template_name, block_name)
        except Exception as e:
            self.__set_error(ctx, e)

    def exitCreate_bus_transmitter_receiver(self, ctx:FileSyntaxParser.Create_bus_transmitter_receiverContext):
        if self.error_is_set():
            return
        block_name = ctx.block_name().text
        try:
            ctx.block = BUS_TRANSMITTER_RECEIVER(block_name)
        except Exception as e:
            self.__set_error(ctx, e)

    def exitCreate_vcc_block(self, ctx:FileSyntaxParser.Create_vcc_blockContext):
        if self.error_is_set():
            return
        block_name = ctx.block_name().text
        io_name = "val"
        try:
            ctx.block = VCCBlock(name=block_name, pin_name=io_name)
        except Exception as e:
            self.__set_error(ctx, e)

    def exitCreate_ground_block(self, ctx:FileSyntaxParser.Create_ground_blockContext):
        if self.error_is_set():
            return
        block_name = ctx.block_name().text
        io_name = "val"
        try:
            ctx.block = GroundBlock(name=block_name, pin_name=io_name)
        except Exception as e:
            self.__set_error(ctx, e)

    def exitDraw_one_edge(self, ctx:FileSyntaxParser.Draw_one_edgeContext):
        self.__sim.draw_node_edge(
            node_name=ctx.node().text,
            direction_list=ctx.draw_direction_snake_edge().direction_list
        )

    def exitDraw_direction_snake_edge(self, ctx:FileSyntaxParser.Draw_direction_snake_edgeContext):
        ctx.direction_list = []
        for context in ctx.draw_direction_snake():
            ctx.direction_list += context.direction_list


    def exitDraw_direction_snake(self, ctx:FileSyntaxParser.Draw_direction_snakeContext):
        ctx.direction_list = []
        if ctx.UINT() is None:
            counter = 1
        else:
            counter = int(str(ctx.UINT()))
        for x in range(counter):
            ctx.direction_list.append(ctx.direction_snake().text)

    def exitDirection_snake(self, ctx:FileSyntaxParser.Direction_snakeContext):
        ctx.text = str(ctx.getText())

    def exitCreate_rom_block(self, ctx:FileSyntaxParser.Create_rom_blockContext):
        num_addr = ctx.num_rom_address().num
        num_data = ctx.num_rom_data().num
        content = ctx.rom_contents().matrix_dict
        block_name = ctx.block_name().text
        try:
            ctx.block = ROM(block_name, num_addr, num_data, content)
        except Exception as e:
            self.__set_error(ctx, e)

    def exitNum_rom_address(self, ctx:FileSyntaxParser.Num_rom_addressContext):
        ctx.num = int(str(ctx.UINT()))

    def exitNum_rom_data(self, ctx:FileSyntaxParser.Num_rom_dataContext):
        ctx.num = int(str(ctx.UINT()))

    def exitRom_contents(self, ctx:FileSyntaxParser.Rom_contentsContext):
        ctx.matrix_dict = ctx.rom_matrix().matrix_dict

    def exitRom_matrix(self, ctx:FileSyntaxParser.Rom_matrixContext):
        matrix_dict = {}
        for context in ctx.rom_row():
            (index, row) = context.row
            matrix_dict[index] = row
        ctx.matrix_dict = matrix_dict

    def exitRow_index(self, ctx:FileSyntaxParser.Row_indexContext):
        ctx.val = int(str(ctx.UINT()))

    def exitRom_row(self, ctx:FileSyntaxParser.Rom_rowContext):
        row = []
        index = ctx.row_index().val
        for context in ctx.rom_value():
            row.append(context.value)
        ctx.row = (index ,row)

    def exitRom_value(self, ctx:FileSyntaxParser.Rom_valueContext):
        ctx.value = int(str(ctx.UINT()))
