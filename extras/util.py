import pygame


class Direction:
    LEFT = -1
    STEADY = 0
    RIGHT = 1


class Image:
    TRUCKER = "truckers_delight.gif"
    SPRITE_SHEET = "truckers_delight_spritesheet.png"
    CLOUD = "cloud.png"
    CITY = "city.png"
    TRASH = "trash.png"
    MENU = "truckers_delight_logo.gif"
    ANY_KEY = "any_key.png"
    GAME_OVER = "game_over.png"
    COIN = "coin.png"
    PIXEL_FONT = "pixel.ttf"
    SOLID_BACK = "solid_back.png"
    HEART = "heart.png"


PATH = "assets/"


def load_image(img):
    image = pygame.image.load(PATH + img).convert_alpha()
    return image


def path_for(img):
    return PATH + img
