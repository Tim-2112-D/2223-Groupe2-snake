import pygame

# import time

pygame.init()

dis_width = 600
dis_height = 600
green = "#32CD32"
size = 20
speed = 2

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake")

programIcon = pygame.image.load("icon.png")
pygame.display.set_icon(programIcon)

IMAGE = pygame.image.load("icon.png").convert()  # or .convert_alpha()
IMAGE = pygame.transform.scale(IMAGE, (size, size))

clock = pygame.time.Clock()


def drawGrid():
    for x in range(0, dis_width, size):
        for y in range(0, dis_height, size):
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
        rect = pygame.draw.rect(dis, green, [self.x, self.y, self.width, self.width])
        if image is True:
            dis.blit(IMAGE, rect)


class Snake:
    def __init__(self, x_pos, y_pos):
        self.counter = 0
        self.length = 4
        self.blocks = [
            Position(x_pos - i * size, y_pos, size) for i in range(self.length)
        ]
        self.vel = Velocity(speed, 0)
        self.block_vel = [Velocity(speed, 0) for i in range(self.length)]

    def draw(self):
        for block in self.blocks:
            block.draw(block == self.blocks[0])

    def keys(self, event):
        if event.key == pygame.K_LEFT and self.vel.x == 0:
            self.vel.x = -speed
            self.vel.y = 0
        elif event.key == pygame.K_RIGHT and self.vel.x == 0:
            self.vel.x = speed
            self.vel.y = 0
        elif event.key == pygame.K_UP and self.vel.y == 0:
            self.vel.x = 0
            self.vel.y = -speed
        elif event.key == pygame.K_DOWN and self.vel.y == 0:
            self.vel.x = 0
            self.vel.y = speed
        # cheat until apples are implemented
        elif event.key == pygame.K_SPACE:
            self.grow()

    def move(self):
        self.counter += 1
        if self.counter >= size / speed:
            self.block_vel.pop(-1)
            self.block_vel = [Velocity(self.vel.x, self.vel.y)] + self.block_vel
            self.counter = 0

        for i in range(self.length):
            self.blocks[i].x += self.block_vel[i].x
            self.blocks[i].y += self.block_vel[i].y

            if self.blocks[i].x >= dis_width and self.block_vel[i].x > 0:
                self.blocks[i].x = 0
            elif self.blocks[i].y >= dis_height and self.block_vel[i].y > 0:
                self.blocks[i].y = 0
            elif self.blocks[i].x <= -20 and self.block_vel[i].x < 0:
                self.blocks[i].x = dis_width - 20
            elif self.blocks[i].y <= -20 and self.block_vel[i].y < 0:
                self.blocks[i].y = dis_height - 20

        clock.tick(30)

    def grow(self):
        self.length += 1
        self.blocks.append(
            Position(
                self.blocks[-1].x - self.block_vel[-1].x / speed * size,
                self.blocks[-1].y - self.block_vel[-1].y / speed * size,
                size,
            )
        )
        self.block_vel.append(Velocity(self.block_vel[-1].x, self.block_vel[-1].y))


def game_loop(time):
    drawGrid()
    if time % size / speed == 0:
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
