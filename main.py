import pygame
from extras import config
from extras.config import width, height
from sprites.trucker import Trucker
from sprites.cloud import Cloud
from sprites.city import City
from extras.util import Direction, load_image, Image, path_for
from sprites.obstacle import Obstacle
from sprites.coin import Coins
from sprites.menu_option import MenuOption


class Main:

    def __init__(self):
        # screen
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(config.SKY)
        # display
        pygame.display.set_caption("Truckers Delight")
        # init sprite list
        self.sprites = pygame.sprite.OrderedUpdates()
        self.init_sprites()

        # font
        pygame.font.init()
        self.font = pygame.font.Font(path_for(Image.PIXEL_FONT), 30)
        self.small_font = pygame.font.Font(path_for(Image.PIXEL_FONT), 23)

        self.clock = pygame.time.Clock()

    def init_sprites(self):
        # init sprites
        self.player = Trucker(163, 168)

        self.city = City()

        self.first_cloud = Cloud(0, 150)
        self.second_cloud = Cloud(0, 150)
        self.obstacle = Obstacle(480, 480)

        self.coins = Coins(5, 250)
        self.coins2 = Coins(3, 400)

        # sprites
        for b in self.city.get_buildings():
            self.sprites.add(b)
        self.sprites.add(self.first_cloud)
        self.sprites.add(self.second_cloud)
        self.sprites.add(self.obstacle)
        for c in self.coins.coins:
            self.sprites.add(c)
        for c in self.coins2.coins:
            self.sprites.add(c)
        self.sprites.add(self.player)

        # updatables
        self.updatables = [
            self.city,
            self.first_cloud,
            self.second_cloud,
            self.player,
            self.obstacle,
            self.coins,
            self.coins2
        ]

        # collideables
        self.collideables = [
            self.obstacle,
            self.coins,
            self.coins2
        ]

        # direction
        self.direction = Direction.STEADY

    def menu(self):
        background = load_image(Image.MENU)
        background = pygame.transform.scale(background, (width, height))

        any_key = load_image(Image.ANY_KEY)
        any_key = pygame.transform.scale(any_key, (400, 100))

        menu = True
        while (menu):

            self.screen.blit(background, (0, 0))
            self.screen.blit(any_key, (220, 30))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    menu = False

            pygame.display.update()
        self.main_menu()

    def main_menu(self):
        background = load_image(Image.SOLID_BACK)
        select_option_text = self.font.render("Please select an option", False,
                                              (255, 255, 255))

        options = [
            MenuOption.PLAY,
            MenuOption.QUIT
        ]
        selected_option = 0

        menu = True
        while menu:

            self.screen.blit(background, (0, 0))

            x = 100
            for opt in options:

                color = (255, 255, 255)
                text = opt
                if opt == options[selected_option]:
                    color = (190, 90, 0)
                    text = '> ' + text
                else:
                    text = '  ' + text

                surface = self.font.render(text, False, color)
                self.screen.blit(surface, (300, x))
                x += 100

            self.screen.blit(self.player.image, (300, 400))
            self.screen.blit(select_option_text, (100, 20))
            self.player.update(Direction.RIGHT)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if selected_option == len(options) - 1:
                            selected_option = 0
                        else:
                            selected_option += 1
                    elif event.key == pygame.K_UP:
                        if selected_option == 0:
                            selected_option = len(options) - 1
                        else:
                            selected_option -= 1
                    elif event.key == pygame.K_RETURN:
                        option = options[selected_option]
                        if option == MenuOption.PLAY:
                            menu = False
                        elif option == MenuOption.QUIT:
                            pygame.quit()
                            return

            pygame.display.update()
        self.run()

    def run(self):
        heart = load_image(Image.HEART)
        heart = pygame.transform.scale(heart, (50, 50))
        running = True
        while (running):

            self.screen.fill(config.SKY)
            self.sprites.draw(self.screen)

            # dead?
            if self.player.is_dead():
                running = False
                self.retry_menu()

            # hearts
            x = 10
            for _ in range(self.player.lives):
                self.screen.blit(heart, (x, 10))
                x += 50

            # show score
            score = self.small_font.render(
                'YOUR SCORE: ' + str(self.player.coins), False, (0, 0, 0))
            self.screen.blit(score, (500, 10))

            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.update_direction(event)

            # update all
            for up in self.updatables:
                up.update(self.direction)

            # check for collisions
            for col in self.collideables:
                col.check(self.player)

            pygame.display.update()
            self.clock.tick(240)

    def retry_menu(self):
        self.sprites.empty()

        background = load_image(Image.GAME_OVER)
        background = pygame.transform.scale(background, (width, height))

        any_key = load_image(Image.ANY_KEY)
        any_key = pygame.transform.scale(any_key, (400, 100))

        score = self.font.render('YOUR SCORE: ' + str(self.player.coins),
                                 False, (255, 255, 255))

        decision = False
        while not decision:

            self.sprites.draw(self.screen)
            self.screen.blit(background, (0, 0))
            self.screen.blit(any_key, (220, 30))
            self.screen.blit(score, (250, 500))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    decision = True

            pygame.display.flip()
        self.init_sprites()
        self.main_menu()

    def update_direction(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key in [pygame.K_SPACE, pygame.K_UP]:
                    self.player.jump()
            elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                self.direction = Direction.STEADY


if __name__ == "__main__":
    main = Main()
    main.menu()
