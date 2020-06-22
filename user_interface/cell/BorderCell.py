from kivy.uix.boxlayout import BoxLayout
from typing import Tuple, List
from user_interface.Color import \
    TextWidget, ColoredWidget, ColorType, TRANSPARENT, BORDER_COLOR
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


class BaseBorderRows(BoxLayout):
    class Row(BoxLayout):
        columns: List[ColoredWidget]

        def __init__(self,
                     column_colors: List[ColorType],
                     column_width_hint: List[float],
                     **kwargs):
            super(BaseBorderRows.Row, self).__init__(**kwargs)
            self.orientation = "horizontal"
            self.columns = []
            for column_index in range(3):
                size_hint = (column_width_hint[column_index], 1)
                bg_col = column_colors[column_index]
                # if the background is transparent
                widget = ColoredWidget(
                    bg_col=bg_col,
                    size_hint=size_hint
                )
                self.add_widget(widget)
                self.columns.append(widget)

        def set_background_color_on(self):
            for cell in self.columns:
                if cell.default_col[3] == 0:
                    cell.set_on_color()

        def set_background_color_off(self):
            for cell in self.columns:
                if cell.default_col[3] == 0:
                    cell.set_off_color()

        def set_background_color_high_impendace(self):
            for cell in self.columns:
                if cell.default_col[3] == 0:
                    cell.set_high_impedance_color()

    rows: List[Row]

    def __init__(self,
                 matrix_colors: List[List[ColorType]],
                 parameters: ParamElem = None,
                 **kwargs):
        super(BaseBorderRows, self).__init__(**kwargs)
        self.orientation = "vertical"
        rest_thickness: float = (1 - BORDER_THICKNESS) / 2
        size_hints: List[float] = [rest_thickness, BORDER_THICKNESS, rest_thickness]
        self.rows = []
        for row_index in range(3):
            widget = BaseBorderRows.Row(
                column_colors=matrix_colors[row_index],
                column_width_hint=size_hints,
                size_hint=(1, size_hints[row_index])
            )
            self.add_widget(widget)
            self.rows.append(widget)

        if parameters is not None:
            if "name" in parameters:
                pos_bias = parameters["name_pos_bias"] if "name_pos_bias" in parameters else (0, 0)
                # TODO use pos bias to move the name to a much suitable position
                self.rows[1].columns[1].add_text_widget(parameters["name"])

    def set_on_color(self):
        for row in self.rows:
            row.set_background_color_on()

    def set_off_color(self):
        for row in self.rows:
            row.set_background_color_off()

    def set_high_impedance_color(self):
        for row in self.rows:
            row.set_background_color_high_impendace()


class UpDownBorder(BaseBorderRows):
    def __init__(self, **kwargs):
        matrix_colors: List[List[ColorType]] = \
            [
                [BORDER_COLOR, BORDER_COLOR, BORDER_COLOR],
                [TRANSPARENT, TRANSPARENT, TRANSPARENT],
                [BORDER_COLOR, BORDER_COLOR, BORDER_COLOR]
            ]
        super(UpDownBorder, self).__init__(matrix_colors=matrix_colors, **kwargs)


class UpDownLeftBorder(BaseBorderRows):
    def __init__(self, **kwargs):
        matrix_colors: List[List[ColorType]] = \
            [
                [BORDER_COLOR, BORDER_COLOR, BORDER_COLOR],
                [BORDER_COLOR, TRANSPARENT, TRANSPARENT],
                [BORDER_COLOR, BORDER_COLOR, BORDER_COLOR]
            ]
        super(UpDownLeftBorder, self).__init__(matrix_colors=matrix_colors, **kwargs)


class UpDownRightBorder(BaseBorderRows):
    def __init__(self, **kwargs):
        matrix_colors: List[List[ColorType]] = \
            [
                [BORDER_COLOR, BORDER_COLOR, BORDER_COLOR],
                [TRANSPARENT, TRANSPARENT, BORDER_COLOR],
                [BORDER_COLOR, BORDER_COLOR, BORDER_COLOR]
            ]
        super(UpDownRightBorder, self).__init__(matrix_colors=matrix_colors, **kwargs)


class LeftRightBorder(BaseBorderRows):
    def __init__(self, **kwargs):
        matrix_colors: List[List[ColorType]] = \
            [
                [BORDER_COLOR, TRANSPARENT, BORDER_COLOR],
                [BORDER_COLOR, TRANSPARENT, BORDER_COLOR],
                [BORDER_COLOR, TRANSPARENT, BORDER_COLOR]
            ]
        super(LeftRightBorder, self).__init__(matrix_colors=matrix_colors, **kwargs)


class LeftRightDownBorder(BaseBorderRows):
    def __init__(self, **kwargs):
        matrix_colors: List[List[ColorType]] = \
            [
                [BORDER_COLOR, TRANSPARENT, BORDER_COLOR],
                [BORDER_COLOR, TRANSPARENT, BORDER_COLOR],
                [BORDER_COLOR, BORDER_COLOR, BORDER_COLOR]
            ]
        super(LeftRightDownBorder, self).__init__(matrix_colors=matrix_colors, **kwargs)


class LeftRightUpBorder(BaseBorderRows):
    def __init__(self, **kwargs):
        matrix_colors: List[List[ColorType]] = \
            [
                [BORDER_COLOR, BORDER_COLOR, BORDER_COLOR],
                [BORDER_COLOR, TRANSPARENT, BORDER_COLOR],
                [BORDER_COLOR, TRANSPARENT, BORDER_COLOR]
            ]
        super(LeftRightUpBorder, self).__init__(matrix_colors=matrix_colors, **kwargs)
