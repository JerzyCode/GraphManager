import customtkinter

from src.main.app.ui.utils.slider_frame import SliderFrame
from src.main.app.utils.constants import LEFT_FRAME_WIDTH

global input_box_bg_color, input_box_fg_color


class SettingsFrame(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root, width=LEFT_FRAME_WIDTH)
        self.root = root
        self.config = root.config
        self.canvas = root.canvas
        self.drawer = root.drawer
        self.grid_rowconfigure(5, weight=1)
        self._create_params_frame()
        self.prepare_slider()

    def prepare_slider(self):
        self.edge_width_frame.set_value_step(5)
        self.edge_width_frame.hide_entry()

    def _create_params_frame(self):
        self.frame_label = customtkinter.CTkLabel(self, text='SETTINGS', font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frame_label.grid(row=0, column=0, pady=10, padx=20)

        self.edge_width_frame = SliderFrame(self, "Edge Width")
        self.edge_width_frame.grid(row=2, column=0, pady=10, padx=20, sticky='nsew')
        self.edge_width_frame.slider.set(50)
        self.edge_width_frame.insert_value('50')

        self.grid_switch_var = customtkinter.BooleanVar()
        self.grid_switch_var.set(self.config.is_grid_enabled)
        self.grid_switch = customtkinter.CTkSwitch(self, text="Grid Switcher", command=self._on_grid_switch,
                                                   variable=self.grid_switch_var, onvalue=True, offvalue=False)
        self.grid_switch.grid(row=3, column=0, pady=10, padx=20)

        close_button = customtkinter.CTkButton(self, text="Close", command=self.close_modal)
        close_button.grid(row=7, column=0, padx=20, pady=(10, 20))

    def close_modal(self):
        self.destroy()

    def _on_grid_switch(self):
        self.config.change_grid_enabled()
