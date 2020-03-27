import sys
from blocks.StateBlock import StateBlock
from gen.FileSyntaxListener import FileSyntaxListener
from gen.FileSyntaxParser import FileSyntaxParser
from Simulation import Simulation
from saved_blocks.AND2 import AND2


class WrapperFileSyntaxListener(FileSyntaxListener):
    __sim: Simulation
    __output: type(sys.stdout)

    def __init__(self, sim: Simulation, output: type(sys.stdout)):
        self.__sim = sim
        self.__output = output

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

    def exitPin_name(self, ctx: FileSyntaxParser.Pin_nameContext):
        ctx.text = str(ctx.NAME())

    def exitNode(self, ctx: FileSyntaxParser.NodeContext):
        block_name = ctx.block_name().text
        pin_name = ctx.pin_name().text
        ctx.text = block_name + "." + pin_name

    def exitCreate_edge(self, ctx: FileSyntaxParser.Create_edgeContext):
        node0 = ctx.node(0).text
        node1 = ctx.node(1).text
        self.__sim.add_edge(node0, node1)

    def exitNode_value(self, ctx: FileSyntaxParser.Node_valueContext):
        ctx.number = str(ctx.INTEGER())

    def exitCondition(self, ctx: FileSyntaxParser.ConditionContext):
        ctx.node = ctx.node().text
        ctx.number = ctx.node_value().number

    def exitInitial_condition(self, ctx: FileSyntaxParser.Initial_conditionContext):
        condition_list = []
        for condition in ctx.condition():
            condition_list.append((condition.node, condition.number))
        self.__sim.add_condition(condition_list)

    def exitRun(self, ctx: FileSyntaxParser.RunContext):
        self.__sim.run()
