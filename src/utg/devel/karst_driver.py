import random

from enum import Enum

import pygame

from .driver import Driver

Modes = Enum("Modes", ["FILLING", "ERODING", "FAULTING", "DONE"])

class KarstDriver(Driver):
    def init(self):
        self._map = [[0 for x in range(self.w)] for y in range(self.h)]
        self.w //= 2
        super().init()
        self.ds = pygame.Surface((self.w, self.h))
        self.mode = Modes.FILLING

    def mget(self, x, y):
        """TIC-80 mget"""
        return self._map[y][x]

    def mset(self, x, y, tile_id):
        """TIC-80 mset"""
        self._map[y][x] = tile_id

    def wget(self, x, y):
        """Water get. Where the drops are."""
        return self.mget(x + self.w, y)

    def wset(self, x, y, tile_id):
        """Water set. Where the drops are."""
        return self.mset(x + self.w, y, tile_id)

    def update(self):
        getattr(self, f"_update_{self.mode.name}")()

    def _update_FILLING(self, fast=True):
        num_cells = self.w * (self.h if fast else 1)
        for _ in range(num_cells):
            # Find a column to fill
            x = random.randrange(self.w)
            for x in range(x, x + self.w):
                x %= self.w
                if self.mget(x, 0) == 0:
                    break
            else:
                # for x in range(self.w):
                #     self.wset(x, 0, 255)
                # self.mode = Modes.ERODING
                self.mode = Modes.FAULTING
                return

            # Drop the particle into it
            for y in range(self.h - 1, -1, -1):
                if self.mget(x, y) == 0:
                    self.mset(x, y, random.randrange(1, 256))
                    break

    PRESSURE = 16
    GRAVITY = 64

    def _update_ERODING(self):
        drops = []
        xvalues, yvalues = range(self.w), range(self.h)
        for y0 in yvalues:
            for x0 in xvalues:
                w = self.wget(x0, y0)
                if w == 0:
                    continue
                # Where can it go?
                pressures = []
                for dy in range(2):
                    for dx in range(-1, 2):
                        x1 = x0 + dx
                        y1 = y0 + dy
                        # calculate pressure
                        p = -dy * self.GRAVITY
                        if y1 in yvalues and x1 in xvalues:
                            p += self.mget(x1, y1)
                            if self.wget(x1, y1) != 0:
                                p += self.PRESSURE
                        else:
                            p += 128  # middle?
                        pressures.append((p, (x1, y1)))
                #if x0 == 60:
                #    print("\n".join(map(str, sorted(pressures))))
                #    raise SystemExit
                drops.append((w, (x0, y0), min(pressures)[-1]))
        for w, xy1, xy2 in drops:
            #print(w, xy1, xy2)
            x, y = xy1
            self.wset(x, y, 0)
        for w, xy1, xy2 in drops:
            x, y = xy2
            if y not in yvalues or x not in xvalues:
                print(f"{xy1} -> {xy2} (GONE)")
                continue
            #w -= 1
            if w == 0:
                # it deposits its dissolved carbonate
                #v = self.mget(x, y)
                #if v < 255:
                #    self.mset(x, y, v + 1)
                print(f"{xy1} -> {xy2} and DUMP")
                continue
            # try not to combine droplets
            if self.wget(x, y) != 0:
                x, y = xy1
            # combine droplets?
            v = self.wget(x, y)
            if v != 0:
                w += v
                w = min(w, 255)
            print(f"{xy1} -> {xy2}")
            self.wset(x, y, w)
            self.mset(x, y, max(self.mget(x, y) - 1, 0))
        for x in range(self.w):
            self.wset(x, 0, 255)

    def _update_FAULTING(self, num_faults=20):
        nexi = []
        for threshold in range(256):
            for y in range(self.h):
                for x in range(self.w):
                    if self.mget(x, y) <= threshold:
                        nexi.append((x, y))
            if len(nexi) >= num_faults:
                break
        for i in range(num_faults):
            nexus = random.choice(nexi)
            nexi.remove(nexus)
            x, y = nexus
            if i % 3 == 0:
                self._h_fault(x)
            else:
                self._v_fault(y)
        self.mode = Modes.DONE

    def _h_fault(self, x):
        for y in range(self.h):
            self.mset(x + self.w, y, 1)

    def _v_fault(self, y):
        for x in range(self.w):
            self.mset(x + self.w, y, 1)

    def _update_DONE(self):
        pass

    def draw(self):
        for y in range(self.h):
            for x in range(self.w):
                v = self.mget(x, y)
                w = self.mget(x + self.w, y)
                if self.mode != Modes.ERODING:
                    if w:
                        self.ds.set_at((x, y), (255, 0, 0))
                    else:
                        self.ds.set_at((x, y), (v, v, v))
                    continue
                w = max(v - w, 0)
                self.ds.set_at((x, y), (w, w, v))
        return self.ds


def main():
    random.seed(186283)
    d = KarstDriver()
    d.run()
