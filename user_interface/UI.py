import kivy
kivy.require("1.11.1")

from user_interface.PanelHandler import PanelHandler, CODE
from Simulation import Simulation
from typing import Tuple, List, Dict
from blocks.BasicBlock import BasicBlock

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class Grid:
    __size: Tuple[int, int]
    # This matrix stores strings which describe the type of block
    # that is stored in that position.
    # Strings are used instead of EmptyCells because EmptyCells update
    # depending on their position in the simulation grid, which means
    # they cause problems when when they are not used.
    # Also, strings take up less memory than emtpy cells.
    __matrix: List[List[str]]
    __ph: PanelHandler

    def __init__(self, size: Tuple[int, int] = (1, 1)):
        self.__size = size
        self.__ph = PanelHandler()
        # creating a matrix of size[0] rows and size[1] columns
        self.__matrix = []
        for row_index in range(self.__size[0]):
            row: List[str] = []
            for col_index in range(self.__size[1]):
                row.append("")
            self.__matrix.append(row)

    def add_blocks(self, blocks: Dict[str, BasicBlock]) -> None:
        print(blocks)
        self.__matrix[0][1] = CODE.BORDER_LEFT_UP
        self.__matrix[0][2] = CODE.BORDER_UP
        self.__matrix[0][3] = CODE.BORDER_RIGHT_UP

        self.__matrix[2][1] = CODE.BORDER_LEFT_DOWN
        self.__matrix[2][2] = CODE.BORDER_DOWN
        self.__matrix[2][3] = CODE.BORDER_RIGHT_DOWN

        self.__matrix[1][1] = CODE.BORDER_LEFT
        self.__matrix[1][3] = CODE.BORDER_RIGHT

        self.__matrix[1][0] = CODE.WIRE_RIGHT

    def get_cell_widget(self, index: Tuple[int, int]) -> Widget:
        str_code: str = self.__matrix[index[0]][index[1]]
        return self.__ph.get_cell(str_code)


class SimulationSection(BoxLayout):
    __grid: Grid
    __simulation: Simulation
    __sim_size: Tuple[int, int]
    __ul_corner: Tuple[int, int]

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
        self.build_grid()
        self.update_panel()

    def build_grid(self):
        self.__grid = Grid(size=(100, 100))
        self.__grid.add_blocks(self.__simulation.get_positionable_blocks())

    def update_panel(self) -> None:
        self.clear_widgets()
        for row_index in range(self.__sim_size[0]):
            row_widget = BoxLayout(
                orientation="horizontal"
            )
            for column_index in range(self.__sim_size[1]):
                cell_widget: Widget = self.__grid.get_cell_widget(
                    index=(row_index, column_index)
                )
                row_widget.add_widget(cell_widget)
            self.add_widget(row_widget)


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
        none_section = NoneSection(
            size=self.margin_size)
        rows_section = RowsSection(
            size=self.margin_size,
            num_elements=sim_size[0])
        cols_section = ColumnsSection(
            size=self.margin_size,
            num_elements=sim_size[1])
        sim_section = SimulationSection(
            simulation=self.__simulation,
            sim_size=sim_size)
        self.add_widget(none_section)
        self.add_widget(cols_section)
        self.add_widget(rows_section)
        self.add_widget(sim_section)


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
