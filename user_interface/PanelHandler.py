from kivy.uix.widget import Widget
from typing import Dict, Callable
from user_interface.EmptyCell import EmptyCell
from user_interface.BorderCell import *


class CODE:
    EMPTY: str = ""
    BORDER_LEFT: str = "b_l"
    BORDER_RIGHT: str = "b_r"
    BORDER_UP: str = "b_u"
    BORDER_DOWN: str = "b_d"
    BORDER_LEFT_UP: str = "b_lu"
    BORDER_LEFT_DOWN: str = "b_ld"
    BORDER_RIGHT_UP: str = "b_ru"
    BORDER_RIGHT_DOWN: str = "b_rd"


def get_empty_cell() -> EmptyCell:
    return EmptyCell()


def get_left_border_cell() -> BorderCell:
    return LeftBorderCell()


def get_left_up_border_cell() -> BorderCell:
    return LeftUpBorderCell()


def get_left_down_border_cell() -> BorderCell:
    return LeftDownBorderCell()


def get_right_border_cell() -> BorderCell:
    return RightBorderCell()


def get_right_up_border_cell() -> BorderCell:
    return RightUpBorderCell()


def get_right_down_border_cell() -> BorderCell:
    return RightDownBorderCell()


def get_up_border_cell() -> BorderCell:
    return UpBorderCell()


def get_down_border_cell() -> BorderCell:
    return DownBorderCell()


class PanelHandler:
    background_color: ColorType
    __code_dict: Dict[str, Callable[[], Widget]] = {
        CODE.EMPTY: get_empty_cell,
        CODE.BORDER_LEFT: get_left_border_cell,
        CODE.BORDER_LEFT_UP: get_left_up_border_cell,
        CODE.BORDER_LEFT_DOWN: get_left_down_border_cell,
        CODE.BORDER_RIGHT: get_right_border_cell,
        CODE.BORDER_RIGHT_UP: get_right_up_border_cell,
        CODE.BORDER_RIGHT_DOWN: get_right_down_border_cell,
        CODE.BORDER_UP: get_up_border_cell,
        CODE.BORDER_DOWN: get_down_border_cell
    }

    def __init__(self):
        pass

    def get_cell(self, code: str) -> Widget:
        return self.__code_dict[code]()
