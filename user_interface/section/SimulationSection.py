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
                 sim_size: Tuple[int, int] = (1, 1),
                 ul_corner: Tuple[int, int] = (0, 0),
                 **kwargs):
        super(SimulationSection, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.__simulation = simulation
        self.__sim_size = sim_size
        self.__ul_corner = ul_corner
        self.__cell_dict = {}
        self.__row_dict = {}
        self.__build_grid()
        self.__update_panel()
        # create the background rectangle
        self.bg_col = BACKGROUND_COLOR
        with self.canvas.before:
            Color(self.bg_col[0], self.bg_col[1], self.bg_col[2], self.bg_col[3])
            self.background_rectangle = Rectangle(size=self.size,
                                                  pos=self.pos)
        self.bind(pos=self.update_background_rectangle,
                  size=self.update_background_rectangle)

    def update_background_rectangle(self, *args):
        self.background_rectangle.pos = self.pos
        self.background_rectangle.size = self.size

    def __build_grid(self):
        self.__grid = Grid(size=(200, 400))
        self.__grid.add_blocks(self.__simulation.get_positionable_blocks())

    # Returns the cell widget corresponding to the given row and column index
    # If the function creates a new cell, it automatically adds it to the
    # cell dictionary
    # If the cell already exists, the function returns the already existing cell
    def __get_cell(self, row_index: int, column_index: int) -> Widget:
        index = (row_index, column_index)
        # check if the cell already exists
        if index in self.__cell_dict:
            return self.__cell_dict[index]
        # create a new cell widget
        cell_widget: Widget = self.__grid.get_cell_widget(
            index=(row_index, column_index)
        )
        # add cell to cell Dictionary
        self.__cell_dict[index] = cell_widget
        return cell_widget

    def __create_row(self, row_index: int) -> BoxLayout:
        print(str(row_index) + "best row index ever")
        # check if the row widget already exists
        if row_index in self.__row_dict:
            return self.__row_dict[row_index]
        # create the BoxLayout that serves as the row widget
        row_widget = BoxLayout(
            orientation="horizontal"
        )
        for column_counter in range(self.__sim_size[1]):
            # get column index from column counter
            column_index: int = column_counter + self.__ul_corner[1]
            cell_widget = self.__get_cell(row_index, column_index)
            # add the row widget to the Box Layout containing all Widgets from this row
            row_widget.add_widget(cell_widget)
        # add the widget to the Dictionary containing all rows
        self.__row_dict[row_index] = row_widget
        return row_widget

    def __update_panel(self) -> None:
        for row_counter in range(self.__sim_size[0]):
            # get the row index from the row counter
            row_index: int = row_counter + self.__ul_corner[0]
            # create row widget according to the current row counter
            # do take into consideration that the row counter is different from the row index
            # the row index is the row counter plus the current upper left position
            row_widget = self.__create_row(row_index)
            # add widget to BoxLayout
            self.add_widget(row_widget)

    def __add_end_column(self) -> None:
        # increment column number
        self.__sim_size = (self.__sim_size[0], self.__sim_size[1] + 1)
        # get the index of the column that does not yet exist
        col_index = self.__ul_corner[1] + self.__sim_size[1] - 1
        # iterate over all rows
        for row_counter in range(self.__sim_size[0]):
            # get row index
            row_index: int = row_counter + self.__ul_corner[0]
            # get cell widget
            cell_widget = self.__get_cell(row_index, col_index)
            print(str(row_index) + ":" + str(col_index))
            # add widget to the corresponding row widget
            self.__row_dict[row_index].add_widget(cell_widget)
            print("woah")

    def __add_end_row(self) -> None:
        # increment row number
        self.__sim_size = (self.__sim_size[0] + 1, self.__sim_size[1])
        # get the index of the row that has not been created yet
        row_index: int = self.__ul_corner[0] + self.__sim_size[0] - 1
        print("add end row " + str(row_index))
        self.add_widget(self.__create_row(row_index))

    def __remove_end_column(self) -> None:
        # get the index of the column that will be deleted
        col_index: int = self.__sim_size[1] +  self.__ul_corner[1] - 1
        # remove last column
        for row_counter in range(self.__sim_size[0]):
            # get row index
            row_index: int = row_counter + self.__ul_corner[0]
            # get index
            index = (row_index, col_index)
            # get widget of the last column and remove it from the corresponding BoxLayout
            widget = self.__cell_dict[index]
            self.__row_dict[row_index].remove_widget(widget)
            widget.parent = None
        # decrement column number
        self.__sim_size = (self.__sim_size[0], self.__sim_size[1] - 1)

    def __remove_end_row(self) -> None:
        # get row index
        row_index = self.__sim_size[0] + self.__ul_corner[0] - 1
        # remove last row
        widget = self.__row_dict[row_index]
        self.remove_widget(widget)
        widget.parent = None
        # decrement row number
        self.__sim_size = (self.__sim_size[0] - 1, self.__sim_size[1])

    def __add_beginning_column(self):
        self.__ul_corner = (self.__ul_corner[0], self.__ul_corner[1] - 1)
        for row_counter in range(self.__sim_size[0]):
            row_index = self.__ul_corner[0] + row_counter
            col_index = self.__ul_corner[1]
            cell_widget = self.__get_cell(row_index, col_index)
            row_widget = self.__row_dict[row_index]
            row_widget.add_widget(cell_widget, len(row_widget.children))

    def __remove_beginning_column(self) -> None:
        for row_index in range(self.__sim_size[0]):
            widget = self.__cell_dict.pop((row_index, self.__ul_corner[1]))
            self.__row_dict[row_index].remove_widget(widget)
            del widget
        self.__ul_corner = (self.__ul_corner[0], self.__ul_corner[1] + 1)

    def move_screen_left(self):
        if self.__ul_corner[1] > 0:
            self.__add_beginning_column()
            self.__remove_end_column()

    def move_screen_right(self):
        self.__add_end_column()
        self.__remove_beginning_column()

    def move_screen_up(self):
        if self.__ul_corner[1] <= 0:
            self.__ul_corner = (self.__ul_corner[0], self.__ul_corner[1] - 1)

    def move_screen_down(self):
        self.__ul_corner = (self.__ul_corner[0], self.__ul_corner[1] + 1)

    def zoom_in(self):
        self.__remove_end_column()
        self.__remove_end_row()

    def zoom_out(self):
        self.__add_end_column()
        self.__add_end_row()

    def set_rows(self, num_rows: int):
        while num_rows < self.__sim_size[0]:
            self.__remove_end_row()
        while num_rows > self.__sim_size[0]:
            self.__add_end_row()

    def set_cols(self, num_cols: int):
        while num_cols < self.__sim_size[1]:
            self.__remove_end_column()
        while num_cols > self.__sim_size[1]:
            self.__add_end_column()
