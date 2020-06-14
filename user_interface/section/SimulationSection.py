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
                 sim_size: Tuple[int, int] = (5, 3),
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
            raise Exception(str(index) + " already exists in __cell_dict")
        # create a new cell widget
        cell_widget: Widget = self.__grid.get_cell_widget(
            index=index
        )
        # add cell to cell Dictionary
        self.__cell_dict[index] = cell_widget
        return cell_widget

    def __create_row(self, row_index: int) -> BoxLayout:
        # check if the row widget already exists
        if row_index in self.__row_dict:
            raise Exception(str(row_index) + " already exists in __row_dict")
        # create the BoxLayout that serves as the row widget
        row_widget = BoxLayout(
            orientation="horizontal"
        )
        for column_counter in range(self.__num_cols()):
            # get column index from column counter
            column_index: int = column_counter + self.__ul_corner[1]
            cell_widget = self.__get_cell(row_index, column_index)
            # add the row widget to the Box Layout containing all Widgets from this row
            row_widget.add_widget(cell_widget)
        # add the widget to the Dictionary containing all rows
        self.__row_dict[row_index] = row_widget
        return row_widget

    def __update_panel(self) -> None:
        for row_counter in range(self.__num_rows()):
            # get the row index from the row counter
            row_index: int = row_counter + self.__ul_corner[0]
            # create row widget according to the current row counter
            # do take into consideration that the row counter is different from the row index
            # the row index is the row counter plus the current upper left position
            row_widget = self.__create_row(row_index)
            # add widget to BoxLayout
            self.add_widget(row_widget)

    def __end_column_index(self) -> int:
        return self.__sim_size[1] - 1

    def __end_row_index(self) -> int:
        return self.__sim_size[0] - 1

    def __beginning_row_index(self) -> int:
        return self.__ul_corner[0]

    def __beginning_column_index(self) -> int:
        return self.__ul_corner[1]

    def __inc_corner_col(self) -> None:
        self.__ul_corner = (self.__ul_corner[0], self.__ul_corner[1] + 1)

    def __dec_corner_col(self) -> None:
        self.__ul_corner = (self.__ul_corner[0], self.__ul_corner[1] - 1)

    def __inc_corner_row(self) -> None:
        self.__ul_corner = (self.__ul_corner[0] + 1, self.__ul_corner[1])

    def __dec_corner_row(self) -> None:
        self.__ul_corner = (self.__ul_corner[0] - 1, self.__ul_corner[1])

    def __inc_size_col(self) -> None:
        self.__sim_size = (self.__sim_size[0], self.__sim_size[1] + 1)

    def __dec_size_col(self) -> None:
        self.__sim_size = (self.__sim_size[0], self.__sim_size[1] - 1)

    def __inc_size_row(self) -> None:
        self.__sim_size = (self.__sim_size[0] + 1, self.__sim_size[1])

    def __dec_size_row(self) -> None:
        self.__sim_size = (self.__sim_size[0] - 1, self.__sim_size[1])

    def __num_rows(self) -> int:
        return self.__sim_size[0]

    def __num_cols(self) -> int:
        return self.__sim_size[1]

    def __pop_cell(self, index: Tuple[int, int]) -> None:
        self.__cell_dict.pop(index)

    def __pop_row(self, row_index: int) -> None:
        # pop all other cells from that row
        for col_counter in range(self.__num_cols()):
            col_index: int = col_counter + self.__ul_corner[1]
            index = (row_index, col_index)
            self.__pop_cell(index)
        # pop the specific row
        self.__row_dict.pop(row_index)

    def __add_end_column(self) -> None:
        # get the index of the column that does not yet exist
        col_index = self.__end_column_index() + 1
        # iterate over all rows
        for row_counter in range(self.__num_rows()):
            # get row index
            row_index: int = row_counter + self.__ul_corner[0]
            # get cell widget
            cell_widget = self.__get_cell(row_index, col_index)
            # add cell widget to the corresponding row widget
            self.__row_dict[row_index].add_widget(cell_widget)
        # add a new column to the screen width
        self.__inc_size_col()

    def __add_end_row(self) -> None:
        # get the index of the row that has not been created yet
        row_index: int = self.__end_row_index() + 1
        self.add_widget(self.__create_row(row_index))
        # increment row number
        self.__inc_size_row()

    def __remove_beginning_row(self) -> None:
        row_index: int = self.__beginning_row_index()
        self.remove_widget(self.__row_dict[row_index])
        self.__pop_row(row_index)
        self.__inc_corner_row()

    def __remove_end_column(self) -> None:
        # get the index of the column that will be deleted
        col_index: int = self.__end_column_index()
        # remove last column
        for row_counter in range(self.__num_rows()):
            # get row index
            row_index: int = row_counter + self.__ul_corner[0]
            # get index
            index = (row_index, col_index)
            # get widget of the last column
            widget = self.__cell_dict[index]
            # remove it from the corresponding BoxLayout
            self.__row_dict[row_index].remove_widget(widget)
            # pop the widget from the dictionary
            self.__pop_cell(index)
        # decrement column number
        self.__dec_size_col()

    def __remove_end_row(self) -> None:
        # get row index
        row_index = self.__end_row_index()
        # remove last row
        widget = self.__row_dict[row_index]
        # remove it the this self BoxLayout
        self.remove_widget(widget)
        # pop the widget from the dictionary
        self.__pop_row(row_index)
        # decrement row number
        self.__dec_size_row()

    def __add_beginning_column(self):
        # now the column number points to the column that does not exist yet
        col_index = self.__beginning_column_index() - 1
        # iterate over the number of rows
        for row_counter in range(self.__num_rows()):
            # generate row index from the row counter and the upper left row
            row_index = self.__ul_corner[0] + row_counter
            # generate the new cell widget
            cell_widget = self.__get_cell(row_index, col_index)
            # get the existing row widget
            row_widget = self.__row_dict[row_index]
            # add the cell to the corresponding row
            row_widget.add_widget(cell_widget, len(row_widget.children))
        # decrement the column number for the upper left corner of the screen
        self.__dec_corner_col()

    def __remove_beginning_column(self) -> None:
        col_index = self.__beginning_column_index()
        for row_counter in range(self.__num_rows()):
            row_index = self.__ul_corner[0] + row_counter
            index = (row_index, col_index)
            # get the cell widget
            widget = self.__cell_dict[index]
            # remove cell from row widget
            self.__row_dict[row_index].remove_widget(widget)
            # remove cell from the dictionary
            self.__pop_cell(index)
        # increment column upper left corner
        self.__inc_corner_col()

    def __add_beginning_row(self) -> None:
        row_index = self.__ul_corner[0] - 1
        self.add_widget(self.__create_row(row_index), len(self.children))
        self.__dec_corner_row()

    def move_screen_left(self):
        if self.__ul_corner[1] > 0:
            self.__add_beginning_column()
            self.__remove_end_column()

    def move_screen_right(self):
        self.__add_end_column()
        self.__remove_beginning_column()

    def move_screen_up(self):
        if self.__ul_corner[0] > 0:
            self.__add_beginning_row()
            self.__remove_end_row()

    def move_screen_down(self):
        self.__add_end_row()
        self.__remove_beginning_row()

    def zoom_in(self):
        self.__remove_end_column()
        self.__remove_end_row()

    def zoom_out(self):
        self.__add_end_column()
        self.__add_end_row()

    def set_rows(self, num_rows: int):
        pass
        """
        while num_rows < self.__sim_size[0]:
            self.__remove_end_row()
        while num_rows > self.__sim_size[0]:
            self.__add_end_row()
        """

    def set_cols(self, num_cols: int):
        pass
        """
        while num_cols < self.__sim_size[1]:
            self.__remove_end_column()
        while num_cols > self.__sim_size[1]:
            self.__add_end_column()
        """
