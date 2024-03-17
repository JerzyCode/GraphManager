class Config:
    def __init__(self, app):
        self.app = app
        self.is_grid_enabled = True
        self.edge_width = 1.35
        self.edge_width_wider = self.edge_width * 1.85

    def change_grid_enabled(self, is_grid_enabled):
        self.is_grid_enabled = is_grid_enabled
        if self.is_grid_enabled:
            self.app.after(50, lambda: self.app.drawer.draw_grid(self.app.canvas.winfo_width(), self.app.canvas.winfo_height()))
        else:
            self.app.drawer.erase_grid()

    def change_window_size(self, event):
        if event.width != self.app.winfo_width() or event.height != self.app.winfo_height():
            self.app.drawer.erase_grid()
            if self.is_grid_enabled:
                self.app.after(50, lambda: self.app.drawer.draw_grid(self.app.canvas.winfo_width(), self.app.canvas.winfo_height()))

    def change_edge_width(self, new_width):
        if new_width == self.edge_width:
            return
        self.edge_width = new_width
        self.edge_width_wider = self.edge_width + 0.85 * self.edge_width
        self.app.drawer.refresh_all(self.app.graph)
