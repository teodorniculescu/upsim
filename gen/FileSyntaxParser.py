# Generated from C:/Users/teodo/PycharmProjects/upsim\FileSyntax.g4 by ANTLR 4.8
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\32")
        buf.write("m\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\3\2\7\2")
        buf.write("\34\n\2\f\2\16\2\37\13\2\3\2\3\2\3\3\3\3\3\3\3\3\5\3\'")
        buf.write("\n\3\3\3\3\3\3\4\3\4\3\4\3\4\7\4/\n\4\f\4\16\4\62\13\4")
        buf.write("\3\5\3\5\5\5\66\n\5\3\6\3\6\3\6\3\6\3\6\3\6\3\7\3\7\3")
        buf.write("\7\3\7\3\b\3\b\3\b\3\b\7\bF\n\b\f\b\16\bI\13\b\3\t\3\t")
        buf.write("\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\6\13")
        buf.write("X\n\13\r\13\16\13Y\3\f\3\f\3\f\3\f\7\f`\n\f\f\f\16\fc")
        buf.write("\13\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\3\r\2\2\16\2\4\6")
        buf.write("\b\n\f\16\20\22\24\26\30\2\2\2h\2\35\3\2\2\2\4\"\3\2\2")
        buf.write("\2\6*\3\2\2\2\b\65\3\2\2\2\n\67\3\2\2\2\f=\3\2\2\2\16")
        buf.write("A\3\2\2\2\20J\3\2\2\2\22O\3\2\2\2\24S\3\2\2\2\26[\3\2")
        buf.write("\2\2\30f\3\2\2\2\32\34\5\4\3\2\33\32\3\2\2\2\34\37\3\2")
        buf.write("\2\2\35\33\3\2\2\2\35\36\3\2\2\2\36 \3\2\2\2\37\35\3\2")
        buf.write("\2\2 !\7\2\2\3!\3\3\2\2\2\"&\7\20\2\2#\'\5\6\4\2$\'\5")
        buf.write("\16\b\2%\'\5\24\13\2&#\3\2\2\2&$\3\2\2\2&%\3\2\2\2\'(")
        buf.write("\3\2\2\2()\7\3\2\2)\5\3\2\2\2*+\7\r\2\2+\60\5\b\5\2,-")
        buf.write("\7\4\2\2-/\5\b\5\2.,\3\2\2\2/\62\3\2\2\2\60.\3\2\2\2\60")
        buf.write("\61\3\2\2\2\61\7\3\2\2\2\62\60\3\2\2\2\63\66\5\f\7\2\64")
        buf.write("\66\5\n\6\2\65\63\3\2\2\2\65\64\3\2\2\2\66\t\3\2\2\2\67")
        buf.write("8\7\21\2\289\7\26\2\29:\7\26\2\2:;\7\26\2\2;<\7\26\2\2")
        buf.write("<\13\3\2\2\2=>\7\f\2\2>?\7\26\2\2?@\7\26\2\2@\r\3\2\2")
        buf.write("\2AB\7\16\2\2BG\5\20\t\2CD\7\4\2\2DF\5\20\t\2EC\3\2\2")
        buf.write("\2FI\3\2\2\2GE\3\2\2\2GH\3\2\2\2H\17\3\2\2\2IG\3\2\2\2")
        buf.write("JK\7\22\2\2KL\5\22\n\2LM\7\23\2\2MN\5\22\n\2N\21\3\2\2")
        buf.write("\2OP\7\26\2\2PQ\7\5\2\2QR\7\26\2\2R\23\3\2\2\2ST\7\17")
        buf.write("\2\2TW\5\26\f\2UV\7\4\2\2VX\5\26\f\2WU\3\2\2\2XY\3\2\2")
        buf.write("\2YW\3\2\2\2YZ\3\2\2\2Z\25\3\2\2\2[\\\7\6\2\2\\a\5\30")
        buf.write("\r\2]^\7\4\2\2^`\5\30\r\2_]\3\2\2\2`c\3\2\2\2a_\3\2\2")
        buf.write("\2ab\3\2\2\2bd\3\2\2\2ca\3\2\2\2de\7\7\2\2e\27\3\2\2\2")
        buf.write("fg\7\26\2\2gh\7\5\2\2hi\7\26\2\2ij\7\b\2\2jk\7\25\2\2")
        buf.write("k\31\3\2\2\2\t\35&\60\65GYa")
        return buf.getvalue()


