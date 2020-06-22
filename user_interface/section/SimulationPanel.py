from user_interface.section.EdgeSection import ColumnsSection, RowsSection
from user_interface.section.SimulationSection import SimulationSection
from user_interface.section.NoneSection import NoneSection
from user_interface.cell.BorderCell import BaseBorderRows
from user_interface.cell.WireCell import *
from user_interface.Grid import Grid
from math import floor
from simulation.Simulation import Simulation
from kivy.uix.gridlayout import GridLayout
from typing import List, Tuple, Dict


class SimulationPanel(GridLayout):

    # when the screen resolution changes, increment the
    # number of rows and columns according to their current
    # size divided by the size of the screen
    margin_size: tuple
    __simulation: Simulation
    __animate: bool
    __animation_frames: List[Tuple[str]]
    __frame_description: List[str]
    __animation_frame_num: int
    __grid: Grid

    def __init__(self,
                 simulation: Simulation,
                 animate: bool,
                 **kwargs):
        super(SimulationPanel, self).__init__(**kwargs)
        self.__simulation = simulation
        self.__animate = animate
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
        self.__grid = self.sim_section.get_grid()
        self.add_widget(self.none_section)
        self.add_widget(self.cols_section)
        self.add_widget(self.rows_section)
        self.add_widget(self.sim_section)
        self.cell_wh = 40
        self.bind(size=self.update_cell_count)
        if self.__animate:
            (self.__frame_description, self.__animation_frames) = self.__simulation.get_animation_frames()
            self.__animation_frame_num = 0

    def get_frame_counter(self) -> Tuple[int, int]:
        return self.__animation_frame_num + 1, len(self.__animation_frames)

    def update_cell_count(self, *args):
        (w, h) = self.size
        num_cols = floor(w / self.cell_wh)
        num_rows = floor(h / self.cell_wh)
        self.rows_section.set_size(num_rows)
        self.cols_section.set_size(num_cols)
        self.sim_section.set_rows(num_rows)
        self.sim_section.set_cols(num_cols)
        self.__animate_frame()

    # How much does the zoom affect to cell width and height
    const_wh: int = 1.1

    def zoom_in(self):
        self.cell_wh *= self.const_wh
        self.update_cell_count()

    def zoom_out(self):
        if self.cell_wh > 20:
            self.cell_wh /= self.const_wh
            self.update_cell_count()

    def move_left(self):
        self.sim_section.move_screen_left()
        self.cols_section.move_lu()
        self.__animate_frame()

    def move_right(self):
        self.sim_section.move_screen_right()
        self.cols_section.move_rd()
        self.__animate_frame()

    def move_up(self):
        self.sim_section.move_screen_up()
        self.rows_section.move_lu()
        self.__animate_frame()

    def move_down(self):
        self.sim_section.move_screen_down()
        self.rows_section.move_rd()
        self.__animate_frame()

    def get_current_animation_frame(self) -> Tuple[str]:
        return self.__animation_frames[self.__animation_frame_num]

    def __animate_frame(self) -> None:
        if not self.__animate:
            return
        wire_widget_dict: Dict[str, List[Tuple[int, int]]] = self.__grid.get_wire_widget_dict()
        bus_widget_dict: Dict[str, List[Tuple[int, int]]] = self.__grid.get_bus_widget_dict()
        if self.__animation_frames == []:
            return
        for node_name, node_value in zip(self.__frame_description, self.get_current_animation_frame()):
            [block_name, pin_name] = node_name.split('.')
            if block_name in bus_widget_dict:
                for widget_index in bus_widget_dict[block_name]:
                    if not self.sim_section.index_within_bounds(widget_index):
                        continue
                    widget:BaseBorderRows = self.sim_section.get_cell_from_dict(widget_index)
                    if node_value == "1":
                        widget.set_on_color()
                    elif node_value == "0":
                        widget.set_off_color()
                    elif node_value == "N":
                        widget.set_high_impedance_color()
                    else:
                        raise Exception("invalid node value")

            if node_name in wire_widget_dict:
                for widget_index in wire_widget_dict[node_name]:
                    if not self.sim_section.index_within_bounds(widget_index):
                        continue
                    widget = self.sim_section.get_cell_from_dict(widget_index)
                    if not isinstance(widget, BaseWireCell):
                        raise Exception('animate_frame retrieved widget is not a basewirecell')
                    if node_value == "1":
                        widget.set_on_color()
                    elif node_value == "0":
                        widget.set_off_color()
                    elif node_value == "N":
                        widget.set_high_impedance_color()
                    else:
                        raise Exception("invalid node value")

    def next_simulation_frame(self) -> None:
        if self.__animate:
            if self.__animation_frame_num < len(self.__animation_frames) - 1:
                self.__animation_frame_num += 1
                self.__animate_frame()

    def prev_simulation_frame(self) -> None:
        if self.__animate:
            if self.__animation_frame_num > 0:
                self.__animation_frame_num -= 1
                self.__animate_frame()


