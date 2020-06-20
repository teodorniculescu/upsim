import kivy
kivy.require("1.11.1")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from user_interface.section.SimulationPanel import SimulationPanel
from simulation.Simulation import Simulation
from kivy.core.window import Window


class ButtonBar(BoxLayout):
    simulation_panel: SimulationPanel

    def __init__(self,
                 simulation_panel: SimulationPanel,
                 **kwargs):
        super(ButtonBar, self).__init__(**kwargs)
        self.simulation_panel = simulation_panel


class SimulationUI(BoxLayout):
    simulation_panel: SimulationPanel

    def __init__(self,
                 simulation: Simulation,
                 animate: bool,
                 **kwargs):
        super(SimulationUI, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.simulation_panel = SimulationPanel(simulation=simulation, animate=animate)
        self.add_widget(ButtonBar(simulation_panel=self.simulation_panel))
        self.add_widget(self.simulation_panel)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == '=':
            self.simulation_panel.zoom_out()
        elif keycode[1] == '-':
            self.simulation_panel.zoom_in()
        elif keycode[1] == 'd':
            self.simulation_panel.move_right()
        elif keycode[1] == 'a':
            self.simulation_panel.move_left()
        elif keycode[1] == 'w':
            self.simulation_panel.move_up()
        elif keycode[1] == 's':
            self.simulation_panel.move_down()
        elif keycode[1] == '1':
            self.simulation_panel.prev_simulation_frame()
        elif keycode[1] == '2':
            self.simulation_panel.next_simulation_frame()
        return True


class UI(App):
    __simulation: Simulation
    __animate: bool

    def __init__(self,
                 simulation: Simulation,
                 animate: bool,
                 **kwargs):
        super(UI, self).__init__(**kwargs)
        self.__simulation = simulation
        self.__animate = animate

    def build(self):
        sim_ui = SimulationUI(
            simulation=self.__simulation,
            animate=self.__animate
        )
        return sim_ui
