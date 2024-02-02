import customtkinter

from src.main.app.utils.constants import DIGRAPH, DIRECTED, WEIGHTED


class ParamsCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.grid(row=0, column=0, rowspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.checkbox_1 = customtkinter.CTkCheckBox(master=self, text=DIRECTED, command=self._on_switch_directed)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")

        self.checkbox_2 = customtkinter.CTkCheckBox(master=self, text=DIGRAPH, command=self._on_switch_digraph)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n", )

        self.checkbox_3 = customtkinter.CTkCheckBox(master=self, text=WEIGHTED, command=self._on_switch_weighted)
        self.checkbox_3.grid(row=3, column=0, pady=(20, 20), padx=20, sticky="n")

    def _on_switch_directed(self):
        self.window.is_directed = not self.window.is_directed

    def _on_switch_digraph(self):
        self.window.is_digraph = not self.window.is_digraph



    def _on_switch_weighted(self):
        self.window.is_weighted = not self.window.is_weighted
