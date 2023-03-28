import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

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

class GraphDriver:
    def __init__(self):
        self.graph = Graph(TESTNODES)
        self.screen = pygame.display.set_mode((1000, 1000))
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.one_frame()

    def one_frame(self):
        for event in pygame.event.get():
            if (event.type == pygame.KEYUP
                and event.key in (pygame.K_ESCAPE,
                                  pygame.K_q)):
                event = pygame.event.Event(pygame.QUIT)
            else:
                self.update_graph()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.draw_screen()
        pygame.display.flip()  # Refresh on-screen display
        self.clock.tick(60)  # wait until next frame (at 60 FPS)

    def draw_screen(self, scale=2):
        self.screen.fill("white")
        for node in self.graph.nodes:
            pygame.draw.circle(self.screen,
                               "navy",
                               (node.x * scale,
                                node.y * scale),
                               radius=6 * scale)

    def update_graph(self):
        pass


def main():
    gd = GraphDriver()
    gd.run()