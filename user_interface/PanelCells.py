from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from typing import Tuple, Dict, Callable, NewType
from kivy.uix.label import Label
from antlr.FileSyntaxErrorListener import \
    ERROR_INVALID_BORDER_THICKNESS, \
    ERROR_INVALID_BORDER_TYPE
from user_interface.Color import ColorType, BORDER_THICKNESS, BORDER_COLOR, BACKGROUND_COLOR, ColoredWidget
from user_interface.EmptyCell import EmptyCell


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


class BorderCell(BoxLayout):
    border_type: str
    l_aw: BoxLayout
    r_aw: BoxLayout
    lu_aw: ColoredWidget
    ru_aw: ColoredWidget
    ld_aw: ColoredWidget
    rd_aw: ColoredWidget

    def __init__(self,
                 luc: ColorType = BACKGROUND_COLOR,
                 ldc: ColorType = BACKGROUND_COLOR,
                 ruc: ColorType = BACKGROUND_COLOR,
                 rdc: ColorType = BACKGROUND_COLOR,
                 lr_size_hint: Tuple[float, float] = (1, 1),
                 ud_size_hint: Tuple[float, float] = (1, 1),
                 **kwargs):
        super(BorderCell, self).__init__(**kwargs)
        self.orientation = "horizontal"
        (self.l_aw, self.lu_aw, self.ld_aw) = self.__get_area(
            uc=luc, dc=ldc, width_sh=lr_size_hint[0], ud_sh=ud_size_hint)
        (self.r_aw, self.ru_aw, self.rd_aw) = self.__get_area(
            uc=ruc, dc=rdc, width_sh=lr_size_hint[1], ud_sh=ud_size_hint)
        self.add_widget(self.l_aw)
        self.add_widget(self.r_aw)

    @staticmethod
    def __get_area(
            uc: ColorType,
            dc: ColorType,
            width_sh: float,
            ud_sh: Tuple[float, float]
    ) -> Tuple[BoxLayout, ColoredWidget, ColoredWidget]:
        area_widget: BoxLayout = BoxLayout(
            orientation="vertical",
            size_hint=(width_sh, 1)
        )
        up = ColoredWidget(
            bg_col=uc,
            size_hint=(1, ud_sh[0])
        )
        down = ColoredWidget(
            bg_col=dc,
            size_hint = (1, ud_sh[1])
        )
        area_widget.add_widget(up)
        area_widget.add_widget(down)
        return area_widget, up, down


class UpBorderCell(BorderCell):
    def __init__(self, **kwargs):
        super(UpBorderCell, self).__init__(
            luc=BORDER_COLOR,
            ruc=BORDER_COLOR,
            ud_size_hint=(BORDER_THICKNESS, 1),
            **kwargs)


class DownBorderCell(BorderCell):
    def __init__(self, **kwargs):
        super(DownBorderCell, self).__init__(
            ldc=BORDER_COLOR,
            rdc=BORDER_COLOR,
            ud_size_hint=(1, BORDER_THICKNESS),
            **kwargs)


class LeftBorderCell(BorderCell):
    def __init__(self, **kwargs):
        super(LeftBorderCell, self).__init__(
            luc=BORDER_COLOR,
            ldc=BORDER_COLOR,
            lr_size_hint=(BORDER_THICKNESS, 1),
            **kwargs)


class LeftUpBorderCell(LeftBorderCell):
    def __init__(self, **kwargs):
        super(LeftUpBorderCell, self).__init__(
            ruc=BORDER_COLOR,
            ud_size_hint=(BORDER_THICKNESS, 1),
            **kwargs)


class LeftDownBorderCell(LeftBorderCell):
    def __init__(self, **kwargs):
        super(LeftDownBorderCell, self).__init__(
            rdc=BORDER_COLOR,
            ud_size_hint=(1, BORDER_THICKNESS),
            **kwargs)


class RightBorderCell(BorderCell):
    def __init__(self, **kwargs):
        super(RightBorderCell, self).__init__(
            ruc=BORDER_COLOR,
            rdc=BORDER_COLOR,
            lr_size_hint=(1, BORDER_THICKNESS),
            **kwargs)


class RightUpBorderCell(RightBorderCell):
    def __init__(self, **kwargs):
        super(RightUpBorderCell, self).__init__(
            luc=BORDER_COLOR,
            ud_size_hint=(BORDER_THICKNESS, 1),
            **kwargs)


class RightDownBorderCell(RightBorderCell):
    def __init__(self, **kwargs):
        super(RightDownBorderCell, self).__init__(
            ldc=BORDER_COLOR,
            ud_size_hint=(1, BORDER_THICKNESS),
            **kwargs)


class PanelHandler:
    background_color: ColorType
    __code_dict: Dict[str, Callable[[], Widget]]

    def __init__(self,
                 background_color: ColorType = BACKGROUND_COLOR
                 ):
        self.background_color = background_color
        self.__code_dict = {
            CODE.EMPTY: self.get_empty_cell,
            CODE.BORDER_LEFT: self.get_left_border_cell,
            CODE.BORDER_LEFT_UP: self.get_left_up_border_cell,
            CODE.BORDER_LEFT_DOWN: self.get_left_down_border_cell,
            CODE.BORDER_RIGHT: self.get_right_border_cell,
            CODE.BORDER_RIGHT_UP: self.get_right_up_border_cell,
            CODE.BORDER_RIGHT_DOWN: self.get_right_down_border_cell,
            CODE.BORDER_UP: self.get_up_border_cell,
            CODE.BORDER_DOWN: self.get_down_border_cell
        }

    def get_empty_cell(self) -> EmptyCell:
        return EmptyCell(
            bg_col=self.background_color
        )

    def get_left_border_cell(self) -> BorderCell:
        return LeftBorderCell()

    def get_left_up_border_cell(self) -> BorderCell:
        return LeftUpBorderCell()

    def get_left_down_border_cell(self) -> BorderCell:
        return LeftDownBorderCell()

    def get_right_border_cell(self) -> BorderCell:
        return RightBorderCell()

    def get_right_up_border_cell(self) -> BorderCell:
        return RightUpBorderCell()

    def get_right_down_border_cell(self) -> BorderCell:
        return RightDownBorderCell()

    def get_up_border_cell(self) -> BorderCell:
        return UpBorderCell()

    def get_down_border_cell(self) -> BorderCell:
        return DownBorderCell()

    def get_cell(self, code: str) -> Widget:
        return self.__code_dict[code]()
