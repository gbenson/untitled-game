import numpy as np

from scipy.spatial import Delaunay


class Level:
    def __init__(self, points=()):
        self.points = np.array(points)
        self.dmesh = Delaunay(self.points)
