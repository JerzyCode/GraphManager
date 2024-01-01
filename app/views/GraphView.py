import tkinter
from turtle import ScrolledCanvas


class GraphView(tkinter.Frame):
    def __init__(self, canvas, master=None):
        super().__init__(master)
        self.master = master
        self.canvas = canvas
        self.pack()
