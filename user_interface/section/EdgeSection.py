from typing import Dict
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class EdgeSection(BoxLayout):
    first_elem_index: int
    last_elem_index: int
    all_widgets: Dict[int, Widget]

    def __init__(self,
                 num_elements:int=1,
                 first_elem_index:int=0,
                 **kwargs):
        super(EdgeSection, self).__init__(**kwargs)
        self.first_elem_index = first_elem_index
        self.last_elem_index = num_elements + first_elem_index - 1
        self.all_widgets = {}
        for index in range(self.first_elem_index, self.last_elem_index + 1):
            self.add_end_widget(index)

    def add_end_widget(self, index: int):
        new_widget = Button(text=str(index))
        self.add_widget(new_widget)
        self.all_widgets[index] = new_widget

    def insert_end_widget(self):
        self.last_elem_index += 1
        self.add_end_widget(self.last_elem_index)

    def insert_beginning_widget(self):
        self.first_elem_index -= 1
        new_widget = Button(text=str(self.first_elem_index))
        self.add_widget(new_widget, len(self.children))
        self.all_widgets[self.first_elem_index] = new_widget


    def get_num_elements(self) -> int:
        return self.last_elem_index - self.first_elem_index + 1

    def zoom_out(self):
        self.insert_end_widget()

    def zoom_in(self):
        if self.first_elem_index == self.last_elem_index:
            return
        self.remove_end_widget()

    def remove_end_widget(self):
        widget = self.all_widgets[self.last_elem_index]
        self.remove_widget(widget)
        del widget
        self.last_elem_index -= 1

    def remove_beginning_widget(self):
        widget = self.all_widgets[self.first_elem_index]
        self.remove_widget(widget)
        del widget
        self.first_elem_index += 1

    def set_size(self, size: int) -> None:
        while size < self.get_num_elements():
            self.zoom_in()
        while size > self.get_num_elements():
            self.zoom_out()

    def move_rd(self) -> None:
        self.remove_beginning_widget()
        self.insert_end_widget()

    def move_lu(self) -> None:
        if self.first_elem_index <= 0:
            return
        self.remove_end_widget()
        self.insert_beginning_widget()


class RowsSection(EdgeSection):
    def __init__(self, **kwargs):
        super(RowsSection, self).__init__(**kwargs)
        self.orientation = "vertical"


class ColumnsSection(EdgeSection):
    def __init__(self, **kwargs):
        super(ColumnsSection, self).__init__(**kwargs)
        self.orientation = "horizontal"
