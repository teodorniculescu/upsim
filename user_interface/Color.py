from typing import Tuple, NewType
from kivy.graphics import Color, Rectangle
import kivy.utils as kivy_utils
from kivy.uix.widget import Widget
from kivy.uix.label import Label

ColorType = NewType("ColorType", Tuple[int, int, int, int])

BLACKCURRANT: ColorType = kivy_utils.get_color_from_hex("#342b38ff")
GULF_STREAM: ColorType = kivy_utils.get_color_from_hex("#80BDABff")
MADANG: ColorType = kivy_utils.get_color_from_hex("#bbf1c8ff")
MONA_LISA: ColorType = kivy_utils.get_color_from_hex("#FF9595ff")
TRANSPARENT: ColorType = ColorType((0, 0, 0, 0))
RED: ColorType = ColorType((1, 0, 0, 1))
GREEN: ColorType = ColorType((0, 1, 0, 1))

BACKGROUND_COLOR: ColorType = BLACKCURRANT
BORDER_COLOR: ColorType = GULF_STREAM
WIRE_COLOR = MADANG
WIRE_ON_COLOR: ColorType = GREEN
WIRE_OFF_COLOR: ColorType = RED


class TextWidget(Widget):
    text_widget: Label

    def __init__(self,
                 **kwargs):
        super(TextWidget, self).__init__(**kwargs)

    def update_text_widget(self, *args):
        self.text_widget.pos = self.pos
        self.text_widget.size = self.size

    def add_text_widget(self, text: str) -> None:
        self.text_widget = Label(text=text)
        self.add_widget(self.text_widget)
        self.bind(pos=self.update_text_widget,
                  size=self.update_text_widget)


class ColoredWidget(TextWidget):
    background_rectangle: Rectangle
    bg_col: ColorType
    default_col: ColorType
    new_bg_col: bool

    def __init__(self,
                 bg_col: ColorType = BACKGROUND_COLOR,
                 **kwargs):
        super(ColoredWidget, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.bg_col = bg_col
        self.default_col = bg_col
        self.new_bg_col = False
        with self.canvas.before:
            Color(self.bg_col[0], self.bg_col[1], self.bg_col[2], self.bg_col[3])
            self.background_rectangle = Rectangle(size=self.size,
                                                  pos=self.pos)
        self.bind(pos=self.update_background_rectangle,
                  size=self.update_background_rectangle)

    def update_background_rectangle(self, *args):
        self.background_rectangle.pos = self.pos
        self.background_rectangle.size = self.size

    def __set_color(self, color: ColorType) -> None:
        if self.default_col != BACKGROUND_COLOR:
            self.canvas.before.clear()
            self.bg_col = color
            self.canvas.before.add(Color(self.bg_col[0], self.bg_col[1], self.bg_col[2], self.bg_col[3]))
            self.background_rectangle = Rectangle(size=self.size, pos=self.pos)
            self.canvas.before.add(self.background_rectangle)

    def set_on_color(self) -> None:
        self.__set_color(WIRE_ON_COLOR)

    def set_off_color(self) -> None:
        self.__set_color(WIRE_OFF_COLOR)

    def set_high_impedance_color(self) -> None:
        self.__set_color(self.default_col)

