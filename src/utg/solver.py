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
        """Pick the edge that leads highest."""
        # that one should be called "bubbling up"
        unvisited_edges = [edge
                           for edge in self.vertex.edges
                           if not edge.visited]
        if not unvisited_edges:
            return
        edge_vertex_pairs = [(edge, [vertex
                                     for vertex in edge.vertices
                                     if vertex is not self.vertex][0])
                             for edge in unvisited_edges]
        _, _, edge, vertex = min(sorted(
            (vertex.y, vertex.x, edge, vertex)
            for edge, vertex in edge_vertex_pairs
            if not vertex.visited))
        edge.visited = True
        edge.wall_edge.visible = False
        vertex.visited = True
        self.vertex = vertex
        for edge in self.vertex.edges:
            if edge.visited:
                continue
            if all(vertex.visited for vertex in edge.vertices):
                edge.visible = False
