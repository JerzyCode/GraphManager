import tkinter as tk
from app.graph.Graph import generate_graph, depth_search
from app.graph.graphics.Drawer import Drawer
from app.utils.const import *


def generate_and_draw_graph():
    global graph, drawer
    size = entry.get()
    if size and size.isdigit() and int(size) < 100:
        canvas.delete('all')
        graph_size = int(entry.get())
        graph = generate_graph(graph_size, canvas)
        drawer = Drawer(graph, canvas)


def run_dfs():
    global graph, drawer
    depth_search(graph, drawer)
    root.after(1000, drawer.refresh_all())


# MAIN WINDOW
root = tk.Tk()
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
root.resizable(True, True)
root.title('Graph Manager')

# BUTTONS PANEL
buttons_panel = tk.Frame(root, bd=2, width=122, padx=5, pady=5, bg=BUTTONS_PANEL_BG_COLOR)
buttons_panel.pack(side=tk.LEFT, fill=tk.BOTH)

size_window = tk.PanedWindow(buttons_panel, orient=tk.HORIZONTAL)
label = tk.Label(size_window, text="size:", font="Courier 10 bold")
entry = tk.Entry(size_window, width=3)
entry.focus_set()
size_window.add(label)
size_window.add(entry)
size_window.pack()

pixelVirtual = tk.PhotoImage(width=1, height=1)
generate_button = tk.Button(buttons_panel, image=pixelVirtual, text="Generate Graph", command=generate_and_draw_graph,
                            width=BUTTONS_VIEW_WIDTH, bg=BUTTON_BG, fg=BUTTON_FG, bd=5, compound="c")
generate_button.pack()
dfs_button = tk.Button(buttons_panel, image=pixelVirtual, text="DFS", command=run_dfs,
                       width=BUTTONS_VIEW_WIDTH, bg=BUTTON_BG, fg=BUTTON_FG, bd=5, compound="c")
dfs_button.pack()

## GRAPH PANEL
graph_panel = tk.PanedWindow(orient='horizontal', bg='black', width=GRAPH_VIEW_WIDTH, height=GRAPH_VIEW_HEIGHT)
graph_panel.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(graph_panel, bg=GRAPH_BG_COLOR)
canvas.pack(fill=tk.BOTH, expand=True)

# print(canvas.winfo_width())

graph = generate_graph(7, canvas)
drawer = Drawer(graph, canvas)

root.mainloop()
