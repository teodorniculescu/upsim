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
        widget = ColoredWidget()
        if parameters is not None:
            if "name" in parameters:
                widget.add_text_widget(parameters["name"])
        self.add_widget(widget )


