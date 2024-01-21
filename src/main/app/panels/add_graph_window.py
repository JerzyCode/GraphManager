import customtkinter

from src.main.app.utils.constants import *


class AddGraphWindow(customtkinter.CTk):
    def __init__(self, set_params_add_graph):
        super().__init__()
        self.is_directed = False
        self.is_digraph = False
        self.is_weighted = False
        self.is_custom = False
        self.on_set_params_btn = set_params_add_graph

        self._configure_window()
        self._create_checkbox_frame()
        self._create_params_frame()

    def _configure_window(self):
        self.title("Add Graph")
        self.geometry(f"{ADD_GRAPH_WINDOW_WIDTH}x{ADD_GRAPH_WINDOW_HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.resizable(False, False)
        self.withdraw()

    def _create_checkbox_frame(self):
        self.checkbox_frame = customtkinter.CTkFrame(self)
        self.checkbox_frame.grid(row=0, column=0, rowspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_frame, text='Directed', command=self._on_switch_directed)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")

        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_frame, text='Digraph', command=self._on_switch_digraph)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n", )

        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_frame, text='Weighted', command=self._on_switch_weighted)
        self.checkbox_3.grid(row=3, column=0, pady=(20, 20), padx=20, sticky="n")

    def _create_params_frame(self):
        self.info_frame = customtkinter.CTkFrame(self)
        self.info_frame.grid(row=0, column=1, rowspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.add_vertex_info = customtkinter.CTkLabel(master=self.info_frame, text='To add vertex, press shift + left mouse button')
        self.add_vertex_info.grid(row=0, column=0, padx=(40, 20), pady=(20, 20))
        self.add_edge_info = customtkinter.CTkLabel(master=self.info_frame, text='To add edge, press alt + left mouse button')
        self.add_edge_info.grid(row=1, column=0, padx=(40, 20), pady=(0, 20), sticky='n')
        self.set_params_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text='Set params',
                                                         text_color=("gray10", "#DCE4EE"), command=self._on_set_params_btn)
        self.set_params_button.grid(row=4, column=0, rowspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def _on_switch_directed(self):
        self.is_directed = not self.is_directed

    def _on_switch_digraph(self):
        self.is_digraph = not self.is_digraph

    def _on_switch_weighted(self):
        self.is_weighted = not self.is_weighted

    def _on_set_params_btn(self):
        print('set params')
        self.on_set_params_btn(self.is_directed, self.is_digraph, self.is_weighted)
        self.set_params_button.configure(state='disabled')

    def _on_close(self):
        self.withdraw()

    def set_params_button_state_normal(self):
        self.set_params_button.configure(state='normal')

    def show_add_graph_panel(self):
        self.deiconify()
