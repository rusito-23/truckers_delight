import pygame
from sprites.scenario import Asset
from extras.util import load_image, Image
from sprites.trucker import State


class Obstacle(Asset):

    def fetch_image(self):
        img = load_image(Image.TRASH)
        return pygame.transform.scale(img, (64, 102))

    def __init__(self, fy, sy):
        Asset.__init__(self, fy, sy)
        self.update_image()

    def check(self, player):
        if self.rect.colliderect(player.rect) and player.is_alive():

            selftop = self.rect.centery - self.rect.height / 2
            playerbottom = player.rect.centery + player.rect.height / 2
            playerbottom -= 5

            if playerbottom < selftop:
                player.state = State.ALIVE
                return
            player.die()
