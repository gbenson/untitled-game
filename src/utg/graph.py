from .triangle import circumcentre

class Node:
    def __init__(self, xy, name=None):
        self.xy = xy
        self.name = name

    def __str__(self):
        result = str(tuple(self.xy))
        if self.name is not None:
            result = f"{self.name} {result}"
        return result

    @property
    def x(self):
        return self.xy[0]

    @property
    def y(self):
        return self.xy[1]

    def __eq__(self, other):
        return self.xy == other

    def __sub__(self, other):
        return Node((self.x - other.x,
                     self.y - other.y))

    def distance2_from(self, other):
        dx, dy = (self - other).xy
        return dx * dx + dy * dy


def nodes_by_distance_from(nodes, point):
    nodes = ((node.distance2_from(point), node) for node in nodes)
    return [node for _, node in sorted(nodes)]


class Polygon:
    def __init__(self, nodes):
        self.nodes = nodes

    def __str__(self):
        return repr(tuple(node.name or node.xy for node in self.nodes))


class Triangle(Polygon):
    pass


# https://en.wikipedia.org/wiki/Cross_product#Computational_geometry
def is_right_handed_system(a, b, c):
    v = b - a
    w = c - a
    P = v.x * w.y - v.y * w.x
    return P > 0


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

    def triangulate(self, stop_after=None):
        """Triangulate the nodes using the the S-hull algorithm.
        """
        # Select a seed point x0 from the set of unique points xi
        x0 = self.centremost_node

        # Sort the remaining points according to |xi - x0|**2
        nodes = nodes_by_distance_from(
            (node for node in self.nodes if node is not x0),
            x0)

        #  Find the point xj closest to x0
        xj = nodes.pop(0)

        # Find the point xk that creates the smallest circumcircle
        # with x0 and xj and record the center of the circumcircle
        # as C
        tmp = ((node, circumcentre(x0, xj, node)) for node in nodes)
        tmp = [(node.distance2_from(cc), node, cc) for node, cc in tmp]
        _, xk, C = min(tmp)
        nodes.remove(xk)

        # Order points [x0, xj, xk] to give a right handed system.
        # This is the initial seed convex hull
        if not is_right_handed_system(x0, xj, xk):
            xj, xk = xk, xj
        x0.name, xj.name, xk.name = "x0", "xj", "xk"
        self.hull = Polygon([x0, xj, xk])
        self.mesh = [Triangle(self.hull.nodes.copy())]

        # Re-sort the remaining points according to |xi - C|**2
        nodes = nodes_by_distance_from(nodes, C)
        for i, node in enumerate(nodes):
            node.name = f"s{i}"

        # Sequentially add the points si to the propagating convex
        # hull.  As each new point is added, the facets of the hull
        # that are visible to it form new triangles.
        for si in nodes:
            for ip, (hj, hk) in enumerate(zip(self.hull.nodes,
                                              self.hull.nodes[1:]
                                              + self.hull.nodes[:1]),
                                          start=1):
                newtri = Triangle((hj, si, hk))
                if not is_right_handed_system(*newtri.nodes):
                    continue  # si not visible from hj-hk

                if stop_after is not None:
                    if stop_after < 1:
                        return
                    stop_after -= 1

                self.hull.nodes.insert(ip, si)
                self.mesh.append(newtri)

                # where we need to act is:
                # s3 x0 xk needs adding
                # which gobbles xk;
                # s3=xk-x0 was the old perimiter,
                # s3-x0 becomes the new perimiter
                # because a line from xk to s3-x0 points out of the hull
                # (the hull became concave at xk when we added s3)

                # ugh, last triangle was ('xj', 's3', 'xk')
                # final hull = ('x0', 's0', 's2', 's1', 'xj', 's3', 'xk')
                # so we need to rotate the hull here
                # (could just always rotate it one)

                # Rotate the hull's nodes by two steps, to handle cases
                # where the insertion point was right at the end.
                self.hull.nodes.extend(self.hull.nodes[:2])
                newtri = Triangle(self.hull.nodes[ip:ip + 3])
                self.hull.nodes = self.hull.nodes[2:]
                ip = None  # XXX 0 ?

                # s3 xk x0 is the section of the hull we're papering over
                #
                if True:  # XXX hull is concave
                    break

                if stop_after is not None:
                    if stop_after < 1:
                        return
                    stop_after -= 1

                # This point got gobbled up!
                self.hull.nodes.pop(ip + 1)
                self.mesh.append(newtri)

        #  8. A non-overlapping triangulation of the set of points has
        #     now been created.  Adjacent pairs of triangles of this
        #     triangulation must be ’flipped’ to create a Delaunay
        #     triangulation.
