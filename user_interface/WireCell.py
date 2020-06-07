from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from user_interface.Color import ColoredWidget, ColorType, BACKGROUND_COLOR, WIRE_COLOR
from user_interface.DataStructure import ParamElem
from typing import List


WIRE_THICKNESS: float = 0.05


class BaseWireCell(BoxLayout):
    class Row(BoxLayout):
        columns: List[ColoredWidget]

        def __init__(self,
                     column_colors: List[ColorType],
                     column_width_hint: List[float],
                     **kwargs):
            super(BaseWireCell.Row, self).__init__(**kwargs)
            self.orientation = "horizontal"
            self.columns = []
            for column_index in range(3):
                widget = ColoredWidget(
                    bg_col=column_colors[column_index],
                    size_hint=(column_width_hint[column_index], 1)
                )
                self.add_widget(widget)
                self.columns.append(widget)

    rows: List[Row]

    def __init__(self,
                 matrix_colors: List[List[ColorType]],
                 parameters: ParamElem = None,
                 **kwargs):
        super(BaseWireCell, self).__init__(**kwargs)
        self.orientation = "vertical"
        rest_thickness: float = (1 - WIRE_THICKNESS) / 2
        size_hints: List[float] = [rest_thickness, WIRE_THICKNESS, rest_thickness]
        self.rows = []
        for row_index in range(3):
            widget = BaseWireCell.Row(
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
                self.rows[0].columns[0].add_text_widget(parameters["name"])



class WireCell:
    class Right(BaseWireCell):
        def __init__(self, **kwargs):
            matrix_colors: List[List[ColorType]] = \
                [
                    [BACKGROUND_COLOR, BACKGROUND_COLOR, BACKGROUND_COLOR],
                    [BACKGROUND_COLOR, WIRE_COLOR, WIRE_COLOR],
                    [BACKGROUND_COLOR, BACKGROUND_COLOR, BACKGROUND_COLOR]
                ]
            super(WireCell.Right, self).__init__(matrix_colors=matrix_colors, **kwargs)

    class RightUp(BaseWireCell):
        def __init__(self, **kwargs):
            matrix_colors: List[List[ColorType]] = \
                [
                    [BACKGROUND_COLOR, WIRE_COLOR, BACKGROUND_COLOR],
                    [BACKGROUND_COLOR, WIRE_COLOR, WIRE_COLOR],
                    [BACKGROUND_COLOR, BACKGROUND_COLOR, BACKGROUND_COLOR]
                ]
            super(WireCell.RightUp, self).__init__(matrix_colors=matrix_colors, **kwargs)

    class RightDown(BaseWireCell):
        def __init__(self, **kwargs):
            matrix_colors: List[List[ColorType]] = \
                [
                    [BACKGROUND_COLOR, BACKGROUND_COLOR, BACKGROUND_COLOR],
                    [BACKGROUND_COLOR, WIRE_COLOR, WIRE_COLOR],
                    [BACKGROUND_COLOR, WIRE_COLOR, BACKGROUND_COLOR]
                ]
            super(WireCell.RightDown, self).__init__(matrix_colors=matrix_colors, **kwargs)

    class Left(BaseWireCell):
        def __init__(self, **kwargs):
            matrix_colors: List[List[ColorType]] = \
                [
                    [BACKGROUND_COLOR, BACKGROUND_COLOR, BACKGROUND_COLOR],
                    [WIRE_COLOR, WIRE_COLOR, BACKGROUND_COLOR],
                    [BACKGROUND_COLOR, BACKGROUND_COLOR, BACKGROUND_COLOR]
                ]
            super(WireCell.Left, self).__init__(matrix_colors=matrix_colors, **kwargs)

    class LeftUp(BaseWireCell):
        def __init__(self, **kwargs):
            matrix_colors: List[List[ColorType]] = \
                [
                    [BACKGROUND_COLOR, WIRE_COLOR, BACKGROUND_COLOR],
                    [WIRE_COLOR, WIRE_COLOR, BACKGROUND_COLOR],
                    [BACKGROUND_COLOR, BACKGROUND_COLOR, BACKGROUND_COLOR]
                ]
            super(WireCell.LeftUp, self).__init__(matrix_colors=matrix_colors, **kwargs)

    class LeftDown(BaseWireCell):
        def __init__(self, **kwargs):
            matrix_colors: List[List[ColorType]] = \
                [
                    [BACKGROUND_COLOR, BACKGROUND_COLOR, BACKGROUND_COLOR],
                    [WIRE_COLOR, WIRE_COLOR, BACKGROUND_COLOR],
                    [BACKGROUND_COLOR, WIRE_COLOR, BACKGROUND_COLOR]
                ]
            super(WireCell.LeftDown, self).__init__(matrix_colors=matrix_colors, **kwargs)

    class LeftRight(BaseWireCell):
        def __init__(self, **kwargs):
            matrix_colors: List[List[ColorType]] = \
                [
                    [BACKGROUND_COLOR, BACKGROUND_COLOR, BACKGROUND_COLOR],
                    [WIRE_COLOR, WIRE_COLOR, WIRE_COLOR],
                    [BACKGROUND_COLOR, BACKGROUND_COLOR, BACKGROUND_COLOR]
                ]
            super(WireCell.LeftRight, self).__init__(matrix_colors=matrix_colors, **kwargs)

    class UpDown(BaseWireCell):
        def __init__(self, **kwargs):
            matrix_colors: List[List[ColorType]] = \
                [
                    [BACKGROUND_COLOR, WIRE_COLOR, BACKGROUND_COLOR],
                    [BACKGROUND_COLOR, WIRE_COLOR, BACKGROUND_COLOR],
                    [BACKGROUND_COLOR, WIRE_COLOR, BACKGROUND_COLOR]
                ]
            super(WireCell.UpDown, self).__init__(matrix_colors=matrix_colors, **kwargs)
