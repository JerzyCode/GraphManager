from tkinter import *

from app.graph.Graph import generate_graph, depth_search
from app.graph.graphics.Drawer import Drawer
from app.utils.const import WINDOW_WIDTH, WINDOW_HEIGHT

root = Tk()
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
root.resizable(False, False)
root.title('Graph Manager')
canvas = Canvas(root)
canvas.pack(fill=BOTH, expand=True)

graph = generate_graph(7, canvas)
drawer = Drawer(graph, canvas)

label = Label(root, text="", font=("Courier 22 bold"))
label.pack()

entry = Entry(root, width=40)
entry.focus_set()
entry.pack()


def generate_and_draw_graph():
    global graph, drawer
    canvas.delete('all')
    graph_size = int(entry.get())  # Pobierz rozmiar grafu z pola tekstowego
    graph = generate_graph(graph_size, canvas)
    drawer = Drawer(graph, canvas)


def run_dfs():
    global graph, drawer
    depth_search(graph, drawer)
    root.after(1000, drawer.refresh_all())


generate_button = Button(root, text="Generate Graph", command=generate_and_draw_graph)
generate_button.pack()

dfs_button = Button(root, text="DFS", command=run_dfs)
dfs_button.pack()

root.mainloop()
