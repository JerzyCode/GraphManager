from src.app.AddGraphPanel import AddGraphPanel
from src.app.graph.Graph import binary_search, depth_search
from src.app.graph.graphics.Drawer import Drawer
from src.app.utils.AppUtils import *

is_directed = True
is_weighted = True


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.resizable(True, True)
        self.root.title('Graph Manager')
        self.input_size = None
        self.input_p = None
        self.add_graph_panel = None
        self._create_gui()

    def _create_gui(self):
        pixel_virtual = tk.PhotoImage(width=1, height=1)
        # BUTTONS PANEL
        buttons_panel = tk.Frame(self.root, padx=5, pady=5, bg=BUTTONS_PANEL_BG_COLOR)
        buttons_panel.pack(side=tk.LEFT, fill=tk.BOTH)
        label = tk.Label(buttons_panel, text='FUNCTIONS', font=FONT, bg=BUTTONS_PANEL_BG_COLOR, bd=0,
                         fg=BUTTONS_PANEL_SIZE_FG_COLOR, pady=5)
        label.pack()
        # GRAPH PANEL
        graph_panel = tk.PanedWindow(orient='horizontal', width=GRAPH_VIEW_WIDTH, height=GRAPH_VIEW_HEIGHT, bd=0)
        graph_panel.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(graph_panel, bg=GRAPH_BG_COLOR)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.drawer = Drawer(self.canvas)
        self.add_graph_panel = AddGraphPanel(self.canvas, self.drawer)
        self.create_all_buttons(buttons_panel, pixel_virtual)
        # self.custom_graph()

        self.root.mainloop()

    def run_dfs(self):
        graph = self.add_graph_panel.graph
        if graph and self.drawer:
            depth_search(graph, self.drawer)

    def run_bfs(self):
        graph = self.add_graph_panel.graph
        try:
            if graph and self.drawer and len(graph.V) > 0:
                binary_search(graph, self.drawer)
        except (NameError, AttributeError, TypeError):
            print('graph is not defined')
            pass

    def refresh_graph(self):
        graph = self.add_graph_panel.graph
        if self.drawer:
            self.drawer.refresh_all(graph)

    def create_all_buttons(self, parent, image):
        create_button(parent, image, "Add Graph", self.add_graph_view_set_visible)
        create_button(parent, image, "Refresh Graph", self.refresh_graph)
        create_button(parent, image, "DFS", self.run_dfs)
        create_button(parent, image, "BFS", self.run_bfs)

    def create_all_inputs(self, parent):
        self.input_size = create_input(parent, 'size:', 7)
        self.input_p = create_input(parent, 'p:', 7)

    def add_graph_view_set_visible(self):
        self.canvas.delete('all')
        self.add_graph_panel.set_visible()
