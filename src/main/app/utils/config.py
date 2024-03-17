from src.main.app.utils.constants import RADIUS, EDGE_WIDTH


class Config:
    def __init__(self, app):
        self.app = app
        self.is_vertex_to_refresh = False
        self.is_edge_to_refresh = False
        self.is_grid_enabled = True
        self.is_label_enabled = True
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
