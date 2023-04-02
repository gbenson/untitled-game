from .point import Point

# A graph is a pair G = (V, E), where V is a set whose elements
# are called vertices (singular: vertex), and E is a set of paired
# vertices, whose elements are called edges.  The vertices a and b
# of an edge {a, b} are called the endpoints of the edge. The edge
# is said to join a and b and to be incident on a and b.
#
# https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Definitions

class Graph:
    def __init__(self, vertices=()):
        self.vertices = list(map(Point, vertices))
        self._edges = {}

    @property
    def edges(self):
        return self._edges.values()

    def add_vertex(self, xy):
        self.vertices.append(Point(xy))

    def _edge_key(self, vertex_indices):
        return tuple(sorted(vertex_indices))

    def has_edge(self, *args, **kwargs):
        edge_key = self._edge_key(*args, *kwargs)
        return edge_key in self._edges

    def add_edge(self, *args, **kwargs):
        edge_key = self._edge_key(*args, *kwargs)
        assert edge_key not in self._edges
        edge = Edge([self.vertices[vi] for vi in edge_key])
        self._edges[edge_key] = edge
        return edge


class Edge:
    def __init__(self, vertices):
        vertices = tuple(vertices)
        if len(vertices) != 2:
            raise ValueError(vertices)
        self.vertices = vertices
        self.visited = False

    @property
    def start(self):
        return self.vertices[0]

    @property
    def end(self):
        return self.vertices[1]
