from kivy.uix.boxlayout import BoxLayout
from typing import List
from user_interface.Color import ColorType, ColoredWidget, BACKGROUND_COLOR
from user_interface.DataStructure import ParamElem


class EmptyCell(BoxLayout):
    def __init__(
            self,
            parameters: ParamElem = None,
            **kwargs
    ):
        super(EmptyCell, self).__init__(**kwargs)
        self.add_widget(ColoredWidget())


