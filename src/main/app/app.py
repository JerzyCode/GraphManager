import customtkinter

from src.main.app.graph.graphics.drawer import Drawer
from src.main.app.graph.handlers.canvas_handler import CanvasHandler
from src.main.app.ui.panels.add_graph_window import AddGraphWindow
from src.main.app.ui.panels.algorithms_window import AlgorithmsWindow
from src.main.app.ui.panels.generate_graph_window import GenerateGraphWindow
from src.main.app.utils.constants import *

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)


def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)


def _on_save_graph_btn():
    print('save graph')


def _on_load_graph_btn():
    print('load graph')


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.canvas_handler = None
        self.graph = None
        self.weight_hidden = False

        self._configure_window()
        self._create_sidebar_frame()
        self._create_graph_display_frame()

    def _configure_window(self):
        self.title("Graph Manager")
        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+0+0")
        self.protocol("WM_DELETE_WINDOW", self._on_close_btn)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((1, 2), weight=1)

    def _create_sidebar_frame(self):
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=1, column=0, rowspan=4, sticky="nsew")

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Graph Manager", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.add_graph_button = customtkinter.CTkButton(self.sidebar_frame, text='Add Graph', command=self._on_add_graph_btn)
        self.add_graph_button.grid(row=1, column=0, padx=20, pady=10)

        self.generate_graph_button = customtkinter.CTkButton(self.sidebar_frame, text='Generate Graph', command=self._on_generate_graph_btn)
        self.generate_graph_button.grid(row=2, column=0, padx=20, pady=10)

        self.save_graph_button = customtkinter.CTkButton(self.sidebar_frame, text='Save Graph', command=_on_save_graph_btn)
        self.save_graph_button.grid(row=3, column=0, padx=20, pady=10)

        self.load_graph_button = customtkinter.CTkButton(self.sidebar_frame, text='Load Graph', command=_on_load_graph_btn)
        self.load_graph_button.grid(row=4, column=0, padx=20, pady=10)

        self.algorithms_button = customtkinter.CTkButton(self.sidebar_frame, text='Algorithms', command=self._on_algorithms_button, fg_color='green')
        self.algorithms_button.grid(row=4, column=0, padx=20, pady=10)

        self.refresh_button = customtkinter.CTkButton(self.sidebar_frame, text='Refresh Graph', command=self._on_refresh_graph_btn)
        self.refresh_button.grid(row=5, column=0, padx=20, pady=10)

        self.refresh_button = customtkinter.CTkButton(self.sidebar_frame, text='Clear Graph', command=self._on_clear_graph_btn)
        self.refresh_button.grid(row=6, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=8, column=0, padx=20, pady=(10, 10))

    def _create_graph_display_frame(self):
        self.canvas = customtkinter.CTkCanvas(self, bg=GRAPH_BG_COLOR, bd=0, highlightthickness=0, relief='ridge')
        self.drawer = Drawer(self.canvas)
        self.add_graph_window = AddGraphWindow(self._set_params_add_graph)
        self.generate_graph_window = GenerateGraphWindow(self.canvas, self.drawer, self._on_graph_generated_hook,
                                                         self.add_graph_window.enable_options)
        self.algorithms_window = AlgorithmsWindow(self.drawer, self.disable_buttons, self.enable_buttons)
        self.canvas.grid(row=1, column=1, rowspan=5, columnspan=2, padx=55, pady=5, sticky="nsew")

    def _on_refresh_graph_btn(self):
        graph = self.graph
        if self.drawer:
            self.drawer.refresh_all(graph)

    def _on_generate_graph_btn(self):
        self.generate_graph_window.show_generate_graph_window_visible()
        self.add_graph_window.disable_options()

    def _on_add_graph_btn(self):
        self.add_graph_window.show_add_graph_panel()

    def _on_algorithms_button(self):
        self.algorithms_window.show_algorithms_window_visible()

    def _on_graph_generated_hook(self):
        graph = self.generate_graph_window.graph
        self.graph = graph
        self.algorithms_window.graph = graph
        self.add_graph_button.configure(state='disabled')

    def _set_params_add_graph(self, is_directed, is_digraph, is_weighted):
        print('add_graph_set_params')
        self.canvas_handler = CanvasHandler(self.canvas, self.drawer, is_directed, is_digraph, is_weighted)
        graph = self.canvas_handler.graph
        self.graph = graph
        self.algorithms_window.graph = graph

    def _on_close_btn(self):
        self.add_graph_window.destroy()
        self.generate_graph_window.destroy()
        self.algorithms_window.destroy()
        self.destroy()

    def _on_clear_graph_btn(self):
        self.add_graph_button.configure(state='normal')
        self.add_graph_window.set_params_button_state_normal()
        self.drawer.erase_all()
        self.generate_graph_window.canvas_handler = None
        self.generate_graph_window.graph = None
        self.algorithms_window.graph = None
        self.graph = None
        if self.canvas_handler is not None:
            self.canvas_handler.unbind()

    def disable_buttons(self):
        self.refresh_button.configure(state='disabled')

    def enable_buttons(self):
        self.refresh_button.configure(state='normal')
