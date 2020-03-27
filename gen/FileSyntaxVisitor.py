# Generated from C:/Users/teodo/PycharmProjects/upsim\FileSyntax.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FileSyntaxParser import FileSyntaxParser
else:
    from FileSyntaxParser import FileSyntaxParser

# This class defines a complete generic visitor for a parse tree produced by FileSyntaxParser.

class FileSyntaxVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FileSyntaxParser#filesyntax.
    def visitFilesyntax(self, ctx:FileSyntaxParser.FilesyntaxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#insert.
    def visitInsert(self, ctx:FileSyntaxParser.InsertContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#insert_blocks.
    def visitInsert_blocks(self, ctx:FileSyntaxParser.Insert_blocksContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#create_block.
    def visitCreate_block(self, ctx:FileSyntaxParser.Create_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#create_and2_block.
    def visitCreate_and2_block(self, ctx:FileSyntaxParser.Create_and2_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#create_state_block.
    def visitCreate_state_block(self, ctx:FileSyntaxParser.Create_state_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#input_pin_name.
    def visitInput_pin_name(self, ctx:FileSyntaxParser.Input_pin_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#output_pin_name.
    def visitOutput_pin_name(self, ctx:FileSyntaxParser.Output_pin_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#io_pin_name.
    def visitIo_pin_name(self, ctx:FileSyntaxParser.Io_pin_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#insert_edges.
    def visitInsert_edges(self, ctx:FileSyntaxParser.Insert_edgesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#create_edge.
    def visitCreate_edge(self, ctx:FileSyntaxParser.Create_edgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#insert_initial_conditions.
    def visitInsert_initial_conditions(self, ctx:FileSyntaxParser.Insert_initial_conditionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#initial_condition.
    def visitInitial_condition(self, ctx:FileSyntaxParser.Initial_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#condition.
    def visitCondition(self, ctx:FileSyntaxParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#node.
    def visitNode(self, ctx:FileSyntaxParser.NodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#block_name.
    def visitBlock_name(self, ctx:FileSyntaxParser.Block_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#pin_name.
    def visitPin_name(self, ctx:FileSyntaxParser.Pin_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#node_value.
    def visitNode_value(self, ctx:FileSyntaxParser.Node_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#run.
    def visitRun(self, ctx:FileSyntaxParser.RunContext):
        return self.visitChildren(ctx)



del FileSyntaxParser