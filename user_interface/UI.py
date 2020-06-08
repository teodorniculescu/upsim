import kivy
kivy.require("1.11.1")

from user_interface.DataStructure import ParamElem
from user_interface.PanelHandler import PanelHandler, CODE
from Simulation import Simulation
from typing import Tuple, List, Dict
from blocks.BasicBlock import BasicBlock

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window


class Grid:
    __size: Tuple[int, int]
    # This matrix stores strings which describe the type of block
    # that is stored in that position.
    # Strings are used instead of EmptyCells because EmptyCells update
    # depending on their position in the simulation grid, which means
    # they cause problems when when they are not used.
    # Also, strings take up less memory than emtpy cells.
    __matrix: List[List[str]]
    __parameter: Dict[Tuple[int, int], ParamElem]
    __ph: PanelHandler

    def __init__(self, size: Tuple[int, int] = (1, 1)):
        self.__size = size
        self.__ph = PanelHandler()
        # creating a matrix of size[0] rows and size[1] columns
        self.__matrix = []
        self.__parameter = {}
        for row_index in range(self.__size[0]):
            row: List[str] = []
            for col_index in range(self.__size[1]):
                row.append("")
            self.__matrix.append(row)

    def add_blocks(self, blocks_dict: Dict[str, BasicBlock]) -> None:
        for block in blocks_dict.values():
            position = block.get_position()
            matrix = block.get_gui_grid()
            num_rows = len(matrix)
            num_cols = len(matrix[0])
            for row_index in range(num_rows):
                for col_index in range(num_cols):
                    (cell_type, cell_param) = matrix[row_index][col_index]
                    # real matrix position
                    rmp = (position[0] + row_index, position[1] + col_index)
                    self.__matrix[rmp[0]][rmp[1]] = cell_type
                    self.__parameter[rmp] = cell_param

    def get_cell_widget(self, index: Tuple[int, int]) -> Widget:
        str_code: str = self.__matrix[index[0]][index[1]]
        parameters: ParamElem = self.__parameter[index] if index in self.__parameter else {}
        return self.__ph.get_cell(str_code, parameters)


class SimulationSection(BoxLayout):
    __grid: Grid
    __simulation: Simulation
    __sim_size: Tuple[int, int]
    __ul_corner: Tuple[int, int]
    __cell_dict: Dict[Tuple[int, int], Widget]
    __row_dict: Dict[int, BoxLayout]

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



class ButtonBar(BoxLayout):
    pass


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


class RowsSection(EdgeSection):
    def __init__(self, **kwargs):
        super(RowsSection, self).__init__(**kwargs)
        self.orientation = "vertical"


class ColumnsSection(EdgeSection):
    def __init__(self, **kwargs):
        super(ColumnsSection, self).__init__(**kwargs)
        self.orientation = "horizontal"


class NoneSection(Widget):
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

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def zoom_in(self):
        self.rows_section.zoom_in()
        self.cols_section.zoom_in()
        self.sim_section.zoom_in()

    def zoom_out(self):
        self.rows_section.zoom_out()
        self.cols_section.zoom_out()
        self.sim_section.zoom_out()

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
