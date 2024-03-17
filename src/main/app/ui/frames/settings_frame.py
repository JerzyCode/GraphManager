import customtkinter

from src.main.app.utils.constants import LEFT_FRAME_WIDTH, EDGE_WIDTH

global input_box_bg_color, input_box_fg_color


class SettingsFrame(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root, width=LEFT_FRAME_WIDTH)
        self.root = root
        self.config = root.config
        self.grid_rowconfigure(5, weight=1)
        self._create_params_frame()
        self.edge_width = EDGE_WIDTH
        # self.prepare_slider()

    def _create_params_frame(self):
        self.frame_label = customtkinter.CTkLabel(self, text='SETTINGS', font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frame_label.grid(row=0, column=0, pady=10, padx=20)

        self.label = customtkinter.CTkLabel(self, text="Edge Width", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label.grid(row=1, column=0, padx=(20, 5), pady=(10, 0))

        self.slider = customtkinter.CTkSlider(self, from_=1, to=3, number_of_steps=20)
        self.slider.configure(command=self._on_width_slider)
        self.slider.grid(row=2, column=0, padx=20, pady=5)

        self.grid_switch_var = customtkinter.BooleanVar()
        self.grid_switch_var.set(self.config.is_grid_enabled)
        self.grid_switch = customtkinter.CTkSwitch(self, text="Grid Switcher",
                                                   variable=self.grid_switch_var, onvalue=True, offvalue=False)
        self.grid_switch.grid(row=3, column=0, pady=10, padx=20)

        save_button = customtkinter.CTkButton(self, text="Save Settings", command=self._on_save_button)
        save_button.grid(row=6, column=0, padx=20, pady=(20, 10))

        close_button = customtkinter.CTkButton(self, text="Close", command=self.close_modal)
        close_button.grid(row=7, column=0, padx=20, pady=(10, 20))

    def close_modal(self):
        self.destroy()

    def _on_width_slider(self, value):
        self.edge_width = value

    def _on_save_button(self):
        self.config.change_grid_enabled(self.grid_switch_var.get())
        self.config.change_edge_width(self.edge_width)
        self.close_modal()
