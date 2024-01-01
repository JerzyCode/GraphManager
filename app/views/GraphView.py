from tkinter import Frame, Canvas


class GraphView(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.canvas = Canvas(master)
        self.pack()
