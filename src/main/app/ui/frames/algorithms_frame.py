import customtkinter

import src.main.app.graph.algorithms.algorithms as algorithm
from src.main.app.utils.constants import *
from src.main.app.utils.logger import setup_logger

logger = setup_logger("AlgorithmsFrame")


class AlgorithmsFrame(customtkinter.CTkFrame):
    def __init__(self, master, graph):
        super().__init__(master, width=LEFT_FRAME_WIDTH)
        self.drawer = master.drawer
        self.grid_rowconfigure(5, weight=1)
        self._create_buttons()
        self.graph = graph

    def _create_buttons(self):
        label = customtkinter.CTkLabel(self, text=ALGORITHMS, font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, padx=20, pady=(20, 10))

        bfs_button = customtkinter.CTkButton(self, text=BFS, command=self._on_run_bfs_btn)
        bfs_button.grid(row=1, column=0, padx=20, pady=10)

        dfs_button = customtkinter.CTkButton(self, text=DFS, command=self._on_run_dfs_btn)
        dfs_button.grid(row=2, column=0, padx=20, pady=10)

        kruskal_button = customtkinter.CTkButton(self, text=KRUSKAL_ALGORITHM, command=self._on_kruskal_algorithm_btn)
        kruskal_button.grid(row=3, column=0, padx=20, pady=10)

        dijkstra_button = customtkinter.CTkButton(self, text=DIJKSTRA_ALGORITHM, command=self._on_dijkstra_algorithm_btn)
        dijkstra_button.grid(row=4, column=0, padx=20, pady=10)

        close_button = customtkinter.CTkButton(self, text="Close", command=self.close_modal)
        close_button.grid(row=6, column=0, padx=20, pady=(10, 20))

    def _on_run_dfs_btn(self):
        logger.debug("Running DFS")
        self._run_search(algorithm.depth_search)

    def _on_run_bfs_btn(self):
        logger.debug("Running BFS")
        self._run_search(algorithm.binary_search)

    def _on_kruskal_algorithm_btn(self):
        if self.graph is None:
            return
        else:
            logger.debug("Running Kruskal")
            algorithm.kruskal_algorithm(self.graph, self.drawer)

    def _on_dijkstra_algorithm_btn(self):
        if self.graph is None:
            return
        else:
            logger.debug("Running Dijkstra")
            algorithm.run_dijkstra_algorithm(self.graph, self.graph.V[0], self.drawer)

    def _run_search(self, search):
        if self.graph is None:
            return
        else:
            search(self.graph, self.drawer)

    def close_modal(self):
        self.destroy()
