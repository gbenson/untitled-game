from utg.graph import Graph
from utg.devel.graph_driver import TESTNODES


def test_graph_default_init():
    """Graphs are created empty by default."""
    assert len(Graph().nodes) == 0

def test_graphs_init_nonempty():
    """Graphs may be created with a list of nodes."""
    assert Graph(TESTNODES).nodes == list(TESTNODES)

def test_graph_centre():
    """A Graph's centre is the centre of its bounding box."""
    assert Graph(TESTNODES).centre == (250, 250)

def test_graph_centremost_node():
    """A Graph's centremost node is the node closest to its centre."""
    assert Graph(TESTNODES).centremost_node == (191, 241)
