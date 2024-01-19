import customtkinter

import src.main.app.utils.algorithms as algorithm
from src.main.app.generate_graph_panel import GenerateGraphPanel
from src.main.app.graph.graphics.drawer import Drawer
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
        self.weight_hidden = False

        # configure window
        self.title("Graph Manager")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Graph Manager",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.generate_graph = customtkinter.CTkButton(self.sidebar_frame, text='Add Graph',
                                                      command=self._on_add_graph_view_visible)
        self.generate_graph.grid(row=1, column=0, padx=20, pady=10)
        self.bfs_button = customtkinter.CTkButton(self.sidebar_frame, text='BFS', command=self._on_run_bfs)
        self.bfs_button.grid(row=2, column=0, padx=20, pady=10)
        self.dfs_button = customtkinter.CTkButton(self.sidebar_frame, text='DFS', command=self._on_run_dfs)
        self.dfs_button.grid(row=3, column=0, padx=20, pady=10)
        self.kruskal_button = customtkinter.CTkButton(self.sidebar_frame, text='Kruskal Algorithm',
                                                      command=self._on_kruskal_algorithm)
        self.kruskal_button.grid(row=4, column=0, padx=20, pady=10)
        # self.ex_button = customtkinter.CTkButton(self.sidebar_frame, text='Exercise Algorithm',
        #                                          command=self._on_ex_algorithm)
        # self.ex_button.grid(row=4, column=0, padx=20, pady=10)
        self.refresh_button = customtkinter.CTkButton(self.sidebar_frame, text='Refresh Graph',
                                                      command=self._on_refresh_graph)
        self.refresh_button.grid(row=5, column=0, padx=20, pady=10)

        # self.hide_weights_button = customtkinter.CTkButton(self.sidebar_frame, text='Hide weights',
        #                                                    command=self.on_hide_weights)
        # self.hide_weights_button.grid(row=5, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=8, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=change_scaling_event)
        self.scaling_option_menu.grid(row=10, column=0, padx=20, pady=(10, 20))

        # graph display
        self.canvas = customtkinter.CTkCanvas(self, bg=GRAPH_BG_COLOR, bd=0, highlightthickness=0,
                                              relief='ridge')
        self.drawer = Drawer(self.canvas)
        self.add_graph_panel = GenerateGraphPanel(self.canvas, self.drawer)
        self.canvas.grid(row=0, column=1, rowspan=5, columnspan=2, padx=55, pady=5, sticky="nsew")

    def _on_run_dfs(self):
        graph = self.add_graph_panel.graph
        if graph and self.drawer:
            algorithm.depth_search(graph, self.drawer)

    def _on_run_bfs(self):
        graph = self.add_graph_panel.graph
        try:
            if graph and self.drawer and len(graph.V) > 0:
                algorithm.binary_search(graph, self.drawer)
        except (NameError, AttributeError, TypeError):
            print('graph is not defined')
            pass

    def _on_refresh_graph(self):
        graph = self.add_graph_panel.graph
        if self.drawer:
            self.drawer.refresh_all(graph)

    def _on_add_graph_view_visible(self):
        self.add_graph_panel.show_add_graph_panel_visible()

    def _on_close(self):
        self.add_graph_panel.destroy()
        self.destroy()

    def _on_kruskal_algorithm(self):
        graph = self.add_graph_panel.graph
        # kruskal_algorithm(graph, self.drawer)
        try:
            if graph and self.drawer and len(graph.V) > 0 and graph.is_weighted:
                algorithm.kruskal_algorithm(graph, self.drawer)
        except (NameError, AttributeError, TypeError):
            print('graph is not defined')
            pass

    def _on_hide_weights(self):
        if not self.weight_hidden:
            self.drawer.hide_all_weights(self.add_graph_panel.graph)
            self.hide_weights_button.configure(text="Show weights")
        else:
            self.hide_weights_button.configure(text="Hide weights")
            self.drawer.draw_all_weights(self.add_graph_panel.graph)
        self.weight_hidden = not self.weight_hidden

    def _on_ex_algorithm(self):
        ex_4(self.add_graph_panel.graph, '1',self.drawer, 3)

        # self.weight_hidden = not self.weight_hidden
        # self.drawer.hide_all_weights(self.add_graph_panel.graph)
