from kivy.uix.boxlayout import BoxLayout
from user_interface.Color import ColorType, ColoredWidget, BACKGROUND_COLOR


class EmptyCell(BoxLayout):
    def __init__(self, **kwargs):
        super(EmptyCell, self).__init__(**kwargs)
        self.add_widget(ColoredWidget())


