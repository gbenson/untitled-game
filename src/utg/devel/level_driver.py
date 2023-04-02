import matplotlib
import matplotlib.pyplot as plt

from utg.level import Level


# The dark blue nodes from
# https://commons.wikimedia.org/wiki/File:Graph_based_maze_animation.gif
# extracted with contrib/planar_graph_example.py
TESTNODES = (
    (110, 35), (222, 47), (379, 73), (41, 93), (160, 115),
    (286, 115), (421, 130), (67, 171), (225, 171), (334, 177),
    (25, 230), (191, 241), (110, 242), (353, 247), (475, 255),
    (268, 307), (52, 312), (375, 341), (202, 388), (113, 389),
    (458, 407), (27, 415), (308, 433), (112, 466),
)

def main():
    level = Level(TESTNODES)
    # print(f"points.dtype = {level.points.dtype}")
    # print(f"dmesh.points.dtype = {level.dmesh.points.dtype}")
    # print(f"len(dmesh.simplices) = {len(level.dmesh.simplices)}")

    matplotlib.use("GTK3Agg")
    plt.triplot([v.x for v in level.d_vertices],
                [v.y for v in level.d_vertices],
                level._d_simplices)
    plt.plot([v.x for v in level.d_vertices],
             [v.y for v in level.d_vertices], "bo")
    plt.plot([v.x for v in level.v_vertices],
             [v.y for v in level.v_vertices], "yo")
    plt.gca().invert_yaxis()
    plt.show()
