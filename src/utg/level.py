from scipy.spatial import Delaunay

from .graph import Graph
from .point import Point


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

        d_mesh = Delaunay(self.d_vertices)
        self._add_v_vertices(d_mesh)
        self._add_paired_edges(d_mesh)

    def _add_v_vertices(self, d_mesh):
        """v_graph vertices are centroids of d_graph simplices."""
        for d_vertex_indices in d_mesh.simplices:
            self.v_graph.add_vertex(
                self._centroid_of([self.d_graph.vertices[dvi]
                                   for dvi in d_vertex_indices]))

    @classmethod
    def _centroid_of(cls, vertices):
        return Point((sum(v.x for v in vertices) // len(vertices),
                      sum(v.y for v in vertices) // len(vertices)))

    def _add_paired_edges(self, d_mesh):
        # ds1 = d_graph simplex 1
        for ds1_index, ds1_neighbor_indices in enumerate(d_mesh.neighbors):
            ds1_vertex_indices = d_mesh.simplices[ds1_index]
            for ds2_index, d_edge_vertex_indices in zip(
                    ds1_neighbor_indices,
                    ((ds1_vertex_indices[1], ds1_vertex_indices[2]),
                     (ds1_vertex_indices[0], ds1_vertex_indices[2]),
                     (ds1_vertex_indices[0], ds1_vertex_indices[1]))):
                if self.d_graph.has_edge(d_edge_vertex_indices):
                    continue
                d_edge = self.d_graph.add_edge(d_edge_vertex_indices)
                if ds2_index < 0:
                    continue
                v_edge = self.v_graph.add_edge((ds1_index, ds2_index))
                d_edge.v_edge = v_edge
                v_edge.d_edge = d_edge

    @property
    def d_vertices(self):
        return self.d_graph.vertices

    @property
    def v_vertices(self):
        return self.v_graph.vertices


# Hey, how the search is conducted is down to us!
# we can prioritize tree or river mazes,
# and maybe prefer horizonatal runs over vertical?
