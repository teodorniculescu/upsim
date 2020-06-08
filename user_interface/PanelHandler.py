from kivy.uix.widget import Widget
from typing import Dict, Any
from user_interface.cell.EmptyCell import EmptyCell
from user_interface.cell.BorderCell import *
from user_interface.cell.WireCell import WireCell
from user_interface.cell.VoidCell import VoidCell
from user_interface.cell.TextCell import TextCell


class CODE:
    VOID: str = ""

    EMPTY: str = "e"

    TEXT: str = "t"

    BORDER_LEFT: str = "b_l"
    BORDER_RIGHT: str = "b_r"
    BORDER_UP: str = "b_u"
    BORDER_DOWN: str = "b_d"
    BORDER_LEFT_UP: str = "b_lu"
    BORDER_LEFT_DOWN: str = "b_ld"
    BORDER_RIGHT_UP: str = "b_ru"
    BORDER_RIGHT_DOWN: str = "b_rd"

    WIRE_LEFT_RIGHT: str = "w_lr"
    WIRE_UP_DOWN: str = "w_ud"
    WIRE_LEFT: str = "w_l"
    WIRE_LEFT_UP: str = "w_lu"
    WIRE_LEFT_DOWN: str = "w_ld"
    WIRE_RIGHT: str = "w_r"
    WIRE_RIGHT_UP: str = "w_ru"
    WIRE_RIGHT_DOWN: str = "w_rd"


class PanelHandler:
    background_color: ColorType
    __code_dict: Dict[str, Any] = {
        CODE.BORDER_LEFT: LeftBorderCell,
        CODE.BORDER_LEFT_UP: LeftUpBorderCell,
        CODE.BORDER_LEFT_DOWN: LeftDownBorderCell,
        CODE.BORDER_RIGHT: RightBorderCell,
        CODE.BORDER_RIGHT_UP: RightUpBorderCell,
        CODE.BORDER_RIGHT_DOWN: RightDownBorderCell,
        CODE.BORDER_UP: UpBorderCell,
        CODE.BORDER_DOWN: DownBorderCell,

        CODE.WIRE_RIGHT: WireCell.Right,
        CODE.WIRE_RIGHT_DOWN: WireCell.RightDown,
        CODE.WIRE_RIGHT_UP: WireCell.RightUp,
        CODE.WIRE_LEFT: WireCell.Left,
        CODE.WIRE_LEFT_DOWN: WireCell.LeftDown,
        CODE.WIRE_LEFT_UP: WireCell.LeftUp,
        CODE.WIRE_LEFT_RIGHT: WireCell.LeftRight,
        CODE.WIRE_UP_DOWN: WireCell.UpDown,

        CODE.TEXT: TextCell,

        CODE.VOID: VoidCell,

        CODE.EMPTY: EmptyCell
    }

    def __init__(self):
        pass

    def get_cell(self, code: str, parameters: Dict[str, str]) -> Widget:
        return self.__code_dict[code](parameters=parameters)
