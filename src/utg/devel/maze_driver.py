import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

from utg.maze import Maze


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
    maze = Maze(TESTNODES)

    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if (event.type == pygame.KEYUP
                and event.key in (pygame.K_ESCAPE,
                                  pygame.K_q)):
                event = pygame.event.Event(pygame.QUIT)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill("white")
        draw_graph(screen, maze.v_graph, "gold")
        draw_graph(screen, maze.d_graph, "navy")
        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)  # wait until next frame (at 60 FPS)

def draw_graph(surface, graph, color, scale=2):
    for edge in graph.edges:
        start, end = [(v.x * scale, v.y*scale) for v in edge.vertices]
        pygame.draw.line(surface, color, start, end, width=2*scale)
    for vertex in graph.vertices:
        pygame.draw.circle(surface, color,
                           (vertex.x * scale,
                            vertex.y * scale),
                           radius=6 * scale)
