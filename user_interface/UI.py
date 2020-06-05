import kivy
kivy.require("1.11.1")
from Simulation import Simulation
from typing import Tuple, List

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
            self.add_widget(
                Button(text=str(index)))

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

class Grid:
    __size: Tuple[int, int]
    __matrix: List[List]

    def __init__(self, size: Tuple[int, int] = (1, 1)):
        self.__size = size
        # creating a matrix of size[0] lines and size[1] columns
        self.__matrix = [[None] * self.__size[1]] * self.__size[0]


class SimulationPanel(GridLayout):

    # when the screen resolution changes, increment the
    # number of rows and columns acording to their current
    # size divided by the size of the screen
    margin_size: tuple
    __simulation: Simulation
    __grid: Grid

    def __init__(self, simulation: Simulation, **kwargs):
        super(SimulationPanel, self).__init__(**kwargs)
        self.__simulation = simulation
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

        self.build_grid()
        self.update_panel()

    def build_grid(self):
        print("grid yo")

    def update_panel(self) -> None:
        print("panel yo")
        print(self.__simulation)

class SimulationUI(BoxLayout):
    __simulation: Simulation
    def __init__(self, simulation: Simulation, **kwargs):
        super(SimulationUI, self).__init__(**kwargs)
        self.__simulation = simulation
        self.orientation = "vertical"
        self.add_widget(ButtonBar())
        self.add_widget(SimulationPanel(simulation=self.__simulation))

class UI(App):
    __simulation: Simulation
    def __init__(self, simulation: Simulation, **kwargs):
        super(UI, self).__init__(**kwargs)
        self.__simulation = simulation

    def build(self):
        simui = SimulationUI(simulation=self.__simulation)
        return simui

