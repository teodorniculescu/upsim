from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from typing import Tuple, Dict, Callable, NewType
from kivy.uix.label import Label
import kivy.utils as kivy_utils
from antlr.FileSyntaxErrorListener import \
    ERROR_INVALID_BORDER_THICKNESS, \
    ERROR_INVALID_BORDER_TYPE


ColorType = NewType("ColorType", Tuple[int, int, int, int])

BLACKCURRANT: ColorType = kivy_utils.get_color_from_hex("#342b38ff")
GULF_STREAM: ColorType = kivy_utils.get_color_from_hex("#80BDABff")
MADANG: ColorType = kivy_utils.get_color_from_hex("#bbf1c8ff")
MONA_LISA: ColorType = kivy_utils.get_color_from_hex("#FF9595ff")

BACKGROUND_COLOR: ColorType = BLACKCURRANT
BORDER_COLOR: ColorType = GULF_STREAM
BORDER_THICKNESS: int = 0.05


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


class EmptyCell(BoxLayout):
    background_rectangle: Rectangle

    def __init__(self,
                 bg_col: ColorType = BACKGROUND_COLOR,
                 **kwargs):
        super(EmptyCell, self).__init__(**kwargs)
        self.add_widget(ColoredWidget())


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
                 lr_size_hint: Tuple[int, int] = (1, 1),
                 ud_size_hint: Tuple[int, int] = (1, 1),
                 **kwargs):
        super(BorderCell, self).__init__(**kwargs)
        self.orientation = "horizontal"
        (self.l_aw, self.lu_aw, self.ld_aw) = self.__get_area(uc=luc, dc=ldc)
        (self.r_aw, self.ru_aw, self.rd_aw) = self.__get_area(uc=ruc, dc=rdc)
        self.add_widget(self.l_aw)
        self.add_widget(self.r_aw)
        self.size_hint = lr_size_hint

    @staticmethod
    def __get_area(uc: ColorType, dc:ColorType) -> Tuple[BoxLayout, ColoredWidget, ColoredWidget]:
        area_widget: BoxLayout = BoxLayout(orientation="vertical")
        up = ColoredWidget(bg_col=uc)
        down = ColoredWidget(bg_col=dc)
        area_widget.add_widget(up)
        area_widget.add_widget(down)
        return area_widget, up, down


class LeftBorderCell(BorderCell):
    def __init__(self, **kwargs):
        super(LeftBorderCell, self).__init__(
            luc=BORDER_COLOR,
            ldc=BORDER_COLOR,
            lr_size_hint=(BORDER_THICKNESS, 1),
            **kwargs)


class PanelHandler:
    background_color: ColorType
    __code_dict: Dict[str, Callable[[], Widget]]

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

    def get_left_border_cell(self) -> BorderCell:
        return LeftBorderCell()

    def get_cell(self, code: str) -> Widget:
        return self.__code_dict[code]()
