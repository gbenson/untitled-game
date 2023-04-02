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

class Maze:
    def __init__(self, wall_vertices=()):
        self.wall_graph = Graph(wall_vertices)
        self.path_graph = Graph()

        wall_mesh = Delaunay(self.wall_graph.vertices)
        self._add_path_vertices(wall_mesh)
        self._add_paired_edges(wall_mesh)

    def _add_path_vertices(self, wall_mesh):
        """path_graph vertices are centroids of d_graph simplices."""
        for wall_vertex_indices in wall_mesh.simplices:
            self.path_graph.add_vertex(
                self._centroid_of([self.wall_graph.vertices[dvi]
                                   for dvi in wall_vertex_indices]))

    @classmethod
    def _centroid_of(cls, vertices):
        return Point((sum(v.x for v in vertices) // len(vertices),
                      sum(v.y for v in vertices) // len(vertices)))

    def _add_paired_edges(self, wall_mesh):
        # ws1 = wall_graph simplex 1
        for ws1_index, ws1_neighbor_indices in enumerate(wall_mesh.neighbors):
            ws1_vertex_indices = wall_mesh.simplices[ws1_index]
            for ws2_index, wall_edge_vertex_indices in zip(
                    ws1_neighbor_indices,
                    ((ws1_vertex_indices[1], ws1_vertex_indices[2]),
                     (ws1_vertex_indices[0], ws1_vertex_indices[2]),
                     (ws1_vertex_indices[0], ws1_vertex_indices[1]))):
                if self.wall_graph.has_edge(wall_edge_vertex_indices):
                    continue
                wall_edge = self.wall_graph.add_edge(wall_edge_vertex_indices)
                if ws2_index < 0:
                    continue
                path_edge = self.path_graph.add_edge((ws1_index, ws2_index))
                wall_edge.path_edge = path_edge
                path_edge.wall_edge = wall_edge


# Hey, how the search is conducted is down to us!
# we can prioritize tree or river mazes,
# and maybe prefer horizonatal runs over vertical?
