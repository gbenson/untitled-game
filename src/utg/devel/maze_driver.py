import os
import random

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

from utg.maze import Maze
from utg.solver import CaveSolver


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


if True:
    num_rows = 8
    num_cols = 4
    page_width = 30
    page_height = 17

    x_clear = 2
    y_clear = 2
    nodes_per_page = 6

    map_width = page_width * num_cols
    map_height = page_height * num_rows

    scale = 10


def testnodes():
    random.seed(186283)
    for row in range(num_rows):
        ymin = row * page_height
        ymax = ymin + page_height
        ymin += y_clear
        ymax -= y_clear
        for col in range(num_cols):
            xmin = col * page_width
            xmax = xmin + page_width
            xmin += x_clear
            xmax -= x_clear
            for _ in range(nodes_per_page):
                yield (random.randrange(xmin, xmax),
                       random.randrange(ymin, ymax))

def clear(screen):
    for row in range(num_rows):
        ymin = row * page_height
        for col in range(num_cols):
            if row & 1 == col & 1:
                continue
            xmin = col * page_width
            screen.fill("#eeeeee",
                        pygame.Rect(
                            [d * scale
                             for d in (xmin, ymin,
                                       page_width,
                                       page_height)]))


def main():
    maze = Maze(testnodes())
    solver = CaveSolver(maze)

    pygame.init()
    screen = pygame.display.set_mode((120 * scale, 136 * scale))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    event = pygame.event.Event(pygame.QUIT)
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        try:
            solver.visit()
        except StopIteration:
            pass

        screen.fill("white")
        clear(screen)
        draw_graph(screen, maze.path_graph, "gold")
        draw_graph(screen, maze.wall_graph, "navy")
        pygame.display.flip()  # Refresh on-screen display
        clock.tick(20)  # wait until next frame (at 60 FPS)

def draw_graph(surface, graph, color):
    for edge in graph.edges:
        if not edge.visible:
            continue
        start, end = [(v.x * scale, v.y*scale) for v in edge.vertices]
        pygame.draw.line(surface,
                         "red" if edge.visited else color,
                         start, end, width=5)
    for vertex in graph.vertices:
        pygame.draw.circle(surface,
                           "red" if vertex.visited else color,
                           (vertex.x * scale,
                            vertex.y * scale),
                           radius=5)
