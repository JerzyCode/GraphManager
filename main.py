from tkinter import *
from tkinter import ttk

from app.graph.Vertex import Vertex
from app.utils.const import WINDOW_WIDTH, WINDOW_HEIGHT, RADIUS

root = Tk()
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
canvas = Canvas(root)
canvas.pack(fill=BOTH, expand=True)


vertex = Vertex("1", 50, 55, canvas)
vertex2 = Vertex("2", 12, 54, canvas)
vertex3 = Vertex("3", 124, 122, canvas)
vertex4 = Vertex("4", 452, 321, canvas)
vertex5 = Vertex("5", 244, 444, canvas)



vertex.add_edge(vertex2)
vertex.add_edge(vertex3)
vertex3.add_edge(vertex2)
vertex4.add_edge(vertex5)
vertex4.add_edge(vertex3)
vertex5.add_edge(vertex)

# create_vertex(canvas, vertex)

root.mainloop()
