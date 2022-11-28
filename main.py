import pygame

# import time

pygame.init()

DIS_WIDTH = 600
DIS_HEIGHT = 600
GREEN = "#32CD32"
SIZE = 20
SPEED = 2
FPS = 30

dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption("Snake")

programIcon = pygame.image.load("icon.png")
pygame.display.set_icon(programIcon)

IMAGE = pygame.image.load("icon.png").convert()  # or .convert_alpha()
IMAGE = pygame.transform.scale(IMAGE, (SIZE, SIZE))

clock = pygame.time.Clock()


class Velocity:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Position:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.rect = None

    def draw(self):
        self.rect = pygame.draw.rect(
            dis, GREEN, [self.x, self.y, self.width, self.width]
        )

    def paint_head(self):
        dis.blit(IMAGE, self.rect)


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
            self.blocks[i].draw()
        self.blocks[0].paint_head()

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
                self.blocks[i].x = -SIZE
            elif self.blocks[i].y >= DIS_HEIGHT and self.block_vel[i].y > 0:
                self.blocks[i].y = -SIZE
            elif self.blocks[i].x <= 0 and self.block_vel[i].x < 0:
                self.blocks[i].x = DIS_WIDTH
            elif self.blocks[i].y <= 0 and self.block_vel[i].y < 0:
                self.blocks[i].y = DIS_HEIGHT

        clock.tick(FPS)

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

    def intersect(self):
        c = 0
        for i in range (3, self.length):        ##We check if the head connects with the body. We check the intersection after the third block because when the snake turns, the second and third block touch the first one
            if self.blocks[0].x < self.blocks[i].x + SIZE and self.blocks[0].x > self.blocks[i].x - SIZE and self.blocks[0].y < self.blocks[i].y + SIZE and self.blocks[0].y > self.blocks[i].y - SIZE:
                c += 1
        if self.blocks[0].x > DIS_WIDTH or self.blocks[0].x < 0 or self.blocks[0].y > DIS_HEIGHT or self.blocks[0].y < 0:
            c += 1
        return c == 0

def game_loop(time, counter):
    # time will later be used for score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN and counter > FPS / 5:
            player.keys(event)
            counter = 0
    player.move()
    counter += 1

    dis.fill("#FFFFFF")
    player.draw()
    pygame.display.update()
    return False, counter


game_over = False
player = Snake(40, 40)
time = 0
count = 0
while not game_over:
    game_over, count = game_loop(time, count)
    time += 1
    if Snake.intersect() is False:
        pygame.quit()
        quit()

pygame.quit()
quit()