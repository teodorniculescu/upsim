from kivy.uix.label import Label


class TextCell(Label):
    def __init__(self,
                 parameters=None,
                 **kwargs):
        text = ""
        if parameters is not None:
            if "name" in parameters:
                text=parameters["name"]

        super(TextCell, self).__init__(text=text, **kwargs)
