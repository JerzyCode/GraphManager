import tkinter as tk
from app.graph.Graph import generate_graph, depth_search, binary_search
from app.graph.graphics.Drawer import Drawer
from app.utils.const import *


is_directed = True

def create_button(parent, image, text, command):
    button = tk.Button(parent, image=image, text=text, command=command, font=FONT,
                       width=BUTTONS_VIEW_WIDTH, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, bd=0.5, compound="c")
    button.pack()
    return button


def create_input(parent, text, input_width):
    label = tk.Label(parent, text=text, font=FONT, bg=BUTTONS_PANEL_SIZE_BG_COLOR, bd=0,
                     fg=BUTTONS_PANEL_SIZE_FG_COLOR)
    entry = tk.Entry(parent, width=input_width, bg=BUTTONS_PANEL_BG_COLOR, fg=BUTTON_FG_COLOR, font=FONT)
    parent.add(label)
    parent.add(entry)
    return entry


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.resizable(True, True)
        self.root.title('Graph Manager')
        self.graph = None
        self.drawer = None
        self.input_size = None
        self.input_p = None
        self._create_gui()

    def _create_gui(self):
        pixel_virtual = tk.PhotoImage(width=1, height=1)
        # BUTTONS PANEL
        buttons_panel = tk.Frame(self.root, padx=5, pady=5, bg=BUTTONS_PANEL_BG_COLOR)
        buttons_panel.pack(side=tk.LEFT, fill=tk.BOTH)

        size_window = tk.PanedWindow(buttons_panel, orient=tk.HORIZONTAL)
        self.create_all_inputs(size_window)

        size_window.add(self.input_p)
        size_window.pack()


        ## GRAPH PANEL
        graph_panel = tk.PanedWindow(orient='horizontal', width=GRAPH_VIEW_WIDTH, height=GRAPH_VIEW_HEIGHT, bd=0)
        graph_panel.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(graph_panel, bg=GRAPH_BG_COLOR)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_all_buttons(buttons_panel, pixel_virtual)
        self.root.mainloop()

    def run_dfs(self):
        if self.graph and self.drawer:
            depth_search(self.graph, self.drawer)

    def run_bfs(self):
        try:
            if self.graph and self.drawer and len(self.graph.V) > 0:
                binary_search(self.graph, self.drawer)
        except (NameError, AttributeError, TypeError):
            print('graph is not defined')
            pass

    def refresh_graph(self):
        if self.drawer:
            self.drawer.refresh_all()


    def generate_and_draw_graph(self):
        size = self.input_size.get()
        p = self.input_p.get()
        if len(p) == 0:
            p = 0.5
        if size and size.isdigit() and int(size) <= 100:
            self.canvas.delete('all')
            graph_size = int(self.input_size.get())
            self.graph = generate_graph(graph_size, self.canvas, float(p), is_directed)
            self.drawer = Drawer(self.graph, self.canvas)

    def create_all_buttons(self, parent, image):
        create_button(parent, image, "Generate Graph", self.generate_and_draw_graph)
        create_button(parent, image, "Add Your Graph", lambda: self.create_add_graph_view(1))
        create_button(parent, image, "Refresh Graph", self.refresh_graph)
        create_button(parent, image, "DFS", self.run_dfs)
        create_button(parent, image, "BFS", self.run_bfs)

    def create_all_inputs(self, parent):
        self.input_size = create_input(parent, 'size:', 7)
        self.input_p = create_input(parent, 'p:', 7)

    def create_add_graph_view(self, size):
        self.canvas.delete('all')
