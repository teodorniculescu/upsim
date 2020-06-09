import kivy
kivy.require("1.11.1")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

from Simulation import Simulation
from user_interface.section.EdgeSection import ColumnsSection, RowsSection
from user_interface.section.SimulationSection import SimulationSection
from user_interface.section.NoneSection import NoneSection
from math import floor


class ButtonBar(BoxLayout):
    pass


class SimulationPanel(GridLayout):

    # when the screen resolution changes, increment the
    # number of rows and columns according to their current
    # size divided by the size of the screen
    margin_size: tuple
    __simulation: Simulation

    def __init__(self, simulation: Simulation, **kwargs):
        super(SimulationPanel, self).__init__(**kwargs)
        self.__simulation = simulation
        self.cols = 2
        self.rows = 2
        self.margin_size = (40, 20)
        sim_size = (8, 8)
        self.none_section = NoneSection(
            size=self.margin_size)
        self.rows_section = RowsSection(
            size=self.margin_size,
            num_elements=sim_size[0])
        self.cols_section = ColumnsSection(
            size=self.margin_size,
            num_elements=sim_size[1])
        self.sim_section = SimulationSection(
            simulation=self.__simulation,
            sim_size=sim_size)
        self.add_widget(self.none_section)
        self.add_widget(self.cols_section)
        self.add_widget(self.rows_section)
        self.add_widget(self.sim_section)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.cell_wh = 128
        self.bind(size=self.update_cell_count)

    def update_cell_count(self, *args):
        (w, h) = self.size
        num_cols = floor(w / self.cell_wh)
        num_rows = floor(h / self.cell_wh)
        print("Num rows " + str(num_rows) + " num cols " + str(num_cols))
        self.rows_section.set_size(num_rows)
        self.cols_section.set_size(num_cols)
        self.sim_section.set_rows(num_rows)
        self.sim_section.set_cols(num_cols)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    # How much does the zoom affect to cell width and height
    const_wh: int = 1.1

    def zoom_in(self):
        self.cell_wh *= self.const_wh
        self.update_cell_count()

    def zoom_out(self):
        if self.cell_wh > 20:
            self.cell_wh /= self.const_wh
            self.update_cell_count()

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == '=':
            self.zoom_out()
        elif keycode[1] == '-':
            self.zoom_in()
        return True


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
        sim_ui = SimulationUI(simulation=self.__simulation)
        return sim_ui