class FileSyntaxParser ( Parser ):

    grammarFileName = "FileSyntax.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "','", "'.'", "'('", "')'", "'='", 
                     "'OUT'", "'IN'", "'INOUT'", "'STATE'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'INSERT'", "'AND2'", "'BETWEEN'", 
                     "'AND'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "OUTPUT_KWD", 
                      "INPUT_KWD", "INPUT_OUTPUT_KWD", "STATE_KWD", "BLOCK_KWD", 
                      "EDGE_KWD", "INITIAL_CONDITIONS_KWD", "INSERT_KWD", 
                      "AND2_KWD", "BETWEEN_KWD", "AND_KWD", "PIN_TYPE", 
                      "INTEGER", "NAME", "COMMENT", "WHITESPACE", "NEWLINE", 
                      "ANY" ]

    RULE_filesyntax = 0
    RULE_insert = 1
    RULE_insert_blocks = 2
    RULE_block = 3
    RULE_and2_block = 4
    RULE_state_block = 5
    RULE_insert_edges = 6
    RULE_edge = 7
    RULE_node = 8
    RULE_insert_initial_conditions = 9
    RULE_initial_condition = 10
    RULE_condition = 11

    ruleNames =  [ "filesyntax", "insert", "insert_blocks", "block", "and2_block", 
                   "state_block", "insert_edges", "edge", "node", "insert_initial_conditions", 
                   "initial_condition", "condition" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    OUTPUT_KWD=7
    INPUT_KWD=8
    INPUT_OUTPUT_KWD=9
    STATE_KWD=10
    BLOCK_KWD=11
    EDGE_KWD=12
    INITIAL_CONDITIONS_KWD=13
    INSERT_KWD=14
    AND2_KWD=15
    BETWEEN_KWD=16
    AND_KWD=17
    PIN_TYPE=18
    INTEGER=19
    NAME=20
    COMMENT=21
    WHITESPACE=22
    NEWLINE=23
    ANY=24

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class FilesyntaxContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(FileSyntaxParser.EOF, 0)

        def insert(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FileSyntaxParser.InsertContext)
            else:
                return self.getTypedRuleContext(FileSyntaxParser.InsertContext,i)


        def getRuleIndex(self):
            return FileSyntaxParser.RULE_filesyntax

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFilesyntax" ):
                listener.enterFilesyntax(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFilesyntax" ):
                listener.exitFilesyntax(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFilesyntax" ):
                return visitor.visitFilesyntax(self)
            else:
                return visitor.visitChildren(self)




    def filesyntax(self):

        localctx = FileSyntaxParser.FilesyntaxContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_filesyntax)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==FileSyntaxParser.INSERT_KWD:
                self.state = 24
                self.insert()
                self.state = 29
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 30
            self.match(FileSyntaxParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InsertContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INSERT_KWD(self):
            return self.getToken(FileSyntaxParser.INSERT_KWD, 0)

        def insert_blocks(self):
            return self.getTypedRuleContext(FileSyntaxParser.Insert_blocksContext,0)


        def insert_edges(self):
            return self.getTypedRuleContext(FileSyntaxParser.Insert_edgesContext,0)


        def insert_initial_conditions(self):
            return self.getTypedRuleContext(FileSyntaxParser.Insert_initial_conditionsContext,0)


        def getRuleIndex(self):
            return FileSyntaxParser.RULE_insert

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInsert" ):
                listener.enterInsert(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInsert" ):
                listener.exitInsert(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInsert" ):
                return visitor.visitInsert(self)
            else:
                return visitor.visitChildren(self)




    def insert(self):

        localctx = FileSyntaxParser.InsertContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_insert)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 32
            self.match(FileSyntaxParser.INSERT_KWD)
            self.state = 36
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [FileSyntaxParser.BLOCK_KWD]:
                self.state = 33
                self.insert_blocks()
                pass
            elif token in [FileSyntaxParser.EDGE_KWD]:
                self.state = 34
                self.insert_edges()
                pass
            elif token in [FileSyntaxParser.INITIAL_CONDITIONS_KWD]:
                self.state = 35
                self.insert_initial_conditions()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 38
            self.match(FileSyntaxParser.T__0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Insert_blocksContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BLOCK_KWD(self):
            return self.getToken(FileSyntaxParser.BLOCK_KWD, 0)

        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FileSyntaxParser.BlockContext)
            else:
                return self.getTypedRuleContext(FileSyntaxParser.BlockContext,i)


        def getRuleIndex(self):
            return FileSyntaxParser.RULE_insert_blocks

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInsert_blocks" ):
                listener.enterInsert_blocks(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInsert_blocks" ):
                listener.exitInsert_blocks(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInsert_blocks" ):
                return visitor.visitInsert_blocks(self)
            else:
                return visitor.visitChildren(self)




    def insert_blocks(self):

        localctx = FileSyntaxParser.Insert_blocksContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_insert_blocks)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self.match(FileSyntaxParser.BLOCK_KWD)
            self.state = 41
            self.block()
            self.state = 46
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==FileSyntaxParser.T__1:
                self.state = 42
                self.match(FileSyntaxParser.T__1)
                self.state = 43
                self.block()
                self.state = 48
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def state_block(self):
            return self.getTypedRuleContext(FileSyntaxParser.State_blockContext,0)


        def and2_block(self):
            return self.getTypedRuleContext(FileSyntaxParser.And2_blockContext,0)


        def getRuleIndex(self):
            return FileSyntaxParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = FileSyntaxParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_block)
        try:
            self.state = 51
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [FileSyntaxParser.STATE_KWD]:
                self.enterOuterAlt(localctx, 1)
                self.state = 49
                self.state_block()
                pass
            elif token in [FileSyntaxParser.AND2_KWD]:
                self.enterOuterAlt(localctx, 2)
                self.state = 50
                self.and2_block()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class And2_blockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AND2_KWD(self):
            return self.getToken(FileSyntaxParser.AND2_KWD, 0)

        def NAME(self, i:int=None):
            if i is None:
                return self.getTokens(FileSyntaxParser.NAME)
            else:
                return self.getToken(FileSyntaxParser.NAME, i)

        def getRuleIndex(self):
            return FileSyntaxParser.RULE_and2_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnd2_block" ):
                listener.enterAnd2_block(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnd2_block" ):
                listener.exitAnd2_block(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnd2_block" ):
                return visitor.visitAnd2_block(self)
            else:
                return visitor.visitChildren(self)




    def and2_block(self):

        localctx = FileSyntaxParser.And2_blockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_and2_block)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self.match(FileSyntaxParser.AND2_KWD)
            self.state = 54
            self.match(FileSyntaxParser.NAME)
            self.state = 55
            self.match(FileSyntaxParser.NAME)
            self.state = 56
            self.match(FileSyntaxParser.NAME)
            self.state = 57
            self.match(FileSyntaxParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class State_blockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STATE_KWD(self):
            return self.getToken(FileSyntaxParser.STATE_KWD, 0)

        def NAME(self, i:int=None):
            if i is None:
                return self.getTokens(FileSyntaxParser.NAME)
            else:
                return self.getToken(FileSyntaxParser.NAME, i)

        def getRuleIndex(self):
            return FileSyntaxParser.RULE_state_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterState_block" ):
                listener.enterState_block(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitState_block" ):
                listener.exitState_block(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitState_block" ):
                return visitor.visitState_block(self)
            else:
                return visitor.visitChildren(self)




    def state_block(self):

        localctx = FileSyntaxParser.State_blockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_state_block)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            self.match(FileSyntaxParser.STATE_KWD)
            self.state = 60
            self.match(FileSyntaxParser.NAME)
            self.state = 61
            self.match(FileSyntaxParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Insert_edgesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EDGE_KWD(self):
            return self.getToken(FileSyntaxParser.EDGE_KWD, 0)

        def edge(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FileSyntaxParser.EdgeContext)
            else:
                return self.getTypedRuleContext(FileSyntaxParser.EdgeContext,i)


        def getRuleIndex(self):
            return FileSyntaxParser.RULE_insert_edges

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInsert_edges" ):
                listener.enterInsert_edges(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInsert_edges" ):
                listener.exitInsert_edges(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInsert_edges" ):
                return visitor.visitInsert_edges(self)
            else:
                return visitor.visitChildren(self)




    def insert_edges(self):

        localctx = FileSyntaxParser.Insert_edgesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_insert_edges)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.match(FileSyntaxParser.EDGE_KWD)
            self.state = 64
            self.edge()
            self.state = 69
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==FileSyntaxParser.T__1:
                self.state = 65
                self.match(FileSyntaxParser.T__1)
                self.state = 66
                self.edge()
                self.state = 71
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EdgeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BETWEEN_KWD(self):
            return self.getToken(FileSyntaxParser.BETWEEN_KWD, 0)

        def node(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FileSyntaxParser.NodeContext)
            else:
                return self.getTypedRuleContext(FileSyntaxParser.NodeContext,i)


        def AND_KWD(self):
            return self.getToken(FileSyntaxParser.AND_KWD, 0)

        def getRuleIndex(self):
            return FileSyntaxParser.RULE_edge

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEdge" ):
                listener.enterEdge(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEdge" ):
                listener.exitEdge(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEdge" ):
                return visitor.visitEdge(self)
            else:
                return visitor.visitChildren(self)




    def edge(self):

        localctx = FileSyntaxParser.EdgeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_edge)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.match(FileSyntaxParser.BETWEEN_KWD)
            self.state = 73
            self.node()
            self.state = 74
            self.match(FileSyntaxParser.AND_KWD)
            self.state = 75
            self.node()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NodeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self, i:int=None):
            if i is None:
                return self.getTokens(FileSyntaxParser.NAME)
            else:
                return self.getToken(FileSyntaxParser.NAME, i)

        def getRuleIndex(self):
            return FileSyntaxParser.RULE_node

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNode" ):
                listener.enterNode(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNode" ):
                listener.exitNode(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNode" ):
                return visitor.visitNode(self)
            else:
                return visitor.visitChildren(self)




    def node(self):

        localctx = FileSyntaxParser.NodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_node)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 77
            self.match(FileSyntaxParser.NAME)
            self.state = 78
            self.match(FileSyntaxParser.T__2)
            self.state = 79
            self.match(FileSyntaxParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Insert_initial_conditionsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INITIAL_CONDITIONS_KWD(self):
            return self.getToken(FileSyntaxParser.INITIAL_CONDITIONS_KWD, 0)

        def initial_condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FileSyntaxParser.Initial_conditionContext)
            else:
                return self.getTypedRuleContext(FileSyntaxParser.Initial_conditionContext,i)


        def getRuleIndex(self):
            return FileSyntaxParser.RULE_insert_initial_conditions

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInsert_initial_conditions" ):
                listener.enterInsert_initial_conditions(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInsert_initial_conditions" ):
                listener.exitInsert_initial_conditions(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInsert_initial_conditions" ):
                return visitor.visitInsert_initial_conditions(self)
            else:
                return visitor.visitChildren(self)




    def insert_initial_conditions(self):

        localctx = FileSyntaxParser.Insert_initial_conditionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_insert_initial_conditions)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self.match(FileSyntaxParser.INITIAL_CONDITIONS_KWD)
            self.state = 82
            self.initial_condition()
            self.state = 85 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 83
                self.match(FileSyntaxParser.T__1)
                self.state = 84
                self.initial_condition()
                self.state = 87 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==FileSyntaxParser.T__1):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Initial_conditionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FileSyntaxParser.ConditionContext)
            else:
                return self.getTypedRuleContext(FileSyntaxParser.ConditionContext,i)


        def getRuleIndex(self):
            return FileSyntaxParser.RULE_initial_condition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInitial_condition" ):
                listener.enterInitial_condition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInitial_condition" ):
                listener.exitInitial_condition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInitial_condition" ):
                return visitor.visitInitial_condition(self)
            else:
                return visitor.visitChildren(self)




    def initial_condition(self):

        localctx = FileSyntaxParser.Initial_conditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_initial_condition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 89
            self.match(FileSyntaxParser.T__3)
            self.state = 90
            self.condition()
            self.state = 95
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==FileSyntaxParser.T__1:
                self.state = 91
                self.match(FileSyntaxParser.T__1)
                self.state = 92
                self.condition()
                self.state = 97
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 98
            self.match(FileSyntaxParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self, i:int=None):
            if i is None:
                return self.getTokens(FileSyntaxParser.NAME)
            else:
                return self.getToken(FileSyntaxParser.NAME, i)

        def INTEGER(self):
            return self.getToken(FileSyntaxParser.INTEGER, 0)

        def getRuleIndex(self):
            return FileSyntaxParser.RULE_condition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondition" ):
                listener.enterCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondition" ):
                listener.exitCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondition" ):
                return visitor.visitCondition(self)
            else:
                return visitor.visitChildren(self)




    def condition(self):

        localctx = FileSyntaxParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 100
            self.match(FileSyntaxParser.NAME)
            self.state = 101
            self.match(FileSyntaxParser.T__2)
            self.state = 102
            self.match(FileSyntaxParser.NAME)
            self.state = 103
            self.match(FileSyntaxParser.T__5)
            self.state = 104
            self.match(FileSyntaxParser.INTEGER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





