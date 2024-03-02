import customtkinter

import src.main.app.graph.digraph as digraph
import src.main.app.graph.directed_graph as directed_graph
import src.main.app.graph.undirected_graph as undirected_graph
import tests.main.app.graph.graph_factory as factory
from src.main.app.graph.graph import Graph
from src.main.app.ui.drawing.canvas_handler import CanvasHandler
from src.main.app.ui.utils.params_checkbox_frame import ParamsCheckboxFrame
from src.main.app.utils.constants import *

global input_box_bg_color, input_box_fg_color


def change_generate_graph_window_appearance_mode(new_appearance_mode: str):
    global input_box_bg_color, input_box_fg_color
    if new_appearance_mode == "Light":
        input_box_fg_color = GRAPH_BG_COLOR_LIGHT
    elif new_appearance_mode == "Dark":
        input_box_fg_color = GRAPH_BG_COLOR_DARK


change_generate_graph_window_appearance_mode("Dark")


class GenerateGraphWindow(customtkinter.CTk):
    def __init__(self, root):
        super().__init__()
        self.canvas_handler = None
        self.is_directed = False
        self.is_digraph = False
        self.is_weighted = False
        self.is_custom = False
        self.root = root
        self.canvas = root.canvas
        self.drawer = root.drawer
        self.graph = Graph([], self.is_weighted,
                           self.canvas.winfo_width(),
                           self.canvas.winfo_height())
        self._configure_window()
        self.checkbox_frame = ParamsCheckboxFrame(self)
        self._create_params_frame()

    def _configure_window(self):
        self.title(GENERATE_GRAPH)
        self.minsize(GENERATE_GRAPH_WINDOW_WIDTH, GENERATE_GRAPH_WINDOW_HEIGHT)
        self.geometry(f"{GENERATE_GRAPH_WINDOW_WIDTH}x{GENERATE_GRAPH_WINDOW_HEIGHT}+0+{WINDOW_HEIGHT + 150}")
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.withdraw()

        self.generate_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text='Generate Graph',
                                                       text_color=("gray10", "#DCE4EE"), command=self._on_generate_graph)
        self.generate_button.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def _create_params_frame(self):
        self.params_frame = customtkinter.CTkFrame(self)
        self.params_frame.grid(row=0, column=1, rowspan=3, padx=(20, 30), pady=(20, 0), sticky="nsew")
        self.frame_label = customtkinter.CTkLabel(self.params_frame, text='GRAPH PARAMS', font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frame_label.grid(row=0, column=2, pady=10, padx=(120, 0))

        self.size_label = customtkinter.CTkLabel(self.params_frame, text='Enter number of vertexes:',
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.size_label.grid(row=1, column=2, padx=(10, 0), pady=(20, 0), sticky="nsew")
        self.size_entry = customtkinter.CTkEntry(self.params_frame, placeholder_text="size", width=100, bg_color=input_box_fg_color)
        self.size_entry.insert(0, '10')
        self.size_entry.grid(row=1, column=3, rowspan=1, padx=(20, 20), pady=(20, 0))

        self.density_label = customtkinter.CTkLabel(self.params_frame, text='Edges density (0 to 1):',
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.density_label.grid(row=2, column=2, padx=(10, 0), pady=(20, 0), sticky="nsew")
        self.density_entry = customtkinter.CTkEntry(self.params_frame, placeholder_text="size", width=100, bg_color=input_box_fg_color)
        self.density_entry.insert(0, '0.5')
        self.density_entry.grid(row=2, column=3, rowspan=1, padx=(20, 20), pady=(20, 0))

    def _on_close(self):
        self.withdraw()
        self.root.add_graph_window.enable_options()
        # self.enable_options()

    def _on_generate_graph(self):
        self._generate_graph()
        self.canvas_handler = CanvasHandler(self.root,
                                            self.is_directed,
                                            self.is_digraph,
                                            self.is_weighted,
                                            self.graph)
        self.root.canvas_handler = self.canvas_handler
        self.root.on_graph_generated_hook()

    def generate_graph_mock(self):
        self.graph = factory.generate_test_weighted_directed_graph()
        self.drawer.draw_graph(self.graph)
        self.canvas_handler = CanvasHandler(self.root,
                                            self.is_directed,
                                            self.is_digraph,
                                            self.is_weighted,
                                            self.graph)
        self.root.canvas_handler = self.canvas_handler
        self.root.on_graph_generated_hook()

    def _generate_graph(self):
        size = self.size_entry.get()
        p = self.density_entry.get()
        if len(p) == 0:
            p = 0.5
        if size and size.isdigit() and int(size) <= 100:
            self.canvas.delete('all')
            graph_size = int(size)
            if self.is_digraph:
                self.graph = digraph.generate_graph(graph_size, float(p),
                                                    self.canvas.winfo_width(),
                                                    self.canvas.winfo_height(),
                                                    self.is_weighted)
            elif self.is_directed:
                self.graph = directed_graph.generate_graph(graph_size, float(p),
                                                           self.canvas.winfo_width(),
                                                           self.canvas.winfo_height(),
                                                           self.is_weighted)
            else:
                self.graph = undirected_graph.generate_graph(graph_size, float(p),
                                                             self.canvas.winfo_width(),
                                                             self.canvas.winfo_height(),
                                                             self.is_weighted)
            self.drawer.draw_graph(self.graph)

    def show_generate_graph_window_visible(self):
        self.deiconify()
