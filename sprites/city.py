import pygame
from extras.util import Image, load_image, Direction


class City:

    def __init__(self):
        # inicializo dos edificios pegados uno del otro
        self.first = Building(0, self)
        self.second = Building(self.first.rect.x + self.first.rect.width, self)

    def update(self, direction):
        if direction == Direction.STEADY:
            return
        self.first.rect.x -= 1
        self.second.rect.x -= 1
        if (self.first.is_outside_plane()):
            self.first.rect.x = self.second.rect.x + self.second.rect.width
        elif (self.second.is_outside_plane()):
            self.second.rect.x = self.first.rect.x + self.first.rect.width

    def get_buildings(self):
        return [self.first, self.second]


class Building(pygame.sprite.Sprite):
    def __init__(self, xpos, city):
        pygame.sprite.Sprite.__init__(self)

        self.image = load_image(Image.CITY)
        self.rect = self.image.get_rect()

        self.rect.x = xpos
        self.rect.y = 70

        self.city = city

    def is_outside_plane(self):
        return self.rect.x + self.rect.width < 0

    def update(self, direction):
        self.city.update(direction)
