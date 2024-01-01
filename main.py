import tkinter as tk
from app.graph.Graph import generate_graph, depth_search, binary_search, Graph
from app.graph.graphics.Drawer import Drawer
from app.utils.const import *


def generate_and_draw_graph():
    global graph, drawer
    size = input_size.get()
    p = input_p.get()
    if len(p) == 0:
        p = 0.5
    if size and size.isdigit() and int(size) <= 100:
        canvas.delete('all')
        graph_size = int(input_size.get())
        graph = generate_graph(graph_size, canvas, float(p))
        drawer = Drawer(graph, canvas)


def run_dfs():
    global graph, drawer
    depth_search(graph, drawer)


def run_bfs():
    global graph, drawer
    try:
        if len(graph.V) > 0:
            binary_search(graph, drawer)
    except (NameError, AttributeError, TypeError):
        print('graph is not defined')
        pass


def refresh_graph():
    global drawer
    drawer.refresh_all()


# MAIN WINDOW
root = tk.Tk()
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
root.resizable(True, True)
root.title('Graph Manager')

# BUTTONS PANEL
buttons_panel = tk.Frame(root, bd=2, width=122, padx=5, pady=5, bg=BUTTONS_PANEL_BG_COLOR)
buttons_panel.pack(side=tk.LEFT, fill=tk.BOTH)

size_window = tk.PanedWindow(buttons_panel, orient=tk.HORIZONTAL)
size_label = tk.Label(size_window, text="size:", font=FONT, bg=BUTTONS_PANEL_SIZE_BG_COLOR, bd=0,
                      fg=BUTTONS_PANEL_SIZE_FG_COLOR)
input_size = tk.Entry(size_window, width=7, bg=BUTTONS_PANEL_BG_COLOR, fg=BUTTON_FG_COLOR, font=FONT)
input_size.focus_set()

probability_label = tk.Label(size_window, text="p:", font=FONT, bg=BUTTONS_PANEL_SIZE_BG_COLOR, bd=0,
                             fg=BUTTONS_PANEL_SIZE_FG_COLOR)
input_p = tk.Entry(size_window, width=8, bg=BUTTONS_PANEL_BG_COLOR, fg=BUTTON_FG_COLOR, font=FONT)
input_p.focus_set()
size_window.add(size_label)
size_window.add(input_size)
size_window.add(probability_label)
size_window.add(input_p)
size_window.pack()

pixelVirtual = tk.PhotoImage(width=1, height=1)
generate_button = tk.Button(buttons_panel, image=pixelVirtual, text="Generate Graph", command=generate_and_draw_graph,
                            width=BUTTONS_VIEW_WIDTH, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, font=FONT, bd=5,
                            compound="c")
generate_button.pack()
dfs_button = tk.Button(buttons_panel, image=pixelVirtual, text="DFS", command=run_dfs, font=FONT,
                       width=BUTTONS_VIEW_WIDTH, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, bd=5, compound="c")
dfs_button.pack()

bfs_button = tk.Button(buttons_panel, image=pixelVirtual, text="BFS", command=run_bfs, font=FONT,
                       width=BUTTONS_VIEW_WIDTH, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, bd=5, compound="c")
bfs_button.pack()

refresh_button = tk.Button(buttons_panel, image=pixelVirtual, text="Refresh Graph", command=refresh_graph, font=FONT,
                           width=BUTTONS_VIEW_WIDTH, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, bd=5, compound="c")
refresh_button.pack()

## GRAPH PANEL
graph_panel = tk.PanedWindow(orient='horizontal', bg='black', width=GRAPH_VIEW_WIDTH, height=GRAPH_VIEW_HEIGHT)
graph_panel.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(graph_panel, bg=GRAPH_BG_COLOR)
canvas.pack(fill=tk.BOTH, expand=True)

A = [
    [1, 1, 1, 1],
    [1, 1, 0, 0],
    [1, 0, 1, 1],
    [1, 0, 0, 1]
]

graph = Graph(A, canvas)
drawer = Drawer(graph, canvas)
root.mainloop()
