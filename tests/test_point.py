import pytest
from utg.point import Point


@pytest.mark.parametrize(
    "xy",
    ((3, 2),
     [3, 2],
     range(3, 1, -1),
     Point((3, 2)),
     ))
def test_point_init(xy):
    """Points can be initialized from any 2-item iterable."""
    p = Point(xy)
    assert isinstance(p, tuple)
    assert p == (3, 2)


@pytest.mark.parametrize(
    "xy",
    ([3],
     (3, 2, 1),
     range(4),
     (),
     ))
def test_point_dimensionality(xy):
    """Points always have two dimensions."""
    with pytest.raises(ValueError):
        Point(xy)


@pytest.mark.parametrize(
    "lhs,rhs,expect_equal",
    ((Point((1, 2)), Point((1, 2)), True),
     (Point((1, 2)), Point((1, 3)), False),
     (Point((1, 2)), Point((3, 2)), False),
     (Point((1, 2)), Point((2, 1)), False),
     (Point((2, 3)), (2, 3), True),
     (Point((2, 3)), (3, 2), False),
     ((5, 4), Point((5, 4)), True),
     ((5, 4), Point((4, 5)), False),
     (Point((2, 3)), [2, 3], False),  # XXX really?
     ([5, 4], Point((5, 4)), False),  # XXX really?
     ))
def test_point_comparability(lhs, rhs, expect_equal):
    """Points may be compared for equality."""
    assert lhs is not rhs
    assert (lhs == rhs) == expect_equal
    assert (lhs != rhs) != expect_equal
