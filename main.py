import pygame
import random

DIS_WIDTH = 600
DIS_HEIGHT = 600
GREEN = "#32CD32"
RED = "#F22323"
SIZE = 20
SPEED = 2
FPS = 30

pygame.init()

dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption("Snake")

programIcon = pygame.image.load("icon.png")
pygame.display.set_icon(programIcon)

IMAGE1 = pygame.image.load("icon.png").convert()  # or .convert_alpha()
IMAGE1 = pygame.transform.scale(IMAGE1, (SIZE, SIZE))

IMAGE2 = pygame.image.load("TIM_snake_face.png").convert()  # or .convert_alpha()
IMAGE2 = pygame.transform.scale(IMAGE2, (SIZE, SIZE))

clock = pygame.time.Clock()


class Velocity:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Position:
    def __init__(self, x, y, width, form="rect", image=None):
        self.x = x
        self.y = y
        self.width = width
        self.form = form
        self.object = None
        self.image = image

    def draw(self, color):
        if self.form == "rect":
            self.object = pygame.draw.rect(
                dis, color, [self.x, self.y, self.width, self.width]
            )
        elif self.form == "circle":
            self.object = pygame.draw.circle(
                dis, color, [self.x, self.y], self.width
            )

    def paint_head(self):
        dis.blit(self.image, self.object)


class Apple:
    def __init__(self):
        self.circle = Position(random.randint(SIZE, DIS_WIDTH-SIZE), random.randint(SIZE, DIS_WIDTH-SIZE), SIZE/2, "circle")

    def draw(self):
        self.circle.draw(RED)

    def move(self):
        self.circle.x = random.randint(SIZE, DIS_WIDTH-SIZE)
        self.circle.y = random.randint(SIZE, DIS_WIDTH-SIZE)

    def collide(self, player):
        distance = pow((player.blocks[0].x - self.circle.x), 2) + pow((player.blocks[0].y - self.circle.y), 2)
        if distance <= pow((player.blocks[0].width/2 + self.circle.width), 2):
            self.move()
            player.grow()


class Snake:
    def __init__(self, x_pos, y_pos, keyboard, image):
        self.counter = 0
        self.length = 4
        # This variable will help us attribute the good keys (1 for player one, 2 for player 2)
        self.keyboard = keyboard
        self.image = image
        self.blocks = [
            Position(x_pos - i * SIZE, y_pos, SIZE, "rect", self.image) for i in range(self.length)
        ]
        self.vel = Velocity(SPEED, 0)
        self.block_vel = [Velocity(SPEED, 0) for i in range(self.length)]

    def draw(self):
        corners = self.find_corner()
        for corner in corners:
            pygame.draw.rect(dis, GREEN, [corner[0], corner[1], SIZE, SIZE])
        for i in range(len(self.blocks)):
            self.blocks[i].draw(GREEN)
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
            if (vec1[0] + vec2[0]) * (vec1[1] + vec2[1]) != 0:
                corner_pos.add(pos)
        return corner_pos

    # Gives the good key depending on the snake (int keyboard)
    def keys(self, event):
        if self.keyboard == 1:
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
        else:
            if event.key == pygame.K_q and self.vel.x == 0:
                self.vel.x = -SPEED
                self.vel.y = 0
            elif event.key == pygame.K_d and self.vel.x == 0:
                self.vel.x = SPEED
                self.vel.y = 0
            elif event.key == pygame.K_z and self.vel.y == 0:
                self.vel.x = 0
                self.vel.y = -SPEED
            elif event.key == pygame.K_s and self.vel.y == 0:
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

        clock.tick(FPS)

    def grow(self):
        self.length += 1
        self.blocks.append(
            Position(
                self.blocks[-1].x - self.block_vel[-1].x / SPEED * SIZE,
                self.blocks[-1].y - self.block_vel[-1].y / SPEED * SIZE,
                SIZE, "rect", self.image
            )
        )
        self.block_vel.append(Velocity(self.block_vel[-1].x, self.block_vel[-1].y))

    def intersect(self):
        # We check if the head connects with the body.
        # We check the intersection after the third block
        # because when the snake turns, the second and third block touch the first one
        c = 0
        for i in range(3, self.length):
            if (
                self.blocks[i].x - SIZE < self.blocks[0].x < self.blocks[i].x + SIZE
                and self.blocks[i].y - SIZE < self.blocks[0].y < self.blocks[i].y + SIZE
            ):
                c += 1
        if (
            self.blocks[0].x > DIS_WIDTH - SIZE
            or self.blocks[0].x < -2
            or self.blocks[0].y > DIS_HEIGHT - SIZE
            or self.blocks[0].y < 0
        ):
            c += 1
        return c == 0

    def intersection(self, snake):
        c = 0
        for i in range(snake.length):
            if self.blocks[0] == snake.blocks[i]:
                pass
        return c == True


def game_loop(time, counter):
    # time will later be used for score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN and counter > FPS / 5:
            player1.keys(event)
            player2.keys(event)
            counter = 0
    player1.move()
    player2.move()

    counter += 1

    dis.fill("#FFFFFF")
    apple.draw()
    player1.draw()
    player2.draw()
    apple.collide(player1)
    apple.collide(player2)
    pygame.display.update()
    return False, counter


game_over = False
player1 = Snake(40, 40, 1, IMAGE1)
player2 = Snake(40, DIS_HEIGHT - 150, 2, IMAGE2)
apple = Apple()
time = 0
count = 0
while not game_over:
    game_over, count = game_loop(time, count)
    time += 1
    if not (player1.intersect() and player2.intersect()):
        pygame.quit()
        quit()
    elif player1.intersection(player2):
        pygame.quit()
        quit()
    elif player2.intersection(player1):
        pygame.quit()
        quit()

pygame.quit()
quit()