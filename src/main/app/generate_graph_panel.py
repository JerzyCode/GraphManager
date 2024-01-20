import customtkinter

import src.main.app.graph.digraph as digraph
import src.main.app.graph.directed_graph as directed_graph
import src.main.app.graph.undirected_graph as undirected_graph
from src.main.app.graph.graph import Graph
from src.main.app.graph.handlers.canvas_handler import CanvasHandler
from src.main.app.utils.constants import *


class GenerateGraphPanel(customtkinter.CTk):
    def __init__(self, canvas, drawer):
        super().__init__()
        self.is_directed = False
        self.is_digraph = False
        self.is_weighted = False
        self.is_custom = False
        self.canvas = canvas
        self.drawer = drawer
        self.graph = Graph([], self.is_weighted,
                           self.canvas.winfo_width(),
                           self.canvas.winfo_height())

        # configure window
        self.title("Add Graph")
        self.geometry(f"{ADD_GRAPH_WINDOW_WIDTH}x{ADD_GRAPH_WINDOW_HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.resizable(False, False)
        self.withdraw()

        # create main entry and button
        self.generate_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                       text='Generate Graph',
                                                       text_color=("gray10", "#DCE4EE"), command=self.generate_graph)
        self.generate_button.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # checkbox frame
        self.checkbox_frame = customtkinter.CTkFrame(self)
        self.checkbox_frame.grid(row=0, column=0, rowspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_frame, text='Directed',
                                                    command=self.switch_directed)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")

        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_frame, text='Digraph',
                                                    command=self.switch_digraph)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n", )

        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_frame, text='Weighted',
                                                    command=self.switch_weighted)
        self.checkbox_3.grid(row=3, column=0, pady=(20, 0), padx=20, sticky="n")

        # params frame
        self.params_frame = customtkinter.CTkFrame(self)
        self.params_frame.grid(row=0, column=1, rowspan=3, padx=(20, 30), pady=(20, 0), sticky="nsew")
        self.frame_label = customtkinter.CTkLabel(self.params_frame, text='GRAPH PARAMS',
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frame_label.grid(row=0, column=2, pady=10, padx=(120, 0))

        self.size_label = customtkinter.CTkLabel(self.params_frame, text='Enter number of vertexes:',
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.size_label.grid(row=1, column=2, padx=(10, 0), pady=(20, 0), sticky="nsew")
        self.size_entry = customtkinter.CTkEntry(self.params_frame, placeholder_text="size", width=100,
                                                 fg_color=GRAPH_BG_COLOR)
        self.size_entry.insert(0, '10')
        self.size_entry.grid(row=1, column=3, rowspan=1, padx=(20, 20), pady=(20, 0))

        self.density_label = customtkinter.CTkLabel(self.params_frame, text='Edges density (0 to 1):',
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.density_label.grid(row=2, column=2, padx=(10, 0), pady=(20, 0), sticky="nsew")
        self.density_entry = customtkinter.CTkEntry(self.params_frame, placeholder_text="size", width=100,
                                                    fg_color=GRAPH_BG_COLOR)
        self.density_entry.insert(0, '0.5')
        self.density_entry.grid(row=2, column=3, rowspan=1, padx=(20, 20), pady=(20, 0))

        self.canvas_handler = CanvasHandler(self.canvas, self.drawer, self.graph, self.is_directed, self.is_digraph)

    def switch_directed(self):
        self.canvas_handler.change_is_directed()
        self.is_directed = not self.is_directed

    def switch_digraph(self):
        self.canvas_handler.change_is_digraph()
        self.is_digraph = not self.is_digraph

    def switch_weighted(self):
        self.is_weighted = not self.is_weighted

    def _on_close(self):
        self.withdraw()

    def show_add_graph_panel_visible(self):
        self.deiconify()

    def generate_graph(self):
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
            self.withdraw()

    def show_add_graph_panel_visible(self):
        self.deiconify()
