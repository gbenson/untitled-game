class Solver:
    def __init__(self, maze):
        self.maze = maze
        self.vertex = self._start_vertex()
        self.vertex.visited = True

    @property
    def vertices(self):
        return self.maze.path_graph.vertices

    def _start_vertex(self):
        """The top-left vertex, Manhattan style."""
        return min((v.x + v.y, i, v)
                   for i, v in enumerate(self.vertices))[-1]

    def visit(self):
        pass
