import customtkinter

from src.main.app.utils.constants import LEFT_FRAME_WIDTH, MAX_RADIUS

global input_box_bg_color, input_box_fg_color


class SettingsFrame(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root, width=LEFT_FRAME_WIDTH)
        self.root = root
        self.config = root.config
        self.grid_rowconfigure(7, weight=1)
        self._create_params_frame()
        self.edge_width = self.config.edge_width
        self.vertex_radius = self.config.vertex_radius

    def _create_params_frame(self):
        self.frame_label = customtkinter.CTkLabel(self, text='SETTINGS', font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frame_label.grid(row=0, column=0, pady=10, padx=20)

        self.label = customtkinter.CTkLabel(self, text="Edge Width", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label.grid(row=1, column=0, padx=(20, 5), pady=(10, 0))

        self.edge_width_slider = customtkinter.CTkSlider(self, from_=1, to=3, number_of_steps=20)
        self.edge_width_slider.set(self.config.edge_width)
        self.edge_width_slider.configure(command=self._on_width_slider)
        self.edge_width_slider.grid(row=2, column=0, padx=20, pady=5)

        self.label = customtkinter.CTkLabel(self, text="Vertex Size", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label.grid(row=3, column=0, padx=(20, 5), pady=(10, 0))

        self.vertex_size_slider = customtkinter.CTkSlider(self, from_=10, to=MAX_RADIUS, number_of_steps=20)
        self.vertex_size_slider.configure(command=self._on_radius_slider)
        self.vertex_size_slider.set(self.config.vertex_radius)
        self.vertex_size_slider.grid(row=4, column=0, padx=20, pady=5)

        self.grid_switch_var = customtkinter.BooleanVar()
        self.grid_switch_var.set(self.config.is_grid_enabled)
        self.grid_switch = customtkinter.CTkSwitch(self, text="Grid Switcher",
                                                   variable=self.grid_switch_var, onvalue=True, offvalue=False)
        self.grid_switch.grid(row=5, column=0, pady=10, padx=(40, 20), sticky='w')

        self.label_switch_var = customtkinter.BooleanVar()
        self.label_switch_var.set(self.config.is_label_enabled)
        self.label_switch = customtkinter.CTkSwitch(self, text="Show Vertex Labels",
                                                    variable=self.label_switch_var, onvalue=True, offvalue=False)
        self.label_switch.grid(row=6, column=0, pady=10, padx=(40, 20), sticky='w')

        save_button = customtkinter.CTkButton(self, text="Save Settings", command=self._on_save_button)
        save_button.grid(row=8, column=0, padx=20, pady=(20, 10))

        close_button = customtkinter.CTkButton(self, text="Close", command=self.close_modal)
        close_button.grid(row=9, column=0, padx=20, pady=(10, 20))

    def close_modal(self):
        self.destroy()

    def _on_width_slider(self, value):
        self.edge_width = value

    def _on_radius_slider(self, value):
        self.vertex_radius = value

    def _on_save_button(self):
        self.config.change_grid_enabled(self.grid_switch_var.get())
        self.config.change_edge_width(self.edge_width)
        self.config.change_label_enabled(self.label_switch_var.get())
        self.config.change_vertex_radius(int(self.vertex_radius))
        self.config.refresh_vertexes()
        self.config.is_vertex_to_refresh = False
        self.close_modal()
