from kivy.uix.boxlayout import BoxLayout
from user_interface.Color import ColorType, ColoredWidget, BACKGROUND_COLOR


class EmptyCell(BoxLayout):
    def __init__(self,
                 bg_col: ColorType = BACKGROUND_COLOR,
                 **kwargs):
        super(EmptyCell, self).__init__(**kwargs)
        self.add_widget(ColoredWidget(
            bg_col=bg_col
        ))


