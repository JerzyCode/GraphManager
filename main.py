from tkinter import *
from tkinter import ttk

from app.graph.Vertex import Vertex
from app.utils.const import WINDOW_WIDTH, WINDOW_HEIGHT, RADIUS

root = Tk()
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
canvas = Canvas(root)
canvas.pack(fill=BOTH, expand=True)


vertex1 = Vertex("A", canvas)
vertex2 = Vertex("B", canvas)
vertex3 = Vertex("C", canvas)
vertex4 = Vertex("D", canvas)
vertex5 = Vertex("E", canvas)
vertex6 = Vertex("F", canvas)
vertex1.add_edge(vertex2)
vertex6.add_edge(vertex2)



# create_vertex(canvas, vertex)

root.mainloop()
