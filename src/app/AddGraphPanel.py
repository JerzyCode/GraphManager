from src.app.graph.Graph import generate_graph
from src.app.utils.AppUtils import *
from src.app.utils.const import *


class AddGraphPanel(tk.Toplevel):
    def __init__(self, canvas, drawer):
        super().__init__()
        self.resizable(False, False)
        self.title("Add Graph")
        self.config(bg=BUTTONS_PANEL_BG_COLOR)
        self.geometry(f'{ADD_GRAPH_WINDOW_WIDTH}x{ADD_GRAPH_WINDOW_HEIGHT}')
        self.input_size = None
        self.input_p = None
        self.panel = None
        self.is_weighted = False
        self.is_directed = False
        self.graph = None
        self.canvas = canvas
        self.drawer = drawer
        self.create_gui()
        self.withdraw()

    def set_visible(self):
        self.deiconify()

    def create_all_buttons(self, parent, image):
        create_button(parent, image, "Generate Graph", self.generate_and_draw_graph)
        create_button(parent, image, "Add Graph", lambda: print('add custom graph'))

    def create_all_inputs(self, parent):
        self.input_size = create_input(parent, 'Vertex number:', 5)
        self.input_size.insert(0, 5)
        self.input_p = create_input(parent, 'probability:', 5)

    def create_gui(self):
        self.panel = tk.Frame(self, padx=5, pady=5, bg=BUTTONS_PANEL_BG_COLOR)
        size_window = tk.PanedWindow(self.panel, orient=tk.HORIZONTAL)
        self.create_all_inputs(size_window)
        size_window.pack(expand=False)
        self.create_all_buttons(self.panel, None)

        checkbox = tk.Checkbutton(self.panel, text='Is Directed',
                                  bg=BUTTON_FG_COLOR,
                                  font=FONT,
                                  fg=BUTTON_BG_COLOR,
                                  command=self.switch_directed)
        checkbox.pack(anchor=tk.W)

        self.panel.pack()

    def generate_and_draw_graph(self):
        size = self.input_size.get()
        p = self.input_p.get()
        if len(p) == 0:
            p = 0.5
        if size and size.isdigit() and int(size) <= 100:
            self.canvas.delete('all')
            graph_size = int(self.input_size.get())
            self.graph = generate_graph(graph_size, float(p), self.is_weighted, self.is_directed,
                                        self.canvas.winfo_width(),
                                        self.canvas.winfo_height())
            self.drawer.draw_graph(self.graph)


    def switch_directed(self):
        self.is_directed = not self.is_directed

    def switch_weighted(self):
        self.is_weighted = not self.is_weighted
