from typing import Tuple, NewType
from kivy.graphics import Color, Rectangle
import kivy.utils as kivy_utils
from kivy.uix.widget import Widget

ColorType = NewType("ColorType", Tuple[int, int, int, int])

BLACKCURRANT: ColorType = kivy_utils.get_color_from_hex("#342b38ff")
GULF_STREAM: ColorType = kivy_utils.get_color_from_hex("#80BDABff")
MADANG: ColorType = kivy_utils.get_color_from_hex("#bbf1c8ff")
MONA_LISA: ColorType = kivy_utils.get_color_from_hex("#FF9595ff")

BACKGROUND_COLOR: ColorType = BLACKCURRANT
BORDER_COLOR: ColorType = GULF_STREAM
WIRE_COLOR = MADANG


class ColoredWidget(Widget):
    background_rectangle: Rectangle
    bg_col: ColorType
    new_bg_col: bool

    def __init__(self,
                 bg_col: ColorType = BACKGROUND_COLOR,
                 **kwargs):
        super(ColoredWidget, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.bg_col = bg_col
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


