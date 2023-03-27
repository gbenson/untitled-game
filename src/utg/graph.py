class Node:
    def __init__(self, xy):
        self.xy = xy

    def __eq__(self, other):
        return self.xy == other


class Graph:
    def __init__(self, nodes=()):
        self.nodes = []
        for node in nodes:
            self.add_node(node)

    def add_node(self, node):
        self.nodes.append(Node(node))
