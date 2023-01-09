import pygame

BLINK_EVENT = pygame.USEREVENT + 0

SIZE = 20
DIS_WIDTH = 600
DIS_HEIGHT = 600

FPS = 30

CLOCK = pygame.time.Clock()

COLORS = {
    "GREEN": "#32CD32",
    "RED": "#F22323",
    "WHITE": "#FFFFFF",
    "BLACK": "#000000",
    "GREY": "#878787",

    "INACTIVE": pygame.Color("lightskyblue3"),
    "ACTIVE": pygame.Color("dodgerblue2"),
}

pygame.font.init()
LARGE_FONT = pygame.font.SysFont("arial", 20)
FONT = pygame.font.Font(None, 32)
