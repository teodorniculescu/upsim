import kivy
kivy.require("1.11.1")
from Simulation import Simulation

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class ButtonBar(BoxLayout):
    pass

class EdgeSection(BoxLayout):
    num_elements: int

    def __init__(self,
                 num_elements=1,
                 **kwargs):
        super(EdgeSection, self).__init__(**kwargs)
        self.num_elements = num_elements
        for index in range(self.num_elements):
            self.add_widget(Button(text=str(index)))

class RowsSection(EdgeSection):
    def __init__(self, **kwargs):
        super(RowsSection, self).__init__(**kwargs)
        self.orientation = "vertical"

class ColumnsSection(EdgeSection):
    def __init__(self, **kwargs):
        super(ColumnsSection, self).__init__(**kwargs)
        self.orientation = "horizontal"

class SimulationSection(GridLayout):
    pass

class NoneSection(Widget):
    pass

class SimulationPanel(GridLayout):

    # when the screen resolution changes, increment the
    # number of rows and columns acording to their current
    # size divided by the size of the screen
    margin_size: tuple

    def __init__(self, **kwargs):
        super(SimulationPanel, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 2
        self.margin_size = (40, 20)
        none_section = NoneSection(
            size=self.margin_size)
        rows_section = RowsSection(
            size=self.margin_size,
            num_elements=8)
        cols_section = ColumnsSection(
            size=self.margin_size,
            num_elements=8)
        sim_section = SimulationSection()
        self.add_widget(none_section)
        self.add_widget(cols_section)
        self.add_widget(rows_section)
        self.add_widget(sim_section)


class SimulationUI(BoxLayout):
    def __init__(self, **kwargs):
        super(SimulationUI, self).__init__(**kwargs)
        self.orientation = "vertical"
    def update(self, dt):
        print("woah " + str(dt))

class UI(App):
    __simulation: Simulation
    def __init__(self, simulation: Simulation, **kwargs):
        super(UI, self).__init__(**kwargs)
        self.__simulation = simulation

    def build(self):
        simui = SimulationUI()
        return simui

