import pygame
import random

pygame.init()

DIS_WIDTH = 600
DIS_HEIGHT = 600
GREEN = "#32CD32"
RED = "#F22323"
WHITE = "#FFFFFF"
BLACK = "#000000"
GREY = "#878787"
LARGE_FONT = pygame.font.SysFont("arial", 20)
SIZE = 20
FPS = 30


dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption("Snake")

programIcon = pygame.image.load("icon.png")
pygame.display.set_icon(programIcon)

IMAGE1 = pygame.image.load("Charles_face.png").convert_alpha()  # or .convert_alpha()
IMAGE1 = pygame.transform.scale(IMAGE1, (SIZE, SIZE))

IMAGE2 = pygame.image.load("TIM_snake_face.png").convert_alpha()  # or .convert_alpha()
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
            self.object = pygame.draw.circle(dis, color, [self.x, self.y], self.width)

    def paint_head(self):
        dis.blit(self.image, self.object)


class Apple:
    def __init__(self):
        self.circle = Position(
            random.randint(SIZE, DIS_WIDTH - SIZE),
            random.randint(SIZE, DIS_WIDTH - SIZE),
            SIZE / 2,
            "circle",
        )

    def draw(self):
        self.circle.draw(RED)

    def move(self):
        self.circle.x = random.randint(SIZE, DIS_WIDTH - SIZE)
        self.circle.y = random.randint(SIZE, DIS_WIDTH - SIZE)

    def collide(self, player):
        x_dist = min(
            [
                player.blocks[0].x + player.blocks[0].width - self.circle.x,
                player.blocks[0].x - self.circle.x,
            ],
            key=abs,
        )
        y_dist = min(
            [
                player.blocks[0].y + player.blocks[0].width - self.circle.y,
                player.blocks[0].y - self.circle.y,
            ],
            key=abs,
        )
        distance = pow(x_dist, 2) + pow(y_dist, 2)
        if distance <= pow(self.circle.width, 2):
            self.move()
            player.grow()


class Snake:
    def __init__(self, x_pos, y_pos, keyboard, image):
        self.last_pause = 0
        self.block_counter = 0
        self.length = 4
        # This variable will help us attribute the good keys
        # (1 for player one, 2 for player 2)
        self.keyboard = keyboard
        self.image = image
        self.blocks = [
            Position(x_pos - i * SIZE, y_pos, SIZE, "rect", self.image)
            for i in range(self.length)
        ]
        self.speed = 2
        self.vel = Velocity(self.speed, 0)
        self.block_vel = [Velocity(self.speed, 0) for _ in range(self.length)]
        self.score = LARGE_FONT.render(
            f"Player {self.keyboard}: {self.length-4}", True, BLACK, GREY
        )

    def draw(self):
        corners = self.find_corner()
        for corner in corners:
            pygame.draw.rect(dis, GREEN, [corner[0], corner[1], SIZE, SIZE])
        self.blocks[0].draw(GREEN)
        for i in range(1, len(self.blocks)):
            self.blocks[i].draw(GREEN)
        self.blocks[0].paint_head()

        dis.blit(self.score, (500, -15 + 25 * self.keyboard))

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
    def keys(self, event, counter):
        if counter - self.last_pause <= FPS / 5:
            pass
        elif self.keyboard == 1:
            if event.key == pygame.K_LEFT and self.vel.x == 0:
                self.vel.x = -self.speed
                self.vel.y = 0
                self.last_pause = counter
            elif event.key == pygame.K_RIGHT and self.vel.x == 0:
                self.vel.x = self.speed
                self.vel.y = 0
                self.last_pause = counter
            elif event.key == pygame.K_UP and self.vel.y == 0:
                self.vel.x = 0
                self.vel.y = -self.speed
                self.last_pause = counter
            elif event.key == pygame.K_DOWN and self.vel.y == 0:
                self.vel.x = 0
                self.vel.y = self.speed
                self.last_pause = counter

            # cheat until apples are implemented
            elif event.key == pygame.K_SPACE:
                self.grow()
        elif self.keyboard == 2:
            if (event.key == pygame.K_q or event.key == pygame.K_a) and self.vel.x == 0:
                self.vel.x = -self.speed
                self.vel.y = 0
                self.last_pause = counter
            elif event.key == pygame.K_d and self.vel.x == 0:
                self.vel.x = self.speed
                self.vel.y = 0
                self.last_pause = counter
            elif (
                event.key == pygame.K_z or event.key == pygame.K_w
            ) and self.vel.y == 0:
                self.vel.x = 0
                self.vel.y = -self.speed
                self.last_pause = counter
            elif event.key == pygame.K_s and self.vel.y == 0:
                self.vel.x = 0
                self.vel.y = self.speed
                self.last_pause = counter

            # cheat until apples are implemented
            elif event.key == pygame.K_SPACE:
                self.grow()

    def move(self):
        # counter until block has to move
        self.block_counter += 1
        if self.block_counter >= SIZE / self.speed:
            self.block_vel.pop(-1)
            self.block_vel = [Velocity(self.vel.x, self.vel.y)] + self.block_vel
            self.block_counter = 0

        for i in range(self.length):
            self.blocks[i].x += self.block_vel[i].x
            self.blocks[i].y += self.block_vel[i].y

        clock.tick(FPS)

    def grow(self):
        self.length += 1
        self.blocks.append(
            Position(
                self.blocks[-1].x - self.block_vel[-1].x / self.speed * SIZE,
                self.blocks[-1].y - self.block_vel[-1].y / self.speed * SIZE,
                SIZE,
                "rect",
                self.image,
            )
        )
        self.block_vel.append(Velocity(self.block_vel[-1].x, self.block_vel[-1].y))
        self.score = LARGE_FONT.render(
            f"Player {self.keyboard}: {self.length-4}", True, BLACK, GREY
        )
        if (self.length - 4) > 0 and (self.length - 4) % 10 == 0:
            self.speed += 2
            for velocity in self.block_vel:
                if velocity.x != 0:
                    velocity.x = velocity.x / abs(velocity.x) * self.speed
                if velocity.y != 0:
                    velocity.y = velocity.y / abs(velocity.y) * self.speed

    def intersect(self):
        # We check if the head connects with the body.
        # We check the intersection after the third block because when the snake turns,
        # the second and third block touch the first one
        for i in range(3, self.length):
            if (
                self.blocks[i].x - SIZE < self.blocks[0].x < self.blocks[i].x + SIZE
                and self.blocks[i].y - SIZE < self.blocks[0].y < self.blocks[i].y + SIZE
            ):
                return False
        if (
            self.blocks[0].x > DIS_WIDTH - SIZE
            or self.blocks[0].x < -2
            or self.blocks[0].y > DIS_HEIGHT - SIZE
            or self.blocks[0].y < 0
        ):
            return False
        return True

    def intersection(self, snake):
        for block1 in snake.blocks:
            dist_x = abs(block1.x - self.blocks[0].x)
            dist_y = abs(block1.y - self.blocks[0].y)
            if dist_x + dist_y <= SIZE:
                return True
        else:
            return False

