import tkinter as tk
from tkinter import Tk

from app.utils.const import *
from app.views.GraphView import GraphView


class App:
    def __init__(self):
        self.createGraphButton = None
        self.root = Tk()
        self.canvas = tk.Canvas(self.root)
        self.graph_view = None
        self.graph_view = GraphView(self.root, self.canvas)
        self.frame = tk.Frame(self.root, padx=10, pady=10)

    def set_frame(self):
        self.root.wm_geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.configure(bg='black')
        

    def create_buttons(self):
        self.createGraphButton = tk.Button(
            self.root,
            text='Create Graph',
            command=self.show_graph_view,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT)
        self.createGraphButton.pack(pady=(self.root.winfo_reqheight() / 2))

    def show_graph_view(self):
        self.hide_buttons()
        self.graph_view.set_graph_view_visible()
        self.canvas.pack(expand=True, fill="both", )
        print('view create graph')

    def hide_graph_view(self):
        self.canvas.pack_forget()

        print("hide graph view")

    def hide_buttons(self):
        self.createGraphButton.pack_forget()

    def start(self):
        # self.set_canvas()
        self.create_buttons()
        self.set_frame()
        self.root.mainloop()
