import pygame
from extras.util import Image, path_for
from extras.spritesheet import spritesheet
import random
from scenario import Asset


class Cloud(Asset):

    def fetch_image(self):
        sprite_sheet = spritesheet(path_for(Image.CLOUD))
        if random.choice([True, False]):
            img = sprite_sheet.image_at((0, 0, 540, 250), colorkey=(0, 0, 0))
        else:
            img = sprite_sheet.image_at((0, 250, 540, 250), colorkey=(0, 0, 0))
        return pygame.transform.scale(img, (270, 125))

    def __init__(self, fy, sy):
        Asset.__init__(self, fy, sy)
        self.update_image()
