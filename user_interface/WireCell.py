from kivy.uix.boxlayout import BoxLayout
from user_interface.Color import ColoredWidget, ColorType, BACKGROUND_COLOR, MADANG
from typing import List


WIRE_THICKNESS = 0.05
WIRE_COLOR = MADANG


class WireCell(BoxLayout):
    class Row(BoxLayout):
        def __init__(self,
                     column_colors: List[ColorType],
                     column_width_hint: List[float],
                     **kwargs):
            super(WireCell.Row, self).__init__(**kwargs)
            self.orientation = "horizontal"
            for column_index in range(3):
                widget = ColoredWidget(
                    bg_col=column_colors[column_index],
                    size_hint=(column_width_hint[column_index], 1)
                )
                self.add_widget(widget)

    def __init__(self,
                 matrix_colors: List[List[ColorType]],
                 **kwargs):
        super(WireCell, self).__init__(**kwargs)
        self.orientation = "vertical"
        rest_thickness: float = (1 - WIRE_THICKNESS) / 2
        size_hints: List[float] = [rest_thickness, WIRE_THICKNESS, rest_thickness]
        for row_index in range(3):
            widget = WireCell.Row(
                column_colors=matrix_colors[row_index],
                column_width_hint=size_hints,
                size_hint=(1, size_hints[row_index])
            )
            self.add_widget(widget)


class RightWireCell(WireCell):
    def __init__(self, **kwargs):
        matrix_colors: List[List[ColorType]] = \
            [
                [BACKGROUND_COLOR, BACKGROUND_COLOR, BACKGROUND_COLOR],
                [WIRE_COLOR, WIRE_COLOR, BACKGROUND_COLOR],
                [BACKGROUND_COLOR, BACKGROUND_COLOR, BACKGROUND_COLOR]
            ]
        super(RightWireCell, self).__init__(matrix_colors=matrix_colors, **kwargs)

