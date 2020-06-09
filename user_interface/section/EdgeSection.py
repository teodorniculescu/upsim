from typing import List
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class EdgeSection(BoxLayout):
    num_elements: int
    all_widgets: List[Widget]

    def __init__(self,
                 num_elements=1,
                 **kwargs):
        super(EdgeSection, self).__init__(**kwargs)
        self.num_elements = num_elements
        self.all_widgets = []
        for index in range(self.num_elements):
            self.add_indicator(index)

    def add_indicator(self, index):
        new_widget = Button(text=str(index))
        self.add_widget(new_widget)
        self.all_widgets.append(new_widget)

    def zoom_out(self):
        self.add_indicator(self.num_elements)
        self.num_elements += 1

    def zoom_in(self):
        if self.num_elements <= 1:
            return
        removed_widget = self.all_widgets.pop()
        self.remove_widget(removed_widget)
        self.num_elements -= 1

    def set_size(self, size: int) -> None:
        while size < self.num_elements:
            self.zoom_in()
        while size > self.num_elements:
            self.zoom_out()


class RowsSection(EdgeSection):
    def __init__(self, **kwargs):
        super(RowsSection, self).__init__(**kwargs)
        self.orientation = "vertical"


class ColumnsSection(EdgeSection):
    def __init__(self, **kwargs):
        super(ColumnsSection, self).__init__(**kwargs)
        self.orientation = "horizontal"
