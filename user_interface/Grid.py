from typing import Tuple, List, Dict
from user_interface.DataStructure import ParamElem
from user_interface.PanelHandler import PanelHandler, CODE
from blocks.BasicBlock import BasicBlock
from kivy.uix.widget import Widget
from values.BaseValue import BaseValue
from simulation.Node import Node
from values.BaseValue import RIGHT, UP, DOWN, LEFT
from antlr.FileSyntaxErrorListener import ERROR_INVALID_DIRECTION_STRING

from gen.FileSyntaxLexer import FileSyntaxLexer

class Grid:
    __size: Tuple[int, int]
    # This matrix stores strings which describe the type of block
    # that is stored in that position.
    # Strings are used instead of EmptyCells because EmptyCells update
    # depending on their position in the simulation grid, which means
    # they cause problems when when they are not used.
    # Also, strings take up less memory than emtpy cells.
    __matrix: List[List[str]]
    __parameter: Dict[Tuple[int, int], ParamElem]
    __ph: PanelHandler

    def __init__(self, size: Tuple[int, int] = (1, 1)):
        self.__size = size
        self.__ph = PanelHandler()
        # creating a matrix of size[0] rows and size[1] columns
        self.__matrix = []
        self.__parameter = {}
        for row_index in range(self.__size[0]):
            row: List[str] = []
            for col_index in range(self.__size[1]):
                row.append("")
            self.__matrix.append(row)

    def add_blocks(self, blocks_dict: Dict[str, BasicBlock]) -> None:
        for block in blocks_dict.values():
            position = block.get_position()
            matrix = block.get_gui_grid()
            num_rows = len(matrix)
            num_cols = len(matrix[0])
            for row_index in range(num_rows):
                for col_index in range(num_cols):
                    (cell_type, cell_param) = matrix[row_index][col_index]
                    # real matrix position
                    rmp = (position[0] + row_index, position[1] + col_index)
                    self.__matrix[rmp[0]][rmp[1]] = cell_type
                    self.__parameter[rmp] = cell_param

    def get_cell_widget(self, index: Tuple[int, int]) -> Widget:
        str_code: str = self.__matrix[index[0]][index[1]]
        parameters: ParamElem = self.__parameter[index] if index in self.__parameter else {}
        return self.__ph.get_cell(str_code, parameters)

    def add_edges(self, nodes_dict: Dict[str, Node]) -> None:
        for node in nodes_dict.values():
            pin = node.get_pin()
            original_position = pin.get_original_position()
            for direction in pin.get_directions_list():
                if direction == RIGHT:
                    print("right nigga")
                elif direction == LEFT:
                    print("left nigga")
                elif direction == DOWN:
                    print("down nigga")
                elif direction == UP:
                    print("up nigga")
                else:
                    raise Exception(ERROR_INVALID_DIRECTION_STRING)
