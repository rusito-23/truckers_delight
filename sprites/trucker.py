import pygame
from extras.util import Image, path_for, Direction
from extras.spritesheet import spritesheet


class State:
    ALIVE = 1
    JUMPING = -1
    DROPPING = 0
    DYING = 23
    DEAD = -23
    ABSOLUTELY_DEAD = 9


class Trucker(pygame.sprite.Sprite):

    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        # load spritesheet
        sprite_sheet = spritesheet(path_for(Image.SPRITE_SHEET))

        # parse spritesheet
        self.run_animation = []
        self.steady = sprite_sheet.image_at(
            (0, 0, width, height), colorkey=(0, 0, 0))
        self.image = self.steady

        # parse animation array
        (x, y) = 0, 0
        while (y < 840):
            img = sprite_sheet.image_at(
                (x, y, width, height), colorkey=(0, 0, 0))
            x += width
            if (x >= 815):
                x = 0
                y += height
            for _ in range(50):
                self.run_animation.append(img)

        # configure rect
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 400
        self.rect.width -= 50
        # animation index
        self.index = 0
        # state
        self.state = State.ALIVE
        # coins
        self.coins = 0
        # lives
        self.lives = 3

    def update(self, direction):
        # dying
        if self.state == State.DYING:
            self.rect.y -= 1
            if self.rect.y <= 230:
                self.state = State.DEAD
            return
        elif self.state == State.DEAD:
            self.rect.y += 1
            if self.rect.y >= 400:
                if self.lives == 0:
                    self.state = State.ABSOLUTELY_DEAD
                else:
                    self.state = State.ALIVE
            return

        # running
        if direction != Direction.STEADY:
            self.index += 1
            if (self.index >= len(self.run_animation)):
                self.index = 0
            self.image = self.run_animation[self.index]
        else:
            self.image = self.steady

        # jumping
        if self.state == State.JUMPING:
            self.rect.y -= 1
            if self.rect.y <= 230:
                self.state = State.DROPPING
        elif self.state == State.DROPPING:
            self.rect.y += 1
            if self.rect.y >= 400:
                self.state = State.ALIVE

        if self.state == State.ALIVE and self.rect.y != 400:
            self.jump()

    def jump(self):
        if not self.state == State.DROPPING and self.is_alive():
            self.state = State.JUMPING

    def avoid_obstacle(self):
        self.state = State.JUMPING

    def die(self):
        print("You dead motherfucker")
        if not self.state == State.DEAD:
            self.image = pygame.transform.rotate(self.image, 90)
            self.state = State.DYING
            self.lives -= 1

    def is_dead(self):
        return self.state == State.ABSOLUTELY_DEAD

    def is_alive(self):
        return not self.state in [State.DEAD, State.DYING,
                                  State.ABSOLUTELY_DEAD]
