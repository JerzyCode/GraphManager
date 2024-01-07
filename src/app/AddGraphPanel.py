import customtkinter
import src.app.graph.DirectedGraph as directedGraph
import src.app.graph.UndirectedGraph as undirectedGraph
import src.app.graph.Digraph as digraph
from src.app.utils.const import *


class AddGraphPanel(customtkinter.CTk):
    def __init__(self, canvas, drawer):
        super().__init__()
        self.is_directed = False
        self.is_digraph = False
        self.is_weighted = False
        self.graph = None
        self.canvas = canvas
        self.drawer = drawer

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{ADD_GRAPH_WINDOW_WIDTH}x{ADD_GRAPH_WINDOW_HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
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
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # params frame
        self.params_frame = customtkinter.CTkFrame(self)
        self.params_frame.grid(row=0, column=1, rowspan=3, padx=(20, 30), pady=(20, 0), sticky="nsew")
        self.frame_label = customtkinter.CTkLabel(self.params_frame, text='GRAPH PARAMS',
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frame_label.grid(row=0, column=2, pady=10, padx=(120, 0))

        self.size_label = customtkinter.CTkLabel(self.params_frame, text='Enter number of vertexes:',
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.size_label.grid(row=1, column=2, padx=(10, 0), pady=(20, 0), sticky="nsew")
        self.size_entry = customtkinter.CTkEntry(self.params_frame, placeholder_text="size", width=100)
        self.size_entry.insert(0, '10')
        self.size_entry.grid(row=1, column=3, rowspan=1, padx=(20, 20), pady=(20, 0))

        self.density_label = customtkinter.CTkLabel(self.params_frame, text='Edges density (0 to 1):',
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.density_label.grid(row=2, column=2, padx=(10, 0), pady=(20, 0), sticky="nsew")
        self.density_entry = customtkinter.CTkEntry(self.params_frame, placeholder_text="size", width=100)
        self.density_entry.insert(0, '0.5')
        self.density_entry.grid(row=2, column=3, rowspan=1, padx=(20, 20), pady=(20, 0))

    def switch_directed(self):
        self.is_directed = not self.is_directed

    def switch_digraph(self):
        self.is_digraph = not self.is_digraph

    def switch_weighted(self):
        self.is_weighted = not self.is_weighted

    def on_close(self):
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
                                                    self.canvas.winfo_height())
            elif self.is_directed:
                self.graph = directedGraph.generate_graph(graph_size, float(p),
                                                          self.canvas.winfo_width(),
                                                          self.canvas.winfo_height())
            else:
                self.graph = undirectedGraph.generate_graph(graph_size, float(p),
                                                            self.canvas.winfo_width(),
                                                            self.canvas.winfo_height())
            self.drawer.draw_graph(self.graph)
            self.withdraw()

    def show_add_graph_panel_visible(self):
        self.deiconify()
