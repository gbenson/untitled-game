class Node:
    def __init__(self, xy):
        self.xy = xy

    @property
    def x(self):
        return self.xy[0]

    @property
    def y(self):
        return self.xy[1]

    def __eq__(self, other):
        return self.xy == other


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
