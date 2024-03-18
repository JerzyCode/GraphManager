import tkinter

import customtkinter

from src.main.app.utils.constants import ADD_WEIGHT_HEIGHT, ADD_WEIGHT_WIDTH
from src.main.app.utils.logger import setup_logger

logger = setup_logger("SetWeightWindow")


class AskWeightDialog(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.config = parent.config
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
        self.configure(bg=self.config.input_weight_bg_color)
        self.grid_columnconfigure(0, weight=1)

    def _create_fields(self):
        color = self.config.input_weight_fg_color
        self.weight_label = customtkinter.CTkLabel(self, text='Weight:', font=customtkinter.CTkFont(size=20, weight="bold"))
        self.weight_label.grid(row=0, column=0, padx=(5, 5), pady=(5, 0), sticky="nsew")
        self.weight_entry = customtkinter.CTkEntry(self, placeholder_text="0", width=100, bg_color=color)
        self.weight_entry.insert(0, '0')
        self.weight_entry.grid(row=0, column=1, padx=(0, 20), pady=(5, 0))
        self.weight_entry.bind("<Return>", self.validate)
        self.submit_button = customtkinter.CTkButton(self, text='Submit', command=self.validate)
        self.submit_button.grid(row=1, column=0, columnspan=3, padx=5, pady=10)

    def validate(self):
        try:
            self.weight = int(self.weight_entry.get())
            self.destroy()
        except ValueError:
            pass

    def _on_close(self):
        self.withdraw()
