from kivy.uix.boxlayout import BoxLayout
from typing import Tuple, List
from user_interface.Color import \
    ColoredWidget, ColorType, TRANSPARENT, BORDER_COLOR
from user_interface.DataStructure import ParamElem


BORDER_THICKNESS: float = 0.5


class BorderCell(BoxLayout):
    l_aw: BoxLayout
    r_aw: BoxLayout
    lu_aw: ColoredWidget
    ru_aw: ColoredWidget
    ld_aw: ColoredWidget
    rd_aw: ColoredWidget

    def __init__(self,
                 luc: ColorType = TRANSPARENT,
                 ldc: ColorType = TRANSPARENT,
                 ruc: ColorType = TRANSPARENT,
                 rdc: ColorType = TRANSPARENT,
                 lr_size_hint: Tuple[float, float] = (1, 1),
                 ud_size_hint: Tuple[float, float] = (1, 1),
                 parameters: ParamElem = None,
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
            size_hint=(1, ud_sh[1])
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
