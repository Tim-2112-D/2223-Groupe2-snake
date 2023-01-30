import pygame

BLINK_EVENT: int = pygame.USEREVENT + 0

SIZE: int = 20
DIS_WIDTH: int = 600
DIS_HEIGHT: int = 600

FPS: int = 30

CLOCK: pygame.time.Clock = pygame.time.Clock()

COLORS: dict[str, str | pygame.Color] = {
    "GREEN": "#32CD32",
    "RED": "#F22323",
    "WHITE": "#FFFFFF",
    "BLACK": "#000000",
    "GREY": "#878787",
    "INACTIVE": pygame.Color("lightskyblue3"),
    "ACTIVE": pygame.Color("dodgerblue2"),
}

pygame.font.init()
FONTS: dict[str, pygame.Surface] = {
    "NORMAL": pygame.font.SysFont("arial", 20),
    "LARGE": pygame.font.SysFont("arial", 26),
}

DISPLAY: pygame.Surface = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
IMAGE1: pygame.Surface = pygame.image.load("images/Charles_face.png").convert_alpha()
IMAGE2: pygame.Surface = pygame.image.load("images/TIM_snake_face.png").convert_alpha()

IMAGES: dict[str, pygame.Surface] = {
    "ICON": pygame.image.load("images/icon.png"),
    "CHARLES": pygame.transform.scale(IMAGE1, (SIZE, SIZE)),
    "TIM": pygame.transform.scale(IMAGE2, (SIZE, SIZE)),
}
