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


class PanelHandler:
    background_color: ColorType
    __code_dict: Dict[str, Callable[[], Widget]] = {
        CODE.EMPTY: EmptyCell,
        CODE.BORDER_LEFT: LeftBorderCell,
        CODE.BORDER_LEFT_UP: LeftUpBorderCell,
        CODE.BORDER_LEFT_DOWN: LeftDownBorderCell,
        CODE.BORDER_RIGHT: RightBorderCell,
        CODE.BORDER_RIGHT_UP: RightUpBorderCell,
        CODE.BORDER_RIGHT_DOWN: RightDownBorderCell,
        CODE.BORDER_UP: UpBorderCell,
        CODE.BORDER_DOWN: DownBorderCell
    }

    def __init__(self):
        pass

    def get_cell(self, code: str) -> Widget:
        return self.__code_dict[code]()
