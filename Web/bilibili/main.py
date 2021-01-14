import json
import os
import sys

import pygame
import pygame.freetype
import requests
from pygame.locals import *

drivers = ['/dev/fb1']


class PyScope:
    screen = None

    def __init__(self, uid):
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
        self.uid = uid
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print("Framebuffer size: %d x %d" % (size[0], size[1]))
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        pygame.font.init()
        pygame.display.update()
        pygame.mouse.set_visible(False)
        pygame.freetype.init()
        self.font = pygame.freetype.Font("font.ttf", 24)

    def __del__(self):
        """Destructor to make sure pygame shuts down, etc."""

    def get_fans(self, uid):
        res = requests.get("http://api.bilibili.com/x/web-interface/card?mid={}".format(uid))
        res = json.loads(res.text)
        if res.get("code") == 0:
            data = res.get("data").get("card")
            ret = {
                "name": data.get("name"),
                "face": data.get("face"),
                "fans": data.get("fans"),
                "friend": data.get("friend")
            }
            name, _ = self.font.render(" 昵 称：{}".format(data.get("name")), (0, 0, 0))
            with open('face.jpg', 'wb') as f:
                f.write(requests.get(data.get("face")).content)
            face = pygame.image.load('face.jpg')
            fans, _ = self.font.render(" 粉丝数：{}".format(data.get("fans")), (0, 0, 0))
            friend, _ = self.font.render(" 关 注：{}".format(data.get("friend")), (0, 0, 0))
            self.screen.blit(name, (0, 60))
            self.screen.blit(pygame.transform.scale(face, (48, 48)), (240 - 60, 6))
            self.screen.blit(fans, (0, 85))
            self.screen.blit(friend, (0, 110))
            return ret
        return None

    def show(self):
        white = (255, 255, 255)
        self.screen.fill(white)
        img = pygame.image.load('logo.png')
        update_info = pygame.USEREVENT
        pygame.time.set_timer(update_info, 3000)
        self.get_fans(self.uid)
        while True:
            self.screen.blit(pygame.transform.scale(img, (120, 57)), (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.get_fans(self.uid)
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


if __name__ == '__main__':
    scope = PyScope(uid="35680373")
    scope.show()
