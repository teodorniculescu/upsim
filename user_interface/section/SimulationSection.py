from user_interface.Grid import Grid
from Simulation import Simulation
from typing import Tuple, List, Dict
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from user_interface.Color import BACKGROUND_COLOR, ColorType, TRANSPARENT


class SimulationSection(BoxLayout):
    __grid: Grid
    __simulation: Simulation
    __sim_size: Tuple[int, int]
    __ul_corner: Tuple[int, int]
    __cell_dict: Dict[Tuple[int, int], Widget]
    __row_dict: Dict[int, BoxLayout]
    background_rectangle: Rectangle
    bg_col: ColorType

    def __init__(self,
                 simulation: Simulation,
                 sim_size: Tuple[int, int],
                 ul_corner: Tuple[int, int] = (0, 0),
                 **kwargs):
        super(SimulationSection, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.__simulation = simulation
        self.__sim_size = sim_size
        self.__ul_corner = ul_corner
        self.__cell_dict = {}
        self.__row_dict = {}
        self.build_grid()
        self.update_panel()
        # create the background rectangle
        self.bg_col = TRANSPARENT
        with self.canvas.before:
            Color(self.bg_col[0], self.bg_col[1], self.bg_col[2], self.bg_col[3])
            self.background_rectangle = Rectangle(size=self.size,
                                                  pos=self.pos)
        self.bind(pos=self.update_background_rectangle,
                  size=self.update_background_rectangle)

    def update_background_rectangle(self, *args):
        self.background_rectangle.pos = self.pos
        self.background_rectangle.size = self.size

    def build_grid(self):
        self.__grid = Grid(size=(100, 100))
        self.__grid.add_blocks(self.__simulation.get_positionable_blocks())

    def __create_row(self, row_index) -> BoxLayout:
        row_widget = BoxLayout(
            orientation="horizontal"
        )
        self.__row_dict[row_index] = row_widget
        for column_index in range(self.__sim_size[1]):
            cell_widget = self.__create_cell(row_index, column_index)
            row_widget.add_widget(cell_widget)
        return row_widget

    def __create_cell(self, row_index, column_index) -> Widget:
        cell_widget: Widget = self.__grid.get_cell_widget(
            index=(row_index, column_index)
        )
        self.__cell_dict[(row_index, column_index)] = cell_widget
        return cell_widget

    def update_panel(self) -> None:
        self.clear_widgets()
        for row_index in range(self.__sim_size[0]):
            row_widget = self.__create_row(row_index)
            self.add_widget(row_widget)

    def zoom_in(self):
        # remove last column
        for row_index in range(self.__sim_size[0]):
            widget = self.__cell_dict.pop((row_index, self.__sim_size[1] - 1))
            self.__row_dict[row_index].remove_widget(widget)
            del widget
        # remove last line
        widget = self.__row_dict.pop(self.__sim_size[0] - 1)
        self.remove_widget(widget)
        # decrement size
        self.__sim_size = (self.__sim_size[0] - 1, self.__sim_size[1] - 1)

    def zoom_out(self):
        # add last line
        self.add_widget(self.__create_row(self.__sim_size[0]))
        # add last column
        for row_index in range(self.__sim_size[0] + 1):
            cell_widget = self.__create_cell(row_index, self.__sim_size[1])
            self.__row_dict[row_index].add_widget(cell_widget)
        # increment size
        self.__sim_size = (self.__sim_size[0] + 1, self.__sim_size[1] + 1)
