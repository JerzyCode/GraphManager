import tkinter

import customtkinter

from src.main.app.utils.constants import *
from src.main.app.utils.logger import setup_logger

logger = setup_logger("SetWeightWindow")

global input_box_bg_color, input_box_fg_color


def change_set_weight_window_appearance_mode(new_appearance_mode: str):
    global input_box_bg_color, input_box_fg_color
    if new_appearance_mode == "Light":
        input_box_bg_color = GRAPH_BG_COLOR_LIGHT
        input_box_fg_color = GRAPH_BG_COLOR_DARK
    elif new_appearance_mode == "Dark":
        input_box_bg_color = GRAPH_BG_COLOR_DARK
        input_box_fg_color = GRAPH_BG_COLOR_LIGHT


change_set_weight_window_appearance_mode("Dark")


class AskWeightDialog(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.transient(parent)
        self.title('Add Weight')
        self.weight = None
        self._configure_window()
        self._create_fields()
        self.weight_entry.focus_set()
        self.wait_window(self)

    def _configure_window(self):
        self.minsize(ADD_WEIGHT_WIDTH, ADD_WEIGHT_HEIGHT)
        self.geometry(f"{ADD_WEIGHT_WIDTH}x{ADD_WEIGHT_HEIGHT}+{ADD_WEIGHT_WIDTH + 50}+0")
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.configure(bg=input_box_bg_color)
        self.grid_columnconfigure(0, weight=1)

    def _create_fields(self):
        self.weight_label = customtkinter.CTkLabel(self, text='Weight:', font=customtkinter.CTkFont(size=20, weight="bold"))
        self.weight_label.grid(row=0, column=0, padx=(5, 5), pady=(5, 0), sticky="nsew")
        self.weight_entry = customtkinter.CTkEntry(self, placeholder_text="0", width=100, bg_color=input_box_fg_color)
        self.weight_entry.insert(0, '0')
        self.weight_entry.grid(row=0, column=1, padx=(0, 20), pady=(5, 0))
        self.weight_entry.bind("<Return>", self.validate)
        self.submit_button = customtkinter.CTkButton(self, text='Submit', command=self.validate)
        self.submit_button.grid(row=1, column=0, columnspan=3, padx=5, pady=10)

    def validate(self, event=None):
        try:
            self.weight = int(self.weight_entry.get())
            self.destroy()
        except ValueError:
            pass

    def _on_close(self):
        self.withdraw()
