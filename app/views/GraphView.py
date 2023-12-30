import tkinter
from turtle import ScrolledCanvas


class GraphView:
    def __init__(self, canvas, root):
        self.turtle = ScrolledCanvas(root)
        self.canvas = canvas
        self.back_button = tkinter.Button(text='Back', command=self.back_to_menu)

    def set_graph_view_visible(self):
        self.turtle.pack_forget()
        self.back_button.pack(side=tkinter.BOTTOM, pady=10)

    def back_to_menu(self):
        self.turtle.pack_forget()
        self.canvas.pack_forget()
        self.back_button.pack_forget()
