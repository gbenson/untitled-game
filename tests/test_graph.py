from utg.graph import Graph

# The dark blue nodes from
# https://commons.wikimedia.org/wiki/File:Graph_based_maze_animation.gif
# extracted with contrib/planar_graph_example.py
TESTNODES = (
    (110, 35), (222, 47), (379, 73), (41, 93), (160, 115),
    (286, 115), (421, 130), (67, 171), (225, 171), (334, 177),
    (25, 230), (191, 241), (110, 242), (353, 247), (475, 255),
    (268, 307), (52, 312), (375, 341), (202, 388), (113, 389),
    (458, 407), (27, 415), (308, 429), (112, 466),
)

def test_graph_default_init():
    """Graphs are created empty by default."""
    assert len(Graph().nodes) == 0

def test_graphs_init_nonempty():
    """Graphs may be created with a list of nodes."""
    assert Graph(TESTNODES).nodes == list(TESTNODES)

def test_graph_centre():
    """A Graph's centre is the centre of its bounding box."""
    assert Graph(TESTNODES).centre == (250, 250)
