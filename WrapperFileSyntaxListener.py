import sys
from blocks.StateBlock import StateBlock
from blocks.BasicBlock import *
from gen.FileSyntaxListener import FileSyntaxListener
from gen.FileSyntaxParser import FileSyntaxParser
from Simulation import Simulation
from saved_blocks.AND2 import AND2
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
        err_msg: str = str(token.line) + ':' + str(token.column) + ' ' + \
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

    def exitExpect(self, ctx:FileSyntaxParser.ExpectContext):
        self.__expecting_error = True
        self.__error_number = int(str(ctx.INTEGER()))

    def exitInsert_blocks(self, ctx: FileSyntaxParser.Insert_blocksContext):
        if self.error_is_set():
            return

    def exitCreate_and2_block(self, ctx: FileSyntaxParser
                              .Create_and2_blockContext):
        if self.error_is_set():
            return
        block_name = ctx.block_name().text
        input0_name = ctx.input_pin_name(0).text
        input1_name = ctx.input_pin_name(1).text
        output_name = ctx.output_pin_name().text
        try:
            self.__sim.add_block(
                AND2(block_name, [input0_name, input1_name], [output_name]))
        except Exception as e:
            self.__set_error(ctx, e)

    def exitCreate_state_block(self, ctx: FileSyntaxParser
                               .Create_state_blockContext):
        if self.error_is_set():
            return
        pin_type = ctx.pin_type().pin_type
        block_name = ctx.block_name().text
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

    def exitCreate_edge(self, ctx: FileSyntaxParser
                        .Create_edgeContext):
        node0 = ctx.node(0).text
        node1 = ctx.node(1).text
        try:
            self.__sim.add_edge(node0, node1)
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
        self.__sim.add_condition(conditions)

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

    def exitShow_blocks(self, ctx:FileSyntaxParser.Show_blocksContext):
        self.__sim.show_all_blocks()

    def exitShow_edges(self, ctx:FileSyntaxParser.Show_edgesContext):
        self.__sim.show_all_edges()
