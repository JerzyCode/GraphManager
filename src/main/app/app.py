import customtkinter

import src.main.app.data.database as db
from src.main.app.graph.digraph import Digraph
from src.main.app.graph.directed_graph import DirectedGraph
from src.main.app.ui.drawing.canvas_handler import CanvasHandler
from src.main.app.ui.drawing.drawer import Drawer, change_appearance_mode
from src.main.app.ui.drawing.edge_drawer import EdgeDrawer
from src.main.app.ui.drawing.vertex_drawer import VertexDrawer
from src.main.app.ui.frames.algorithms_frame import AlgorithmsFrame
from src.main.app.ui.windows.add_graph_window import AddGraphWindow
from src.main.app.ui.windows.generate_graph_window import GenerateGraphWindow, change_generate_graph_window_appearance_mode
from src.main.app.ui.windows.save_load_graph_window import SaveLoadGraphWindow
from src.main.app.ui.windows.set_weight_window import change_set_weight_window_appearance_mode
from src.main.app.utils.constants import *
from src.main.app.utils.logger import setup_logger

logger = setup_logger("App")

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)


def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)


class App(customtkinter.CTk):
    def __init__(self, db_url):
        super().__init__()
        logger.debug("App starting...")
        db.start_database(db_url)
        self.canvas_handler = None
        self.graph = None
        self.weight_hidden = False
        self._configure_window()
        self._create_sidebar_frame()
        self._create_graph_display_frame()
        self.save_load_graph_window = SaveLoadGraphWindow()
        # self.generate_graph_window.generate_graph_mock()

    def _configure_window(self):
        logger.debug("Configuring Window...")
        self.title("Graph Manager")
        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width - WINDOW_WIDTH) / 2)
        center_y = int((screen_height - WINDOW_HEIGHT) / 2)

        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}")

        self.protocol("WM_DELETE_WINDOW", self._on_close_btn)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

    def _create_sidebar_frame(self):
        logger.debug("Creating Sidebar Frame...")
        self.sidebar_frame = customtkinter.CTkFrame(self, width=LEFT_FRAME_WIDTH, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=11, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Graph Manager", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.add_graph_button = customtkinter.CTkButton(self.sidebar_frame, text='Add Graph', command=self._on_add_graph_btn)
        self.add_graph_button.grid(row=1, column=0, padx=20, pady=10)

        self.generate_graph_button = customtkinter.CTkButton(self.sidebar_frame, text='Generate Graph', command=self._on_generate_graph_btn)
        self.generate_graph_button.grid(row=2, column=0, padx=20, pady=10)

        self.save_graph_button = customtkinter.CTkButton(self.sidebar_frame, text='Save Graph', command=self._on_save_graph_btn)
        self.save_graph_button.grid(row=3, column=0, padx=20, pady=10)

        self.load_graph_button = customtkinter.CTkButton(self.sidebar_frame, text='Load Graph', command=self._on_load_graph_btn)
        self.load_graph_button.grid(row=4, column=0, padx=20, pady=10)

        self.algorithms_button = customtkinter.CTkButton(self.sidebar_frame, text='Algorithms', command=self._on_algorithms_button, fg_color='green')
        self.algorithms_button.grid(row=5, column=0, padx=20, pady=10)

        self.refresh_button = customtkinter.CTkButton(self.sidebar_frame, text='Refresh Graph', command=self._on_refresh_graph_btn)
        self.refresh_button.grid(row=6, column=0, padx=20, pady=10)

        self.clear_button = customtkinter.CTkButton(self.sidebar_frame, text='Clear Graph', command=self._on_clear_graph_btn)
        self.clear_button.grid(row=7, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark"],
                                                                       command=self._change_appearance_mode)
        self.appearance_mode_option_menu.set("Dark")
        self.appearance_mode_option_menu.grid(row=10, column=0, padx=20, pady=(10, 20))

    def _create_graph_display_frame(self):
        logger.debug("Creating Graph Display Frame...")
        self.canvas = customtkinter.CTkCanvas(self, bg=GRAPH_BG_COLOR_DARK, bd=0, highlightthickness=0, relief='ridge')
        self.edge_drawer = EdgeDrawer(self.canvas)
        self.vertex_drawer = VertexDrawer(self.canvas)
        self.drawer = Drawer(self.canvas, self.edge_drawer, self.vertex_drawer)
        self.add_graph_window = AddGraphWindow(self._set_params_add_graph)
        self.generate_graph_window = GenerateGraphWindow(self)
        self.canvas.grid(row=0, column=1, rowspan=11, columnspan=2, padx=5, pady=5, sticky="nsew")

    def _on_refresh_graph_btn(self):
        logger.debug("Refreshing Graph")
        graph = self.graph
        if self.drawer:
            self.drawer.refresh_all(graph)

    def _on_generate_graph_btn(self):
        logger.debug("On Generate Graph")
        self.generate_graph_window.show_generate_graph_window_visible()
        self.add_graph_window.disable_options()

    def _on_add_graph_btn(self):
        logger.debug("On Add Graph")
        self.add_graph_window.show_add_graph_window()

    def _on_algorithms_button(self):
        frame = AlgorithmsFrame(self, self.graph)
        self.open_frame(frame)

    def on_graph_generated_hook(self):
        graph = self.generate_graph_window.graph
        self.set_graph(graph)
        self.add_graph_button.configure(state='disabled')

    def set_graph(self, graph):
        self.graph = graph
        self.save_load_graph_window.graph = graph
        self.drawer.graph = graph
        self.canvas_handler.set_graph(graph)

    def _set_params_add_graph(self, is_directed, is_digraph, is_weighted):
        logger.debug("Clearing Graph")
        self.canvas_handler = CanvasHandler(self, is_directed, is_digraph, is_weighted)
        graph = self.canvas_handler.graph
        self.set_graph(graph)

    def _on_close_btn(self):
        logger.debug("Closing App")
        # db.clear_tables()
        self.add_graph_window.destroy()
        self.generate_graph_window.destroy()
        self.save_load_graph_window.destroy()
        self.destroy()

    def _on_clear_graph_btn(self):
        logger.debug("Clearing Graph")
        self.add_graph_button.configure(state='normal')
        self.add_graph_window.set_params_button_state_normal()
        self.drawer.erase_all()
        self.generate_graph_window.canvas_handler = None
        self.generate_graph_window.graph = None
        self.graph = None
        if self.canvas_handler is not None:
            self.canvas_handler.enabled = False
            self.canvas_handler.unbind()

    def _change_appearance_mode(self, new_appearance_mode: str):
        logger.debug("Changing appearance mode to: " + new_appearance_mode)
        change_appearance_mode_event(new_appearance_mode)
        if new_appearance_mode == "Light":
            self.canvas.configure(bg=GRAPH_BG_COLOR_LIGHT)
            change_appearance_mode("Light")
            change_generate_graph_window_appearance_mode("Light")
            change_set_weight_window_appearance_mode("Light")
        elif new_appearance_mode == "Dark":
            self.canvas.configure(bg=GRAPH_BG_COLOR_DARK)
            change_appearance_mode("Dark")
            change_generate_graph_window_appearance_mode("Dark")
            change_set_weight_window_appearance_mode("Dark")
        self.drawer.refresh_all(self.graph)

    def _on_save_graph_btn(self):
        self.save_load_graph_window.show_save_load_graph_window_visible('save')

    def _on_load_graph_btn(self):
        self.save_load_graph_window.show_save_load_graph_window_visible('load', load_hook=self.load_graph_hook)

    def load_graph_hook(self, graph):
        self.canvas_handler = CanvasHandler(self, isinstance(graph, DirectedGraph), isinstance(graph, Digraph), graph.is_weighted)
        self._on_clear_graph_btn()
        self.graph = graph
        self.set_graph(graph)
        self.drawer.draw_graph(graph)

    def open_frame(self, frame):
        frame.grid(row=0, column=0, rowspan=11, sticky="nsew")
