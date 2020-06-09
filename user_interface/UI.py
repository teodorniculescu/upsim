import kivy
kivy.require("1.11.1")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from user_interface.section.SimulationPanel import SimulationPanel
from Simulation import Simulation


class ButtonBar(BoxLayout):
    pass


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
