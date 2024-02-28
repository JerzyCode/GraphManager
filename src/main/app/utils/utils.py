import tkinter as tk

from src.main.app.graph.edge import Edge
from src.main.app.graph.vertex import Vertex
from src.main.app.utils.constants import *


def create_button(parent, image, text, command):
    button = create_button_no_pack(parent, image, text, command)
    button.pack(pady=2)
    return button


def create_button_no_pack(parent, image, text, command):
    button = tk.Button(parent, image=image, text=text, command=command, font=FONT,
                       width=BUTTONS_VIEW_WIDTH, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, bd=0.5, compound="c")
    return button


def create_input(parent, text, input_width):
    label = tk.Label(parent, text=text, font=FONT, bg=BUTTONS_PANEL_SIZE_BG_COLOR, bd=0,
                     fg=BUTTONS_PANEL_SIZE_FG_COLOR, padx=2)
    entry = tk.Entry(parent, width=input_width, bg=BUTTONS_PANEL_BG_COLOR, fg=BUTTON_FG_COLOR, font=FONT)
    parent.add(label)
    parent.add(entry)
    return entry


def get_colored_vertexes(elements):
    result = []
    for element in elements:
        if isinstance(element, Vertex):
            result.append(element)
    return result


def get_colored_edges(elements):
    result = []
    for element in elements:
        if isinstance(element, Edge):
            result.append(element)
    return result
