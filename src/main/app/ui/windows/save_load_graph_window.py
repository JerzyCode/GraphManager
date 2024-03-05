import customtkinter

import src.main.app.data.database as db
from src.main.app.utils.constants import *
from src.main.app.utils.logger import setup_logger

logger = setup_logger("LoadSaveGraphWindow")


class GraphScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command
        self.frames = []
        self.load_graph = None
        self.save_name = None

    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, width=200, text=item, command=self._on_check_box)
        checkbox.grid(row=len(self.frames), column=0, pady=(0, 10), sticky='w')
        remove_button = customtkinter.CTkButton(self, text='X', width=5, command=lambda: self.remove_item(item))
        remove_button.grid(row=len(self.frames), column=1, pady=(0, 10), sticky='e')
        self.frames.append([checkbox, remove_button])

    def _on_check_box(self):
        selected = None
        for frame in self.frames:
            checkbox = frame[0]
            if checkbox.get() == 1:
                selected = checkbox
                self.save_name = checkbox.cget('text')
                break

        for frame in self.frames:
            checkbox = frame[0]
            if selected is not None:
                if checkbox != selected:
                    checkbox.configure(state='disabled')
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
                db.delete_save(name)
                return

    def reload_graphs(self):
        for frame in self.frames:
            if frame[0] is not None:
                frame[0].destroy()
            frame[1].destroy()
        self.frames.clear()
        self.save_name = None
        saves = db.get_all_saves()
        for save in saves:
            self.add_item(save)

    def get_selected_graph(self):
        return db.get_graph(self.save_name)


class SaveLoadGraphWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.entry = None
        self.add_entry_button = None
        self._configure_window()
        self._create_inputs()
        self.graph = None
        self.load_hook = None

    def _configure_window(self):
        self.minsize(LOAD_GRAPH_WINDOW_WIDTH, LOAD_GRAPH_WINDOW_HEIGHT)
        self.geometry(f"{LOAD_GRAPH_WINDOW_WIDTH}x{LOAD_GRAPH_WINDOW_WIDTH}")
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.grid_columnconfigure(0, weight=1)
        self._create_scrollable_frame()
        self.resizable(width=False, height=False)
        self.withdraw()

    def _create_scrollable_frame(self):
        self.scrollable_frame = GraphScrollableFrame(self, command=None)
        self.scrollable_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=2)

    def _create_inputs(self):
        self.action_button = customtkinter.CTkButton(self)

    def _on_close(self):
        self.withdraw()

    def show_save_load_graph_window_visible(self, mode, load_hook=None):
        self.scrollable_frame.reload_graphs()
        self.load_hook = load_hook
        if mode == 'save':
            self.configure(title='Save Graph')
            self.entry = customtkinter.CTkEntry(self, placeholder_text='Save name')
            self.action_button.configure(text='Save', command=self._on_save_graph)
            self.action_button.grid(row=1, column=0, padx=10, pady=20)
            self.entry.grid(row=1, column=1, padx=10)
        elif mode == 'load':
            self.configure(title='Load Graph')
            if self.entry is not None:
                self.entry.destroy()
            self.action_button.configure(text='Load', command=self._on_load_graph)
            self.action_button.grid(row=1, column=0, padx=10, pady=20)
        self.deiconify()

    def _on_load_graph(self):
        graph = self.scrollable_frame.get_selected_graph()
        logger.debug('loading graph')
        if graph is not None:
            self.scrollable_frame.enable_checkbox()
            self.load_hook(graph)
            self._on_close()

    def _on_save_graph(self):
        if self.graph is None:
            logger.debug('Can\'t save empty graph.')
        if self._is_valid_name():
            save_name = self.entry.get()
            if self.scrollable_frame.get_selected_graph() is not None:
                old_save_name = self.scrollable_frame.save_name
                db.update_graph(self.graph, old_save_name, save_name)
            else:
                db.save_graph(self.graph, save_name)
            self.scrollable_frame.reload_graphs()

    def _is_valid_name(self):
        name = self.entry.get()
        if len(name) < 3 or len(name) > 20 or db.check_if_exist(name):
            logger.debug('name is invalid, name=' + name)
            return False
        return True