def Scoreboard(snake1, snake2):
    font = pygame.font.Font(None, 36)
    score1 = snake1.length
    score2 = snake2.length
    scores = [
        {"name": "Player 1", "score": snake1.length},
        {"name": "Player 2", "score": snake2.length},
    ]
    dis.fill(BLACK)
    text = font.render("Scoreboard", True, WHITE)
    text_rect = text.get_rect()
    text_rect.centerx = DIS_WIDTH // 2
    text_rect.y = 10
    dis.blit(text, text_rect)
    # Draw the scores
    y = 50
    for score in scores:
        text = font.render(f"{score['name']}: {score['score']}", True, WHITE)
        text_rect = text.get_rect()
        text_rect.centerx = DIS_WIDTH // 2
        text_rect.y = y
        dis.blit(text, text_rect)
        y += 50
    pygame.display.update()



def redrawWindow():
    text = LARGE_FONT.render(
        "Score: " + str(30), True, (255, 255, 255)
    )  # create our text

    dis.blit(text, (700, 10))  # draw the text to the screen


def game_loop(time):
    # time will later be used for score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            player1.keys(event, time)
            player2.keys(event, time)
    player1.move()
    player2.move()

    dis.fill(WHITE)
    pygame.draw.rect(dis, GREY, [490, 0, 110, 70])
    apple.draw()
    player1.draw()
    player2.draw()
    apple.collide(player1)
    apple.collide(player2)
    pygame.display.update()
    return False


game_over = False
player1 = Snake(40, 40, 1, IMAGE1)
player2 = Snake(40, DIS_HEIGHT - 150, 2, IMAGE2)
apple = Apple()
time = 0
while not game_over:
    game_over = game_loop(time)
    time += 1
    if not (player1.intersect() and player2.intersect()):
        break
    elif player1.intersection(player2):
        break
    elif player2.intersection(player1):
        break
while not game_over:
    Scoreboard(player1, player2)
    pygame.time.delay(1000)

pygame.quit()
quit()
