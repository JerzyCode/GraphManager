import customtkinter

import src.main.app.graph.digraph as digraph
import src.main.app.graph.directed_graph as directed_graph
import src.main.app.graph.undirected_graph as undirected_graph
import tests.main.app.graph.graph_factory as factory
from src.main.app.graph.graph import Graph
from src.main.app.ui.drawing.canvas_handler import CanvasHandler
from src.main.app.ui.utils.params_checkbox_frame import ParamsCheckboxFrame
from src.main.app.ui.utils.slider_frame import SliderFrame
from src.main.app.utils.constants import *

global input_box_bg_color, input_box_fg_color


class GenerateGraphFrame(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root, width=LEFT_FRAME_WIDTH)
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
        # self._configure_window()
        self.grid_rowconfigure(5, weight=1)
        self._create_params_frame()

    def _configure_window(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def _create_params_frame(self):

        self.frame_label = customtkinter.CTkLabel(self, text='GENERATE GRAPH', font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frame_label.grid(row=0, column=0, pady=10, padx=20)

        self.checkbox_frame = ParamsCheckboxFrame(self)
        self.checkbox_frame.grid(row=5, column=0, pady=10, padx=20)

        self.vertex_slider_frame = SliderFrame(self, "Number of vertexes: ")
        self.vertex_slider_frame.grid(row=2, column=0, pady=10, padx=20, sticky='nsew')
        self.vertex_slider_frame.slider.set(10)
        self.vertex_slider_frame.insert_value('10')

        self.density_slider_frame = SliderFrame(self, "Density of edges: ")
        self.density_slider_frame.grid(row=3, column=0, pady=10, padx=20, sticky='nsew')
        self.density_slider_frame.insert_value(50)

        self.generate_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text='Generate Graph',
                                                       text_color=("gray10", "#DCE4EE"), command=self._on_generate_graph)
        self.generate_button.grid(row=6, column=0, padx=20, pady=(20, 10))

        close_button = customtkinter.CTkButton(self, text="Close", command=self.close_modal)
        close_button.grid(row=7, column=0, padx=20, pady=(10, 20))

    def close_modal(self):
        self.destroy()

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
        size = self.vertex_slider_frame.get_value()
        p = self.density_slider_frame.get_value()
        if not p or not p.isdigit() or int(p) < 0 or int(p) > 100:
            return
        p = int(p) * 0.01
        if size and size.isdigit() and 100 >= int(size) >= 0:
            self.canvas.delete('all')
            graph_size = int(size)
            if self.is_digraph:
                self.graph = digraph.generate_graph(graph_size, p,
                                                    self.canvas.winfo_width(),
                                                    self.canvas.winfo_height(),
                                                    self.is_weighted)
            elif self.is_directed:
                self.graph = directed_graph.generate_graph(graph_size, p,
                                                           self.canvas.winfo_width(),
                                                           self.canvas.winfo_height(),
                                                           self.is_weighted)
            else:
                self.graph = undirected_graph.generate_graph(graph_size, p,
                                                             self.canvas.winfo_width(),
                                                             self.canvas.winfo_height(),
                                                             self.is_weighted)
            self.root.graph = self.graph
            self.drawer.draw_graph(self.graph)
