from typing import Tuple, List, Dict
from user_interface.DataStructure import ParamElem
from user_interface.PanelHandler import PanelHandler, CODE
from blocks.BasicBlock import BasicBlock
from kivy.uix.widget import Widget
from values.BaseValue import BaseValue
from simulation.Node import Node
from values.BaseValue import RIGHT, UP, DOWN, LEFT
from antlr.FileSyntaxErrorListener import \
    ERROR_INVALID_DIRECTION_STRING, \
    ERROR_GRID_OUT_OF_BOUNDS

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

    def __move_right(self, orig_pos: Tuple[int, int]) -> Tuple[int, int]:
        return (
            orig_pos[0],
            orig_pos[1] + 1
        )

    def __move_left(self, orig_pos: Tuple[int, int]) -> Tuple[int, int]:
        return (
            orig_pos[0],
            orig_pos[1] - 1
        )

    def __move_up(self, orig_pos: Tuple[int, int]) -> Tuple[int, int]:
        return (
            orig_pos[0] - 1,
            orig_pos[1]
        )

    def __move_down(self, orig_pos: Tuple[int, int]) -> Tuple[int, int]:
        return (
            orig_pos[0] + 1,
            orig_pos[1]
        )

    def __move(self, direction: int, node: Node, position: Tuple[int, int]) -> Tuple[int, int]:
        if direction == RIGHT:
            position = self.__move_right(position)
        elif direction == LEFT:
            if position[0] <= 0:
                raise Exception(ERROR_GRID_OUT_OF_BOUNDS % node.__str__(), "LEFT", str(position))
            position = self.__move_left(position)
        elif direction == DOWN:
            position = self.__move_down(position)
        elif direction == UP:
            if position[1] <= 0:
                raise Exception(ERROR_GRID_OUT_OF_BOUNDS % node.__str__(), "UP", str(position))
            position = self.__move_up(position)
        else:
            raise Exception(ERROR_INVALID_DIRECTION_STRING)
        return position

    def __set_prev_code(self, pos: Tuple[int, int], direction: int) -> None:
        prev_value = self.__matrix[pos[0]][pos[1]]
        if prev_value == CODE.WIRE_UP:
            if direction == DOWN:
                value = CODE.WIRE_UP_DOWN
            elif direction == LEFT:
                value = CODE.WIRE_LEFT_UP
            elif direction == RIGHT:
                value = CODE.WIRE_RIGHT_UP
            else:
                raise Exception(ERROR_INVALID_DIRECTION_STRING)
        elif prev_value == CODE.WIRE_DOWN:
            if direction == UP:
                value = CODE.WIRE_UP_DOWN
            elif direction == LEFT:
                value = CODE.WIRE_LEFT_DOWN
            elif direction == RIGHT:
                value = CODE.WIRE_RIGHT_DOWN
            else:
                raise Exception(ERROR_INVALID_DIRECTION_STRING)
        elif prev_value == CODE.WIRE_RIGHT:
            if direction == UP:
                value = CODE.WIRE_RIGHT_UP
            elif direction == DOWN:
                value = CODE.WIRE_RIGHT_DOWN
            elif direction == LEFT:
                value = CODE.WIRE_LEFT_RIGHT
            else:
                raise Exception(ERROR_INVALID_DIRECTION_STRING)
        elif prev_value == CODE.WIRE_LEFT:
            if direction == UP:
                value = CODE.WIRE_LEFT_UP
            elif direction == DOWN:
                value = CODE.WIRE_LEFT_DOWN
            elif direction == RIGHT:
                value = CODE.WIRE_LEFT_RIGHT
            else:
                raise Exception(ERROR_INVALID_DIRECTION_STRING)
        else:
            raise Exception(ERROR_INVALID_DIRECTION_STRING)
        self.__matrix[pos[0]][pos[1]] = value

    def __set_new_code(self, pos: Tuple[int, int], direction: int) -> None:
        prev_value = self.__matrix[pos[0]][pos[1]]
        if prev_value == CODE.VOID:
            if direction == UP:
                value = CODE.WIRE_DOWN
            elif direction == DOWN:
                value = CODE.WIRE_UP
            elif direction == LEFT:
                value = CODE.WIRE_RIGHT
            elif direction == RIGHT:
                value = CODE.WIRE_LEFT
            else:
                raise Exception(ERROR_INVALID_DIRECTION_STRING)
        elif prev_value == CODE.WIRE_UP:
            if direction == DOWN:
                value = CODE.WIRE_UP_DOWN
            elif direction == LEFT:
                value = CODE.WIRE_LEFT_UP
            elif direction == RIGHT:
                value = CODE.WIRE_RIGHT_UP
            else:
                raise Exception(ERROR_INVALID_DIRECTION_STRING)
        elif prev_value == CODE.WIRE_DOWN:
            if direction == UP:
                value = CODE.WIRE_UP_DOWN
            elif direction == LEFT:
                value = CODE.WIRE_LEFT_DOWN
            elif direction == RIGHT:
                value = CODE.WIRE_RIGHT_DOWN
            else:
                raise Exception(ERROR_INVALID_DIRECTION_STRING)
        elif prev_value == CODE.WIRE_RIGHT:
            if direction == UP:
                value = CODE.WIRE_RIGHT_UP
            elif direction == DOWN:
                value = CODE.WIRE_RIGHT_DOWN
            elif direction == RIGHT:
                value = CODE.WIRE_LEFT_RIGHT
            else:
                raise Exception(ERROR_INVALID_DIRECTION_STRING)
        elif prev_value == CODE.WIRE_LEFT:
            if direction == UP:
                value = CODE.WIRE_LEFT_UP
            elif direction == DOWN:
                value = CODE.WIRE_LEFT_DOWN
            elif direction == RIGHT:
                value = CODE.WIRE_LEFT_RIGHT
            else:
                raise Exception(ERROR_INVALID_DIRECTION_STRING)
        else:
            print(prev_value)
            raise Exception(ERROR_INVALID_DIRECTION_STRING)
        self.__matrix[pos[0]][pos[1]] = value

    def add_edges(self, nodes_dict: Dict[str, Node]) -> None:
        for node in nodes_dict.values():
            pin = node.get_pin()
            original_position = pin.get_original_position()
            new_position = original_position
            for direction in pin.get_directions_list():
                # save the previous position
                prev_position = new_position
                new_position = self.__move(direction, node, new_position)
                self.__set_prev_code(pos=prev_position, direction=direction)
                self.__set_new_code(pos=new_position, direction=direction)
                print(new_position)



