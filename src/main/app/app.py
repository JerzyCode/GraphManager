import customtkinter

import src.main.app.utils.algorithms as algorithm
from src.main.app.graph.graphics.drawer import Drawer
from src.main.app.graph.handlers.canvas_handler import CanvasHandler
from src.main.app.panels.add_graph_window import AddGraphWindow
from src.main.app.panels.generate_graph_panel import GenerateGraphPanel
from src.main.app.utils.constants import *
from src.main.app.utils.study_ex_algorithms import ex_4

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)


def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)


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
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self._on_close_btn)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def _create_sidebar_frame(self):
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Graph Manager", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.add_graph_button = customtkinter.CTkButton(self.sidebar_frame, text='Add Graph', command=self._on_add_graph_btn)
        self.add_graph_button.grid(row=1, column=0, padx=20, pady=10)

        self.generate_graph = customtkinter.CTkButton(self.sidebar_frame, text='Generate Graph', command=self._on_generate_graph_btn)
        self.generate_graph.grid(row=2, column=0, padx=20, pady=10)

        self.bfs_button = customtkinter.CTkButton(self.sidebar_frame, text='BFS', command=self._on_run_bfs_btn)
        self.bfs_button.grid(row=3, column=0, padx=20, pady=10)

        self.dfs_button = customtkinter.CTkButton(self.sidebar_frame, text='DFS', command=self._on_run_dfs_btn)
        self.dfs_button.grid(row=4, column=0, padx=20, pady=10)

        self.kruskal_button = customtkinter.CTkButton(self.sidebar_frame, text='Kruskal Algorithm', command=self._on_kruskal_algorithm_btn)
        self.kruskal_button.grid(row=5, column=0, padx=20, pady=10)
        # self.ex_button = customtkinter.CTkButton(self.sidebar_frame, text='Exercise Algorithm',
        #                                          command=self._on_ex_algorithm)
        # self.ex_button.grid(row=4, column=0, padx=20, pady=10)
        self.refresh_button = customtkinter.CTkButton(self.sidebar_frame, text='Refresh Graph', command=self._on_refresh_graph_btn)
        self.refresh_button.grid(row=6, column=0, padx=20, pady=10)

        self.refresh_button = customtkinter.CTkButton(self.sidebar_frame, text='Clear Graph', command=self._on_clear_graph_btn)
        self.refresh_button.grid(row=7, column=0, padx=20, pady=10)

        # self.hide_weights_button = customtkinter.CTkButton(self.sidebar_frame, text='Hide weights',
        #                                                    command=self.on_hide_weights)
        # self.hide_weights_button.grid(row=5, column=0, padx=20, pady=10)
        #
        # self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        # self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        # self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
        #                                                                values=["Light", "Dark", "System"],
        #                                                                command=change_appearance_mode_event)
        # self.appearance_mode_option_menu.grid(row=8, column=0, padx=20, pady=(10, 10))
        # self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        # self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        # self.scaling_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
        #                                                        values=["80%", "90%", "100%", "110%", "120%"],
        #                                                        command=change_scaling_event)
        # self.scaling_option_menu.grid(row=10, column=0, padx=20, pady=(10, 20))

    def _create_graph_display_frame(self):
        self.canvas = customtkinter.CTkCanvas(self, bg=GRAPH_BG_COLOR, bd=0, highlightthickness=0, relief='ridge')
        self.drawer = Drawer(self.canvas)
        self.add_graph_window = AddGraphWindow(self._set_params_add_graph)
        self.generate_graph_window = GenerateGraphPanel(self.canvas, self.drawer, self._on_graph_generated_hook)
        self.canvas.grid(row=0, column=1, rowspan=5, columnspan=2, padx=55, pady=5, sticky="nsew")

    def _on_run_dfs_btn(self):
        graph = self.graph
        if graph and self.drawer:
            algorithm.depth_search(graph, self.drawer)

    def _on_run_bfs_btn(self):
        graph = self.graph
        try:
            if graph and self.drawer and len(graph.V) > 0:
                algorithm.binary_search(graph, self.drawer)
        except (NameError, AttributeError, TypeError):
            print('graph is not defined')
            pass

    def _on_kruskal_algorithm_btn(self):
        graph = self.graph
        try:
            if graph and self.drawer and len(graph.V) > 0 and graph.is_weighted:
                algorithm.kruskal_algorithm(graph, self.drawer)
        except (NameError, AttributeError, TypeError):
            print('graph is not defined')
            pass

    def _on_refresh_graph_btn(self):
        graph = self.graph
        if self.drawer:
            self.drawer.refresh_all(graph)

    def _on_generate_graph_btn(self):
        self.generate_graph_window.show_generate_graph_panel_visible()
        # self.graph = self.generate_graph_panel.graph

    def _on_graph_generated_hook(self):
        self.graph = self.generate_graph_window.graph
        self.add_graph_button.configure(state='disabled')

    def _on_add_graph_btn(self):
        self.add_graph_window.show_add_graph_panel()

    def _set_params_add_graph(self, is_directed, is_digraph, is_weighted):
        print('add_graph_set_params')
        self.canvas_handler = CanvasHandler(self.canvas, self.drawer, is_directed, is_digraph, is_weighted)
        self.graph = self.canvas_handler.graph

    def _on_close_btn(self):
        self.add_graph_window.destroy()
        self.generate_graph_window.destroy()
        self.destroy()

    def _on_clear_graph_btn(self):
        self.add_graph_button.configure(state='normal')
        self.add_graph_window.set_params_button_state_normal()
        self.drawer.erase_all()
        self.generate_graph_window.canvas_handler = None
        self.generate_graph_window.graph = None
        self.canvas_handler.unbind()
        self.graph = None
        print('clear graph')

    def _on_hide_weights(self):
        if not self.weight_hidden:
            self.drawer.hide_all_weights(self.generate_graph_window.graph)
            # self.hide_weights_button.configure(text="Show weights")
        else:
            # self.hide_weights_button.configure(text="Hide weights")
            self.drawer.draw_all_weights(self.generate_graph_window.graph)
        self.weight_hidden = not self.weight_hidden

    def _on_ex_algorithm(self):
        ex_4(self.generate_graph_window.graph, '1', self.drawer, 3)

        # self.weight_hidden = not self.weight_hidden
        # self.drawer.hide_all_weights(self.add_graph_panel.graph)
