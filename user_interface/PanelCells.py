from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from typing import Tuple, Dict, Callable, NewType
from kivy.uix.label import Label


ColorType = NewType("ColorType", Tuple[int, int, int, int])


class EmptyCell(Widget):
    background_rectangle: Rectangle

    def __init__(self,
                 bg_col: ColorType = (0, 0, 0, 0),
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

    def add_text(self, text:str) -> None:
        self.clear_widgets()
        self.add_widget(Label(text=text))


class BorderCell(EmptyCell):
    border_thickness: int
    def __init__(self,
                 border_thickness: int = 5,
                 **kwargs):
        super(BorderCell, self).__init__(**kwargs)
        self.border_thickness = border_thickness


class PanelHandler:
    background_color: ColorType
    __code_dict: Dict[str, Callable[[], EmptyCell]]

    def __init__(self,
                 background_color: ColorType = (0, 0, 0, 0)):
        self.background_color = background_color
        self.__code_dict = {
            "": self.get_empty_cell
        }

    def get_empty_cell(self) -> EmptyCell:
        return EmptyCell(
            bg_col=self.background_color)

    def get_cell(self, code: str) -> EmptyCell:
        return self.__code_dict[code]()
