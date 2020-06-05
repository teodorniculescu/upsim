from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from typing import Tuple, Dict, Callable, NewType
from kivy.uix.label import Label
import kivy.utils as kivy_utils
from antlr.FileSyntaxErrorListener import ERROR_INVALID_BORDER_THICKNESS


ColorType = NewType("ColorType", Tuple[int, int, int, int])

BLACKCURRANT: ColorType = kivy_utils.get_color_from_hex("#342b38ff")
GULF_STREAM: ColorType = kivy_utils.get_color_from_hex("#80BDABff")
MADANG: ColorType = kivy_utils.get_color_from_hex("#bbf1c8ff")
MONA_LISA: ColorType = kivy_utils.get_color_from_hex("#FF9595ff")

BACKGROUND_COLOR: ColorType = BLACKCURRANT
BORDER_COLOR: ColorType = GULF_STREAM



class EmptyCell(BoxLayout):
    background_rectangle: Rectangle

    def __init__(self,
                 bg_col: ColorType = BACKGROUND_COLOR,
                 **kwargs):
        super(EmptyCell, self).__init__(**kwargs)
        with self.canvas.before:
            Color(bg_col[0], bg_col[1], bg_col[2], bg_col[3])
            self.background_rectangle = Rectangle(size=self.size,
                                                  pos=self.pos)
        self.bind(pos=self.update_background_rectangle,
                  size=self.update_background_rectangle)

    def update_background_rectangle(self, *args):
        self.background_rectangle.pos = self.pos
        self.background_rectangle.size = self.size


class BorderCell(EmptyCell):
    border_thickness: int

    def __init__(self,
                 border_thickness: int = 0.05,
                 **kwargs):
        super(BorderCell, self).__init__(**kwargs)
        if not (border_thickness > 0 and border_thickness <= 1):
            raise Exception(ERROR_INVALID_BORDER_THICKNESS % border_thickness)
        self.border_thickness = border_thickness


class LeftBorderCell(BorderCell):
    def __init__(self, **kwargs):
        super(LeftBorderCell, self).__init__(**kwargs)
        self.left_border_widget = EmptyCell(
            bg_col=BORDER_COLOR,
            size_hint=(self.border_thickness, 1),
        )
        self.right_area_widget = EmptyCell()
        self.add_widget(self.left_border_widget)
        self.add_widget(self.right_area_widget)


class PanelHandler:
    background_color: ColorType
    __code_dict: Dict[str, Callable[[], EmptyCell]]

    def __init__(self,
                 background_color: ColorType = BACKGROUND_COLOR
                 ):
        self.background_color = background_color
        self.__code_dict \
            = {
            "": self.get_empty_cell,
            "b_l": self.get_left_border_cell
        }

    def get_empty_cell(self) -> EmptyCell:
        return EmptyCell(
            bg_col=self.background_color
        )

    def get_left_border_cell(self) -> LeftBorderCell:
        return LeftBorderCell(
            bg_col=self.background_color
        )

    def get_cell(self, code: str) -> EmptyCell:
        return self.__code_dict[code]()
