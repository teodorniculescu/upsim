from blocks.StateBlock import StateBlock
from gen.FileSyntaxListener import FileSyntaxListener
from gen.FileSyntaxParser import FileSyntaxParser
from Simulation import Simulation
from blocks.store.LogicGates import *
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
            raise Exception(err_msg)

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
        self.__error_number = int(str(ctx.INTEGER()))

    def exitInsert_blocks(self, ctx: FileSyntaxParser.Insert_blocksContext):
        if self.error_is_set():
            return

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
            self.__sim.add_block(
                func(block_name, [input0_name, input1_name], [output_name]))
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
            self.__sim.add_block(
                StateBlock(block_name, pin_type, io_name))
        except Exception as e:
            self.__set_error(ctx, e)

    def exitBlock_name(self, ctx: FileSyntaxParser
                       .Block_nameContext):
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
        try:
            for input_node in input_nodes:
                self.__sim.add_edge(output_node, input_node)
        except Exception as e:
            self.__set_error(ctx, e)

    def exitNode_value(self, ctx: FileSyntaxParser
                       .Node_valueContext):
        ctx.number = str(ctx.INTEGER())

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
        try:
            self.__sim.add_condition(conditions)
        except Exception as e:
            self.__set_error(ctx, e)

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
            self.__sim.add_block(
                func(block_name, input_names, [output_name]))
        except Exception as e:
            self.__set_error(ctx, e)

