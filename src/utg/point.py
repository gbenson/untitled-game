class Point(tuple):
    """A point in two dimensions."""

    # Tuples are immutable => __init__ may not be overridden
    # https://stackoverflow.com/a/13094796/21220975
    # https://docs.python.org/3/reference/datamodel.html#object.__new__
    def __new__(cls, xy):
        t_xy = tuple(xy)
        if len(t_xy) != 2:
            raise ValueError(xy)
        return super(Point, cls).__new__(cls, t_xy)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]
