import pygame
from extras import config
import random
from extras.util import Direction


class Asset(pygame.sprite.Sprite):

    def __init__(self, fy, sy):
        pygame.sprite.Sprite.__init__(self)
        self.fy = fy
        self.sy = sy

    def update(self, direction):
        if direction != Direction.STEADY:
            if (self.rect.x < -self.rect.width):
                self.update_image()
            else:
                self.rect.x -= 1

    def update_image(self):
        self.image = self.fetch_image()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(config.width, config.width + 250)
        self.rect.y = random.randint(self.fy, self.sy)
        self.rect.width -= 50
