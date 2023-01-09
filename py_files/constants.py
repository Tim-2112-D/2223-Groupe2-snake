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
FONTS = {
    "NORMAL": pygame.font.SysFont("arial", 20),
    "LARGE": pygame.font.SysFont("arial", 26)
}

DISPLAY = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
IMAGE1 = pygame.image.load("Charles_face.png").convert_alpha()
IMAGE2 = pygame.image.load("TIM_snake_face.png").convert_alpha()

IMAGES = {
    "ICON": pygame.image.load("icon.png"),
    "CHARLES": pygame.transform.scale(IMAGE1, (SIZE, SIZE)),
    "TIM": pygame.transform.scale(IMAGE2, (SIZE, SIZE)),
}
