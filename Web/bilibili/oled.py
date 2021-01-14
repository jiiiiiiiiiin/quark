import os
import pygame
import sys
from pygame.locals import *

drivers = ['/dev/fb1']


class PyScope:
    screen = None

    def __init__(self):
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_FBDEV'):
                os.putenv('SDL_FBDEV', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print("Driver: " + str(driver) + "failed.")
                continue
            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')

        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print("Framebuffer size: %d x %d" % (size[0], size[1]))
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        pygame.font.init()
        pygame.display.update()
        pygame.mouse.set_visible(False)

    def __del__(self):
        """Destructor to make sure pygame shuts down, etc."""

    def test(self):
        white = (255, 255, 255)
        self.screen.fill(white)
        pygame.image.load('favicon.ico')
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


scope = PyScope()
scope.test()
