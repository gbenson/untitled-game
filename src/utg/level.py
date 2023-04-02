from scipy.spatial import Delaunay

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

    def add_vertex(self, xy):
        self.vertices.append(Point(xy))


# First, the computer creates a random planar graph G shown in blue,
# and its dual F shown in yellow. Second, the computer traverses F
# using a chosen algorithm, such as a depth-first search, coloring the
# path red. During the traversal, whenever a red edge crosses over a
# blue edge, the blue edge is removed. Finally, when all vertices of
# F have been visited, F is erased and two edges from G, one for the
# entrance and one for the exit, are removed.
#
# https://en.wikipedia.org/wiki/Maze_generation_algorithm

class Level:
    def __init__(self, d_vertices=()):
        self.d_graph = Graph(d_vertices)
        self.v_graph = Graph()

        d = Delaunay(self.d_vertices)
        for vertex_indices in d.simplices:
            self.v_graph.add_vertex(
                self._centroid_of([self.d_graph.vertices[i]
                                   for i in vertex_indices]))

    @classmethod
    def _centroid_of(cls, vertices):
        return Point((sum(v.x for v in vertices) // len(vertices),
                      sum(v.y for v in vertices) // len(vertices)))

    @property
    def d_vertices(self):
        return self.d_graph.vertices

    @property
    def v_vertices(self):
        return self.v_graph.vertices


# Hey, how the search is conducted is down to us!
# we can prioritize tree or river mazes,
# and maybe prefer horizonatal runs over vertical?
