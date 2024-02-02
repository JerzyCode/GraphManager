import customtkinter

import src.main.app.utils.algorithms as algorithm
from src.main.app.utils.constants import *


class AlgorithmsWindow(customtkinter.CTk):
    def __init__(self, drawer):
        super().__init__()
        self.drawer = drawer
        self._configure_window()
        self._create_buttons()
        self.graph = None

    def _configure_window(self):
        self.title(ALGORITHMS)
        self.minsize(ALGORITHMS_WINDOW_WIDTH, ALGORITHMS_WINDOW_HEIGHT)
        self.geometry(f"{ALGORITHMS_WINDOW_WIDTH}x{ALGORITHMS_WINDOW_HEIGHT}+{WINDOW_WIDTH + 200}+0")
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.grid_columnconfigure(0, weight=1)

        self.withdraw()

    def _create_buttons(self):
        self.label = customtkinter.CTkLabel(self, text=ALGORITHMS, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.bfs_button = customtkinter.CTkButton(self, text=BFS, command=self._on_run_bfs_btn)
        self.bfs_button.grid(row=1, column=0, padx=20, pady=10)

        self.dfs_button = customtkinter.CTkButton(self, text=DFS, command=self._on_run_dfs_btn)
        self.dfs_button.grid(row=2, column=0, padx=20, pady=10)

        self.kruskal_button = customtkinter.CTkButton(self, text=KRUSKAL_ALGORITHM, command=self._on_kruskal_algorithm_btn)
        self.kruskal_button.grid(row=3, column=0, padx=20, pady=10)

    def _on_close(self):
        self.withdraw()

    def show_algorithms_window_visible(self):
        self.deiconify()

    def _on_run_dfs_btn(self):
        if self.graph is None:
            return
        else:
            algorithm.depth_search(self.graph, self.drawer)

    def _on_run_bfs_btn(self):
        if self.graph is None:
            return
        else:
            algorithm.binary_search(self.graph, self.drawer)

    def _on_kruskal_algorithm_btn(self):
        if self.graph is None:
            return
        else:
            algorithm.kruskal_algorithm(self.graph, self.drawer)
