import pytest
from utg.graph import Node

def test_node_init():
    """Nodes may be created from sequences."""
    assert Node((3, 2)).xy == (3, 2)

def test_node_clone():
    """Nodes may be created from other nodes."""
    assert Node(Node((5, 4))).xy == (5, 4)

@pytest.mark.parametrize(
    "lhs,rhs,expect_equal",
    ((Node((1, 2)), Node((1, 2)), True),
     (Node((1, 2)), Node((1, 3)), False),
     (Node((1, 2)), Node((3, 2)), False),
     (Node((1, 2)), Node((2, 1)), False),
     (Node((2, 3)), (2, 3), True),
     (Node((2, 3)), (3, 2), False),
     ((5, 4), Node((5, 4)), True),
     ((5, 4), Node((4, 5)), False),
     ))
def test_node_comparability(lhs, rhs, expect_equal):
    """Nodes may be compared for equality."""
    assert lhs is not rhs
    assert (lhs == rhs) == expect_equal
    assert (lhs != rhs) != expect_equal
