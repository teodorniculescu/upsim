import kivy
kivy.require("1.11.1")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from user_interface.section.SimulationPanel import SimulationPanel
from simulation.Simulation import Simulation


class ButtonBar(BoxLayout):
    pass


class SimulationUI(BoxLayout):
    def __init__(self,
                 simulation: Simulation,
                 animate: bool,
                 **kwargs):
        super(SimulationUI, self).__init__(**kwargs)
        self.orientation = "vertical"
        #self.add_widget(ButtonBar())
        self.add_widget(
            SimulationPanel(simulation=simulation, animate=animate))


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
