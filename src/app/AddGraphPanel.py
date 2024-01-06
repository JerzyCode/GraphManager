import tkinter
import src.app.graph.DirectedGraph as directedGraph
import src.app.graph.UndirectedGraph as undirectedGraph
import src.app.graph.Digraph as digraph

from src.app.utils.AppUtils import *
from src.app.utils.const import *


class AddGraphPanel(tk.Toplevel):
    def __init__(self, canvas, drawer):
        super().__init__()
        self.create_button = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.resizable(False, False)
        self.title("Add Graph")
        self.config(bg=BUTTONS_PANEL_BG_COLOR)
        self.geometry(f'{ADD_GRAPH_WINDOW_WIDTH}x{ADD_GRAPH_WINDOW_HEIGHT}+{WINDOW_WIDTH + 80}+{10}')
        self.input_size = None
        self.input_p = None
        self.panel = None
        self.is_digraph = False
        self.is_directed = False
        self.graph = None
        self.canvas = canvas
        self.drawer = drawer
        self.create_gui()
        self.withdraw()

    def show_add_graph_panel_visible(self):
        self.deiconify()

    def on_close(self):
        self.withdraw()

    def create_all_inputs(self, parent):
        self.input_size = create_input(parent, 'Vertex number:', 5)
        self.input_size.insert(0, 8)
        self.input_p = create_input(parent, 'probability:', 5)

    def create_gui(self):
        self.panel = tk.Frame(self, padx=10, pady=10, bg=BUTTONS_PANEL_BG_COLOR)
        size_window = tk.PanedWindow(self.panel, orient=tk.HORIZONTAL)
        self.create_all_inputs(size_window)
        size_window.pack(expand=False, pady=25)
        self.create_button = create_button_no_pack(self.panel, None,
                                                   "Generate Graph", self.generate_and_draw_graph)

        checkboxes = tk.PanedWindow(self.panel, orient=tk.HORIZONTAL)

        checkbox = tk.Checkbutton(checkboxes, text='Is Directed',
                                  bg=BUTTONS_PANEL_BG_COLOR,
                                  font=FONT,
                                  fg=BUTTON_BG_COLOR,
                                  command=self.switch_directed, )
        checkbox.pack(side=tk.LEFT)

        checkbox = tk.Checkbutton(checkboxes, text='Is Digraph',
                                  bg=BUTTONS_PANEL_BG_COLOR,
                                  font=FONT,
                                  fg=BUTTON_BG_COLOR,
                                  command=self.switch_digraph)
        checkbox.pack(side=tk.RIGHT)
        checkboxes.pack(pady=50)

        self.create_button.pack(side=tk.BOTTOM)
        self.panel.pack(fill=tkinter.BOTH, expand=True)

    def generate_and_draw_graph(self):
        size = self.input_size.get()
        p = self.input_p.get()
        if len(p) == 0:
            p = 0.5
        if size and size.isdigit() and int(size) <= 100:
            self.canvas.delete('all')
            graph_size = int(self.input_size.get())
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

    def switch_directed(self):
        self.is_directed = not self.is_directed

    def switch_digraph(self):
        self.is_digraph = not self.is_digraph
