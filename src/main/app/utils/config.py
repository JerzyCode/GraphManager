import customtkinter

import src.main.app.utils.constants as const
from src.main.app.utils.constants import RADIUS, EDGE_WIDTH, GRAPH_BG_COLOR_DARK, VERTEX_BG_COLOR_DARK, VERTEX_FG_COLOR_DARK, \
    VERTEX_COLOR_CHANGE_BG_DARK, VERTEX_COLOR_CHANGE_FG_DARK, EDGE_COLOR_DARK, EDGE_COLOR_CHANGE_DARK, WEIGHT_COLOR_DARK, WEIGHT_COLOR_CHANGE_DARK, \
    INPUT_WEIGHT_BG_COLOR_DARK, INPUT_WEIGHT_BG_COLOR_LIGHT


class Config:
    def __init__(self, app):
        self.app = app
        self.is_vertex_to_refresh = False
        self.is_edge_to_refresh = False
        self.is_grid_enabled = True
        self.is_label_enabled = True
        self.graph_bg_color = GRAPH_BG_COLOR_DARK
        self.vertex_bg_color = VERTEX_BG_COLOR_DARK
        self.vertex_fg_color = VERTEX_FG_COLOR_DARK
        self.vertex_bg_color_changed = VERTEX_COLOR_CHANGE_BG_DARK
        self.vertex_fg_color_changed = VERTEX_COLOR_CHANGE_FG_DARK
        self.edge_color = EDGE_COLOR_DARK
        self.edge_color_changed = EDGE_COLOR_CHANGE_DARK
        self.input_weight_bg_color = INPUT_WEIGHT_BG_COLOR_DARK
        self.input_weight_fg_color = INPUT_WEIGHT_BG_COLOR_LIGHT
        self.weight_color = WEIGHT_COLOR_DARK
        self.weight_color_changed = WEIGHT_COLOR_CHANGE_DARK
        self.edge_width = EDGE_WIDTH
        self.edge_width_wider = self.edge_width * 1.85
        self.vertex_radius = RADIUS

    def change_grid_enabled(self, is_grid_enabled):
        if self.is_grid_enabled == is_grid_enabled:
            return
        self.is_grid_enabled = is_grid_enabled
        if self.is_grid_enabled:
            self.app.after(50, lambda: self.app.drawer.draw_grid(self.app.canvas.winfo_width(), self.app.canvas.winfo_height()))
        else:
            self.app.drawer.erase_grid()

    def change_label_enabled(self, is_label_enabled):
        if is_label_enabled == self.is_label_enabled:
            return
        self.is_label_enabled = is_label_enabled
        self.is_vertex_to_refresh = True

    def change_window_size(self, event):
        if event.width != self.app.winfo_width() or event.height != self.app.winfo_height():
            self.app.drawer.erase_grid()
            if self.is_grid_enabled:
                self.app.after(50, lambda: self.app.drawer.draw_grid(self.app.canvas.winfo_width(), self.app.canvas.winfo_height()))

    def change_vertex_radius(self, new_radius):
        if self.vertex_radius == new_radius:
            return
        self.vertex_radius = new_radius
        self.is_vertex_to_refresh = True
        self.is_edge_to_refresh = True

    def change_edge_width(self, new_width):
        if new_width == self.edge_width:
            return
        self.edge_width = new_width
        self.edge_width_wider = self.edge_width + 0.85 * self.edge_width
        self.app.drawer.refresh_all(self.app.graph)

    def refresh_vertexes(self):
        if self.app.graph is not None and self.is_vertex_to_refresh:
            if self.is_edge_to_refresh:
                self.app.drawer.refresh_all(self.app.graph)
            else:
                self.app.vertex_drawer.refresh_all_vertexes(self.app.graph.V)

    def change_appearance_mode(self, new_appearance_mode: str):
        if new_appearance_mode == "Light":
            customtkinter.set_appearance_mode("Light")
            self._set_all_colors("LIGHT")
        elif new_appearance_mode == "Dark":
            customtkinter.set_appearance_mode("Dark")
            self._set_all_colors("DARK")
        self.app.canvas.configure(bg=self.graph_bg_color)
        self.app.drawer.refresh_all(self.app.graph)

    def _close_set_weight(self):
        if self.app.canvas_handler is not None:
            self.app.canvas_handler.dialog.destroy()

    def _set_all_colors(self, mode):
        self.graph_bg_color = getattr(const, f"GRAPH_BG_COLOR_{mode}")
        self.vertex_bg_color = getattr(const, f"VERTEX_BG_COLOR_{mode}")
        self.vertex_fg_color = getattr(const, f"VERTEX_FG_COLOR_{mode}")
        self.vertex_bg_color_changed = getattr(const, f"VERTEX_COLOR_CHANGE_BG_{mode}")
        self.vertex_fg_color_changed = getattr(const, f"VERTEX_COLOR_CHANGE_FG_{mode}")
        self.edge_color = getattr(const, f"EDGE_COLOR_{mode}")
        self.edge_color_changed = getattr(const, f"EDGE_COLOR_CHANGE_{mode}")
        self.weight_color = getattr(const, f"WEIGHT_COLOR_{mode}")
        self.weight_color_changed = getattr(const, f"WEIGHT_COLOR_CHANGE_{mode}")
        mode_change = "DARK" if mode == "LIGHT" else "LIGHT"
        self.input_weight_bg_color = getattr(const, f"INPUT_WEIGHT_BG_COLOR_{mode}")
        self.input_weight_fg_color = getattr(const, f"INPUT_WEIGHT_BG_COLOR_{mode_change}")
