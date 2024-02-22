import random as rd

from src.main.app.graph.vertex import Vertex


def generate_test_vertex(label: str):
    max_width = rd.randint(150, 500)
    max_height = rd.randint(150, 500)
    return Vertex(label, max_width, max_height)
