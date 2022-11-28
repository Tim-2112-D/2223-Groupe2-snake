import pygame

# import time

pygame.init()

DIS_WIDTH = 600
DIS_HEIGHT = 600
GREEN = "#32CD32"
SIZE = 20
SPEED = 2

dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption("Snake")

programIcon = pygame.image.load("icon.png")
pygame.display.set_icon(programIcon)

IMAGE = pygame.image.load("icon.png").convert()  # or .convert_alpha()
IMAGE = pygame.transform.scale(IMAGE, (SIZE, SIZE))

clock = pygame.time.Clock()


def drawGrid():
    for x in range(0, DIS_WIDTH, SIZE):
        for y in range(0, DIS_HEIGHT, SIZE):
            # rect = pygame.Rect(x, y, size, size)
            # pygame.draw.rect(dis, rect, 1)
            pass


class Velocity:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Position:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width

    def draw(self, image=False):
        rect = pygame.draw.rect(dis, GREEN, [self.x, self.y, self.width, self.width])
        if image is True:
            dis.blit(IMAGE, rect)


class Snake:
    def __init__(self, x_pos, y_pos):
        self.counter = 0
        self.length = 4
        self.blocks = [
            Position(x_pos - i * SIZE, y_pos, SIZE) for i in range(self.length)
        ]
        self.vel = Velocity(SPEED, 0)
        self.block_vel = [Velocity(SPEED, 0) for i in range(self.length)]

    def draw(self):
        corners = self.find_corner()
        for corner in corners:
            pygame.draw.rect(dis, GREEN, [corner[0], corner[1], SIZE, SIZE])
        for i in range(len(self.blocks)):
            self.blocks[i].draw(self.blocks[i] == self.blocks[0])

    def find_corner(self):
        corner_pos = set(())
        for i in range(1, len(self.blocks)):
            vec1 = [
                1 if self.block_vel[i - 1].x == 0 else 0,
                1 if self.block_vel[i - 1].y == 0 else 0,
            ]
            vec2 = [
                1 if self.block_vel[i].x == 0 else 0,
                1 if self.block_vel[i].y == 0 else 0,
            ]
            pos = (
                vec1[0] * self.blocks[i - 1].x + vec2[0] * self.blocks[i].x,
                vec1[1] * self.blocks[i - 1].y + vec2[1] * self.blocks[i].y,
            )
            if 0 not in pos:
                corner_pos.add(pos)
        return corner_pos

    def keys(self, event):
        if event.key == pygame.K_LEFT and self.vel.x == 0:
            self.vel.x = -SPEED
            self.vel.y = 0
        elif event.key == pygame.K_RIGHT and self.vel.x == 0:
            self.vel.x = SPEED
            self.vel.y = 0
        elif event.key == pygame.K_UP and self.vel.y == 0:
            self.vel.x = 0
            self.vel.y = -SPEED
        elif event.key == pygame.K_DOWN and self.vel.y == 0:
            self.vel.x = 0
            self.vel.y = SPEED
        # cheat until apples are implemented
        elif event.key == pygame.K_SPACE:
            self.grow()

    def move(self):
        # counter until block has to move
        self.counter += 1
        if self.counter >= SIZE / SPEED:
            self.block_vel.pop(-1)
            self.block_vel = [Velocity(self.vel.x, self.vel.y)] + self.block_vel
            self.counter = 0

        for i in range(self.length):
            self.blocks[i].x += self.block_vel[i].x
            self.blocks[i].y += self.block_vel[i].y

            if self.blocks[i].x >= DIS_WIDTH and self.block_vel[i].x > 0:
                self.blocks[i].x = 0
            elif self.blocks[i].y >= DIS_HEIGHT and self.block_vel[i].y > 0:
                self.blocks[i].y = 0
            elif self.blocks[i].x <= -20 and self.block_vel[i].x < 0:
                self.blocks[i].x = DIS_WIDTH - 20
            elif self.blocks[i].y <= -20 and self.block_vel[i].y < 0:
                self.blocks[i].y = DIS_HEIGHT - 20

        clock.tick(30)

    def grow(self):
        self.length += 1
        self.blocks.append(
            Position(
                self.blocks[-1].x - self.block_vel[-1].x / SPEED * SIZE,
                self.blocks[-1].y - self.block_vel[-1].y / SPEED * SIZE,
                SIZE,
            )
        )
        self.block_vel.append(Velocity(self.block_vel[-1].x, self.block_vel[-1].y))


def game_loop(time):
    drawGrid()
    if time % SIZE / SPEED == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                player.keys(event)
    player.move()

    dis.fill("#FFFFFF")
    player.draw()
    pygame.display.update()
    return False


game_over = False
player = Snake(40, 40)
time = 0
while not game_over:
    time += 1
    game_over = game_loop(time)

pygame.quit()
quit()
