import random

from enum import Enum

import pygame

from .driver import Driver

Modes = Enum("Modes", ["FILLING", "ERODING"])

class KarstDriver(Driver):
    def init(self):
        self._map = [[0 for x in range(self.w)] for y in range(self.h)]
        self.w //= 2
        super().init()
        self.ds = pygame.Surface((self.w, self.h))
        self.mode = Modes.FILLING

    def mget(self, x, y):
        return self._map[y][x]

    def mset(self, x, y, tile_id):
        self._map[y][x] = tile_id

    def update(self):
        getattr(self, f"_update_{self.mode.name}")()

    def _update_FILLING(self):
        for _ in range(self.w):
            # Find a column to fill
            x = random.randrange(self.w)
            for x in range(x, x + self.w):
                x %= self.w
                if self.mget(x, 0) == 0:
                    break
            else:
                self.mode = Modes.ERODING
                return

            # Drop the particle into it
            for y in range(self.h - 1, -1, -1):
                if self.mget(x, y) == 0:
                    self.mset(x, y, random.randrange(1, 256))
                    break

    def draw(self):
        for y in range(self.h):
            for x in range(self.w):
                v = self.mget(x, y)
                self.ds.set_at((x, y), (v, v, v))
        return self.ds


def main():
    random.seed(186283)
    d = KarstDriver()
    d.run()
