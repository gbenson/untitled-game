class Node:
    def __init__(self, xy):
        self.xy = xy

    def __str__(self):
        return str(self.xy)

    @property
    def x(self):
        return self.xy[0]

    @property
    def y(self):
        return self.xy[1]

    def __eq__(self, other):
        return self.xy == other

    def distance2_from(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy


def nodes_by_distance_from(nodes, point):
    nodes = ((node.distance2_from(point), node) for node in nodes)
    return [node for _, node in sorted(nodes)]


class Graph:
    def __init__(self, nodes=()):
        self.nodes = []
        for node in nodes:
            self.add_node(node)

    def add_node(self, node):
        self.nodes.append(Node(node))

    @property
    def centre(self):
        min_x = min(node.x for node in self.nodes)
        max_x = max(node.x for node in self.nodes)
        min_y = min(node.y for node in self.nodes)
        max_y = max(node.y for node in self.nodes)
        return Node(((min_x + max_x) // 2, (min_y + max_y) // 2))

    @property
    def centremost_node(self):
        return nodes_by_distance_from(self.nodes, self.centre)[0]

    def triangulate(self):
        """Triangulate the nodes using the the S-hull algorithm.
        """
        # Select a seed point x0 from the set of unique points xi
        x0 = self.centremost_node

        # Sort the remaining points according to |xi − x0|**2
        nodes = nodes_by_distance_from(
            (node for node in self.nodes if node is not x0),
            x0)

        #  Find the point xj closest to x0
        xj = nodes.pop(0)


        #  4. Find the point xk that creates the smallest circumcircle
        #     with x0 and xj and record the center of the circumcircle
        #     as C.
        #  5. Order points [x0, xj, xk] to give a right handed system.
        #     This is the initial seed convex hull.
        #  6. Re-sort the remaining points according to |xi − C|**2
        #     to give points si.
        #  7. Sequentially add the points si to the propagating convex
        #     hull.  As each new point is added, the facets of the hull
        #     that are visible to it form new triangles.
        #  8. A non-overlapping triangulation of the set of points has
        #     now been created.  Adjacent pairs of triangles of this
        #     triangulation must be ’flipped’ to create a Delaunay
        #     triangulation.
