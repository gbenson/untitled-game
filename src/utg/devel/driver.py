import pygame


class Driver:
    def __init__(self):
        self.w = 240
        self.h = 136
        self.fps = 60

    def run(self):
        self.init()
        try:
            self._run()
        finally:
            self.teardown()

    def _run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def init(self):
        pygame.init()
        dinfo = pygame.display.Info()
        xscale = dinfo.current_w // self.w
        yscale = dinfo.current_h // self.h
        self.scale = max(1, min(xscale, yscale))
        dsize = self.w * self.scale, self.h * self.scale
        self.display = pygame.display.set_mode(dsize)
        pygame.display.set_caption("Untitled game")
        self.clock = pygame.time.Clock()

    def teardown(self):
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            self.handle_event(event)

    def handle_event(self, event):
        if event.type == pygame.KEYUP:
            raise SystemExit

    def update(self):
        pass

    def draw(self):
        pass


def main():
    d = Driver()
    d.run()
