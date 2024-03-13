import customtkinter

import src.main.app.data.database as db
from src.main.app.utils.logger import setup_logger

logger = setup_logger("LoadSaveGraphFrame")


class GraphScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command
        self.frames = []
        self.save_name = None

    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, text=item, width=175, command=self._on_check_box)
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


class SaveLoadGraphFrame(customtkinter.CTkFrame):
    def __init__(self, master, mode):
        super().__init__(master)
        self.entry = None
        self.add_entry_button = None
        self.load_hook = master.load_graph_hook
        self._configure_window()
        self.action_button = customtkinter.CTkButton(self)
        self._create_frame(mode)
        self.graph = master.graph

    def _create_frame(self, mode):
        if mode == 'save':
            self.save_graph_frame()
        else:
            self.load_graph_frame()

    def _configure_window(self):
        self._create_scrollable_frame()
        self.grid_rowconfigure(0, weight=1)

    def _create_scrollable_frame(self):
        self.scrollable_frame = GraphScrollableFrame(self, command=None)
        self.scrollable_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def _create_inputs(self):
        self.action_button = customtkinter.CTkButton(self)

    def close_modal(self):
        self.destroy()

    def save_graph_frame(self):
        self.scrollable_frame.reload_graphs()
        self.entry = customtkinter.CTkEntry(self, placeholder_text='Save name')
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky='esw')
        self.action_button.configure(text='Save', command=self._on_save_graph)
        self.action_button.grid(row=2, column=0, padx=20, sticky='esw')
        close_button = customtkinter.CTkButton(self, text="Close", command=self.close_modal)
        close_button.grid(row=3, column=0, padx=20, pady=(20, 20), sticky='s')

    def load_graph_frame(self):
        self.scrollable_frame.reload_graphs()
        self.action_button.configure(text='Load', command=self._on_load_graph)
        self.action_button.grid(row=1, column=0, padx=20, sticky='esw')
        close_button = customtkinter.CTkButton(self, text="Close", command=self.close_modal)
        close_button.grid(row=2, column=0, padx=20, pady=(20, 20), sticky='s')

    def _on_load_graph(self):
        graph = self.scrollable_frame.get_selected_graph()
        logger.debug('loading graph')
        if graph is not None:
            self.scrollable_frame.enable_checkbox()
            self.load_hook(graph)

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
