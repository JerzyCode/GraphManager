import customtkinter

from src.main.app.ui.drawing.canvas_handler import CanvasHandler
from src.main.app.ui.utils.params_checkbox_frame import ParamsCheckboxFrame
from src.main.app.utils.constants import LEFT_FRAME_WIDTH
from src.main.app.utils.logger import setup_logger

logger = setup_logger("AddGraphFrame")


class AddGraphFrame(customtkinter.CTkFrame):
    def __init__(self, root, graph):
        super().__init__(master=root, width=LEFT_FRAME_WIDTH)
        self.graph = graph
        self.root = root
        self.is_directed = False
        self.is_digraph = False
        self.is_weighted = False
        self.is_custom = False
        self.grid_rowconfigure(6, weight=1)
        self.checkbox_frame = ParamsCheckboxFrame(self)
        self._create_params_frame()

    def _create_params_frame(self):
        info_frame = customtkinter.CTkFrame(self, width=LEFT_FRAME_WIDTH)
        info_frame.grid(row=0, column=0, rowspan=4, padx=20, pady=(20, 10), sticky="nsew")

        set_params_info = customtkinter.CTkLabel(master=info_frame, text='Set params and then do the following:')
        set_params_info.grid(row=1, column=0, padx=20, pady=(20, 5), sticky='w')

        add_vertex_info = customtkinter.CTkLabel(master=info_frame, text='\u2013 To add vertex, press shift + left mouse button', justify='left')
        add_vertex_info.grid(row=2, column=0, padx=20, pady=(5, 5), sticky='w')
        add_edge_info = customtkinter.CTkLabel(master=info_frame, text='\u2013 To add edge, press alt + left mouse button', justify='left')
        add_edge_info.grid(row=3, column=0, padx=20, pady=(5, 20), sticky='w')
        after_set_params_info = customtkinter.CTkLabel(master=info_frame, text='Set Params will clear your current graph!!',
                                                       justify='left', font=customtkinter.CTkFont(size=15, weight="bold"))
        after_set_params_info.grid(row=4, column=0, padx=20, pady=(5, 20), sticky='w')
        self.checkbox_frame.grid(row=5, column=0, padx=20, pady=20)

        self.set_params_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text='Set params',
                                                         text_color=("gray10", "#DCE4EE"), command=self._on_set_params_btn)
        self.set_params_button.grid(row=7, column=0, padx=20, pady=(20, 20))

        close_button = customtkinter.CTkButton(self, text="Close", command=self.close_modal)
        close_button.grid(row=8, column=0, padx=20, pady=(10, 20))

    def _on_set_params_btn(self):
        logger.debug("Setting params for graph")
        self.root.on_clear_graph()
        self.root.canvas_handler = CanvasHandler(self.root, self.is_directed, self.is_digraph, self.is_weighted)
        self.graph = self.root.canvas_handler.graph
        self.root.set_graph(self.graph)

    def close_modal(self):
        self.destroy()
