from src.main.app.app import App
from src.main.app.graph.vertex import Vertex

if __name__ == "__main__":
    app = App()
    app.mainloop()

#
# W = set()
# A = set()
# B = set()
# vertex1 = Vertex('1', 12, 12)
# vertex2 = Vertex('2', 12, 12)
# A.add(vertex1)
# B.add(vertex2)
# W.add(frozenset(A))
# W.add(frozenset(B))
#
# are_in_different_sets(vertex1, vertex2, W)
