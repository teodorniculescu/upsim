import kivy
kivy.require("1.11.1")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from user_interface.section.SimulationPanel import SimulationPanel
from simulation.Simulation import Simulation
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label


class ButtonBar(BoxLayout):
    simulation_panel: SimulationPanel

    def __init__(self,
                 simulation_panel: SimulationPanel,
                 **kwargs):
        super(ButtonBar, self).__init__(**kwargs)
        self.simulation_panel = simulation_panel

        zoom_widget = BoxLayout()
        zoom_widget.add_widget(Label(size_hint=(None, 1), text='Zoom'))
        zoom_widget.add_widget(Button(size_hint=(None, 1), text='In', on_press=self.callback_zoom_in))
        zoom_widget.add_widget(Button(size_hint=(None, 1), text='Out', on_press=self.callback_zoom_out))
        self.add_widget(zoom_widget)

        self.prev_frame = Button(size_hint=(None, 1), text='Prev', on_press=self.callback_prev_frame)
        self.next_frame = Button(size_hint=(None, 1), text='Next', on_press=self.callback_next_frame)
        self.frame_counter = Label(size_hint=(None, 1), text='0/1')
        frame_widget = BoxLayout()
        frame_widget.add_widget(Label(size_hint=(None, 1), text='Frame'))
        frame_widget.add_widget(self.prev_frame)
        frame_widget.add_widget(self.next_frame)
        frame_widget.add_widget(self.frame_counter)
        self.add_widget(frame_widget)
        self.change_frame_counter()

    def callback_zoom_in(self, instance):
        self.simulation_panel.zoom_in()

    def callback_zoom_out(self, instance):
        self.simulation_panel.zoom_out()

    def callback_next_frame(self, instance):
        self.simulation_panel.next_simulation_frame()
        self.change_frame_counter()

    def callback_prev_frame(self, instance):
        self.simulation_panel.prev_simulation_frame()
        self.change_frame_counter()

    def change_frame_counter(self) -> None:
        (current_counter, max_counter) = self.simulation_panel.get_frame_counter()
        self.frame_counter.text = str(current_counter) + "/" + str(max_counter)

class SimulationUI(BoxLayout):
    simulation_panel: SimulationPanel

    def __init__(self,
                 simulation: Simulation,
                 animate: bool,
                 **kwargs):
        super(SimulationUI, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.simulation_panel = SimulationPanel(simulation=simulation, animate=animate)
        self.button_bar = ButtonBar(simulation_panel=self.simulation_panel)
        self.add_widget(self.button_bar)
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
            self.button_bar.callback_prev_frame(instance=None)
        elif keycode[1] == '2':
            self.button_bar.callback_next_frame(instance=None)
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
