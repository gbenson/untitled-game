from abc import ABC, abstractmethod


class Solver(ABC):
    def __init__(self, maze):
        self.maze = maze
        self.init()

    @property
    def vertices(self):
        return self.maze.path_graph.vertices

    @property
    def edges(self):
        return self.maze.path_graph.edges

    def init(self):
        pass

    @property
    def start_vertex(self):
        """Default to starting at the top-left vertex."""
        return min((v.x * v.x + v.y * v.y, v.x, v)
                   for v in self.vertices)[-1]

    @abstractmethod
    def visit(self):
        pass

    def solve(self):
        try:
            while True:
                self.visit()
        except StopIteration:
            pass


class PrimSolver(Solver):
    """A solver that uses Prim's algorithm."""

    def init(self):
        for edge in self.edges:
            edge.weight = self.edge_weight_for(edge)
        self.start_vertex.visited = True

    @abstractmethod
    def edge_weight_for(self, edge):
        pass

    def visit(self):
        """Add the edge with the minimum weight."""
        edges = [(edge.weight, index, edge)
                 for index, edge in enumerate(self.edges)
                 if (not edge.visited
                     and (edge.start.visited
                          or edge.end.visited))]
        if not edges:
            raise StopIteration
        edge = min(edges)[-1]
        edge.visited = True
        edge.wall_edge.visible = False
        for vertex in edge.vertices:
            if vertex.visited:
                continue
            vertex.visited = True
            for edge in vertex.edges:
                if edge.visited:
                    continue
                if all(vertex.visited for vertex in edge.vertices):
                    edge.visited = True
                    edge.visible = False


class CaveSolver(PrimSolver):
    """A solver that makes mazes with horizontal passages."""

    def edge_weight_for(self, edge):
        p, q = edge.vertices
        dx = q.x - p.x
        dy = q.y - p.y
        return abs(dy) - abs(dx)
