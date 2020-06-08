from kivy.uix.widget import Widget
from user_interface.DataStructure import ParamElem


class VoidCell(Widget):
    def __init__(
            self,
            parameters: ParamElem = None,
            **kwargs
    ):
        super(VoidCell, self).__init__(**kwargs)
