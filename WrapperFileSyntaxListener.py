from gen.FileSyntaxListener import FileSyntaxListener
from gen.FileSyntaxParser import FileSyntaxParser


class WrapperFileSyntaxListener(FileSyntaxListener):
    def __init__(self):
        pass

    def enterInsert_blocks(self, ctx:FileSyntaxParser.Insert_blocksContext):
        print("aseara in gara")

    def exitInsert_blocks(self, ctx:FileSyntaxParser.Insert_blocksContext):
        print("gara de nord")

    def enterState_block(self, ctx:FileSyntaxParser.State_blockContext):
        afis = ""
        afis += str(ctx.NAME(0))
        afis += str(ctx.NAME(1))
        afis += str(ctx.STATE_KWD())
        print(afis)
