import customtkinter

from src.main.app.utils.constants import *
from src.main.app.utils.logger import setup_logger

logger = setup_logger("SaveGraphWindow")


class SaveGraphWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self._configure_window()
        self._create_inputs()
        self.name_entry.focus_set()
        self.graph = None

    def _configure_window(self):
        self.title("Save Graph")
        self.minsize(SAVE_GRAPH_WINDOW_WIDTH, SAVE_GRAPH_WINDOW_HEIGHT)
        self.geometry(f"{SAVE_GRAPH_WINDOW_WIDTH}x{SAVE_GRAPH_WINDOW_HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.resizable(width=False, height=False)
        self.withdraw()

    def _create_inputs(self):
        self.label = customtkinter.CTkLabel(self, text="Save Name:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label.grid(row=0, column=0, padx=(10, 2), pady=(20, 10))

        self.name_entry = customtkinter.CTkEntry(self, placeholder_text="", width=175)
        self.name_entry.grid(row=0, column=1, columnspan=2, padx=(0, 10), pady=(20, 10))

        self.save_button = customtkinter.CTkButton(self, text='Save', command=self._on_save_graph)
        self.save_button.grid(row=1, column=0, padx=10)

    def _on_close(self):
        self.withdraw()

    def show_save_graph_window_visible(self):
        self.deiconify()

    def _on_save_graph(self):
        logger.debug('saving graph...name=' + self.name_entry.get())
