import tkinter

import customtkinter

from src.main.app.utils.constants import DIGRAPH, DIRECTED, WEIGHTED


class ParamsCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, window):
        super().__init__(window)

        self.directed_var = tkinter.IntVar()

        self.window = window
        self.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="n")

        self.checkbox_1 = customtkinter.CTkCheckBox(master=self, text=DIRECTED
                                                    , variable=self.directed_var, command=self._on_switch_directed)
        self.checkbox_1.grid(row=0, column=0, pady=10, padx=(10, 5), sticky="n")

        self.checkbox_2 = customtkinter.CTkCheckBox(master=self, text=DIGRAPH, command=self._on_switch_digraph)
        self.checkbox_2.grid(row=0, column=1, pady=10, padx=5, sticky="n", )

        self.checkbox_3 = customtkinter.CTkCheckBox(master=self, text=WEIGHTED, command=self._on_switch_weighted)
        self.checkbox_3.grid(row=0, column=2, pady=10, padx=(5, 10), sticky="n")

    def _on_switch_directed(self):
        self.window.is_directed = not self.window.is_directed

    def _on_switch_digraph(self):
        self.window.is_digraph = not self.window.is_digraph
        if self.window.is_digraph:
            self.window.is_directed = True
            self.directed_var.set(1)
            self.checkbox_1.configure(state='disabled')
        else:
            self.window.is_directed = False
            self.directed_var.set(0)
            self.checkbox_1.configure(state='normal')

    def _on_switch_weighted(self):
        self.window.is_weighted = not self.window.is_weighted
