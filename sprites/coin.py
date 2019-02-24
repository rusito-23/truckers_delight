import pygame
from extras.util import Image, path_for
from extras.spritesheet import spritesheet
from extras.util import Direction
from extras.config import width, coin_height, coin_width


class Coin(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = spritesheet(path_for(Image.COIN))
        self.movement = []
        i = 0
        while i < 692:
            img = sprite_sheet.image_at((i, 0, 115, 97), colorkey=(0, 0, 0))
            img = pygame.transform.scale(img, (coin_width, coin_height))
            i += 115
            for _ in range(0, 50):
                self.movement.append(img)
        self.index = 0
        self.image = self.movement[self.index]
        self.rect = self.image.get_rect()
        self.image_none = sprite_sheet.image_at((692, 115, 115, 97),
                                                colorkey=(0, 0, 0))

        self.fx = x
        self.rect.x = x
        self.rect.y = y
        self.used = False

    def update(self, direction):
        # update position
        if not direction == Direction.STEADY:
            self.rect.x -= 1
            if self.rect.x < -self.rect.width:
                self.rect.x = width
                self.used = False
                self.index = 0

        # show movement
        if not self.used:
            self.index += 1
            if self.index >= len(self.movement):
                self.index = 0
            self.image = self.movement[self.index]
            return True
        else:
            self.image = self.image_none


class Coins:

    def __init__(self, quantity, all_height):
        self.coins = []

        start = width
        extra = 15
        self.quantity = quantity

        while (start < width + (quantity * (coin_width + extra))):
            coin = Coin(start, all_height)
            self.coins.append(coin)
            start += coin_width + extra

    def update(self, direction):
        for c in self.coins:
            c.update(direction)

    def check(self, player):
        for c in self.coins:
            if c.rect.colliderect(player.rect) and player.is_alive():
                if not c.used:
                    player.coins += 1
                c.used = True
