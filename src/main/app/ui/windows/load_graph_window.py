import customtkinter

from src.main.app.repositories import graph_repository
from src.main.app.utils.constants import *
from src.main.app.utils.logger import setup_logger

logger = setup_logger("LoadGraphWindow")


class GraphScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command
        self.frames = []
        self.load_graph = None
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, width=200, text=item, command=self._on_check_box)
        remove_button = customtkinter.CTkButton(self, text='X', width=5, command=lambda i=item: self.remove_item(i))
        checkbox.grid(row=len(self.frames), column=0, pady=(0, 10), sticky='w')
        remove_button.grid(row=len(self.frames), column=1, pady=(0, 10), sticky='e')
        self.frames.append([checkbox, remove_button])

    def _on_check_box(self):
        selected = None
        for frame in self.frames:
            checkbox = frame[0]
            if checkbox.get() == 1:
                selected = checkbox
                break

        for frame in self.frames:
            checkbox = frame[0]
            if selected is not None:
                if checkbox != selected:
                    checkbox.configure(state='disabled')
                else:
                    self.load_graph = graph_repository.graphs.get(checkbox.cget('text'))
            else:
                checkbox.configure(state='normal')
        if selected is None:
            for frame in self.frames:
                frame[0].configure(state='normal')

    def enable_checkbox(self):
        for frame in self.frames:
            frame[0].configure(state='enabled')

    def remove_item(self, item):
        for frame in self.frames:
            name = frame[0].cget("text")
            if item == name:
                frame[0].destroy()
                frame[1].destroy()
                self.frames.remove(frame)
                graph_repository.graphs.pop(name, None)
                return

    def get_selected_graph(self):
        graph = self.load_graph
        self.load_graph = None
        return graph
        # for frame in self.frames:
        #     if frame[0].get() == 1:
        #         return frame[0].cget("text")


class LoadGraphWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self._configure_window()
        self._create_inputs()
        self.load_hook = None
        self.graphs = graph_repository.graphs

    def _configure_window(self):
        self.title("Load Graph")
        self.minsize(LOAD_GRAPH_WINDOW_WIDTH, LOAD_GRAPH_WINDOW_HEIGHT)
        self.geometry(f"{LOAD_GRAPH_WINDOW_WIDTH}x{LOAD_GRAPH_WINDOW_WIDTH}")
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.grid_columnconfigure(0, weight=1)
        self._create_scrollable_frame()
        self.resizable(width=False, height=False)
        self.withdraw()

    def _create_scrollable_frame(self):
        self.scrollable_frame = GraphScrollableFrame(self, item_list=[], command=None)
        self.scrollable_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

    def _create_inputs(self):
        self.save_button = customtkinter.CTkButton(self, text='Load', command=self._on_load_graph)
        self.save_button.grid(row=1, column=0, padx=10)

    def _on_close(self):
        self.withdraw()

    def show_load_graph_window_visible(self, load_hook):
        self.scrollable_frame.frames = []
        self.load_hook = load_hook
        for key in graph_repository.graphs.keys():
            self.scrollable_frame.add_item(key)
        self.deiconify()

    def _on_load_graph(self):
        graph = self.scrollable_frame.get_selected_graph()
        if graph is not None:
            self.scrollable_frame.enable_checkbox()
            self.load_hook(graph)
            self._on_close()
