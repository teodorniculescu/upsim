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


    # Visit a parse tree produced by FileSyntaxParser#block.
    def visitBlock(self, ctx:FileSyntaxParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#and2_block.
    def visitAnd2_block(self, ctx:FileSyntaxParser.And2_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#state_block.
    def visitState_block(self, ctx:FileSyntaxParser.State_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#insert_edges.
    def visitInsert_edges(self, ctx:FileSyntaxParser.Insert_edgesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#edge.
    def visitEdge(self, ctx:FileSyntaxParser.EdgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FileSyntaxParser#node.
    def visitNode(self, ctx:FileSyntaxParser.NodeContext):
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



del FileSyntaxParser