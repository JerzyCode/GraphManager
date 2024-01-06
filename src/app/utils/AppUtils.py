import tkinter as tk

from src.app.utils.const import *


def create_button(parent, image, text, command):
    button = tk.Button(parent, image=image, text=text, command=command, font=FONT,
                       width=BUTTONS_VIEW_WIDTH, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, bd=0.5, compound="c")
    button.pack()
    return button


def create_input(parent, text, input_width):
    label = tk.Label(parent, text=text, font=FONT, bg=BUTTONS_PANEL_SIZE_BG_COLOR, bd=0,
                     fg=BUTTONS_PANEL_SIZE_FG_COLOR)
    entry = tk.Entry(parent, width=input_width, bg=BUTTONS_PANEL_BG_COLOR, fg=BUTTON_FG_COLOR, font=FONT)
    parent.add(label)
    parent.add(entry)
    return entry
