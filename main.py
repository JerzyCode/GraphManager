from tkinter import *

from app.graph.Graph import generate_graph
from app.graph.graphics.Drawer import Drawer
from app.utils.const import WINDOW_WIDTH, WINDOW_HEIGHT

root = Tk()
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
root.resizable(False, False)
canvas = Canvas(root)
canvas.pack(fill=BOTH, expand=True)


def generate_and_draw_graph():
    global entry
    canvas.delete('all')
    graph_size = int(entry.get())  # Pobierz rozmiar grafu z pola tekstowego
    graph = generate_graph(graph_size, canvas)
    Drawer(graph, canvas)


A = [[1, 0, 1, 1],
     [0, 1, 1, 1],
     [1, 1, 0, 1],
     [1, 1, 1, 0]]

graph = generate_graph(5, canvas)
drawer = Drawer(graph, canvas)

label = Label(root, text="", font=("Courier 22 bold"))
label.pack()

entry = Entry(root, width=40)
entry.focus_set()
entry.pack()


generate_button = Button(root, text="Generate Graph", command=generate_and_draw_graph)
generate_button.pack()

root.mainloop()
