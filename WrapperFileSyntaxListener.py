from blocks.StateBlock import StateBlock
from gen.FileSyntaxListener import FileSyntaxListener
from gen.FileSyntaxParser import FileSyntaxParser
from Simulation import Simulation
from saved_blocks.AND2 import AND2


class WrapperFileSyntaxListener(FileSyntaxListener):
    __sim: Simulation

    def __init__(self, sim: Simulation):
        self.__sim = sim

    def exitCreate_and2_block(self, ctx: FileSyntaxParser.Create_and2_blockContext):
        block_name = ctx.block_name().text
        input0_name = ctx.input_pin_name(0).text
        input1_name = ctx.input_pin_name(1).text
        output_name = ctx.output_pin_name().text
        block = AND2(block_name, [input0_name, input1_name], [output_name])
        self.__sim.add_logical_block(block)

    def exitCreate_state_block(self, ctx: FileSyntaxParser.Create_state_blockContext):
        block_name = ctx.block_name().text
        io_name = ctx.io_pin_name().text
        block = StateBlock(block_name, io_name)
        self.__sim.add_state_block(block)

    def exitBlock_name(self, ctx: FileSyntaxParser.Block_nameContext):
        ctx.text = str(ctx.NAME())

    def exitInput_pin_name(self, ctx: FileSyntaxParser.Input_pin_nameContext):
        ctx.text = str(ctx.NAME())

    def exitOutput_pin_name(self, ctx: FileSyntaxParser.Output_pin_nameContext):
        ctx.text = str(ctx.NAME())

    def exitIo_pin_name(self, ctx: FileSyntaxParser.Io_pin_nameContext):
        ctx.text = str(ctx.NAME())

