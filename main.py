import pygame
import random

pygame.init()

BLINK_EVENT = pygame.USEREVENT + 0
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

COLOR_INACTIVE = pygame.Color("lightskyblue3")
COLOR_ACTIVE = pygame.Color("dodgerblue2")
FONT = pygame.font.Font(None, 32)


dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption("Snake")

programIcon = pygame.image.load("icon.png")
pygame.display.set_icon(programIcon)

IMAGE1 = pygame.image.load("Charles_face.png").convert_alpha()
IMAGE1 = pygame.transform.scale(IMAGE1, (SIZE, SIZE))

IMAGE2 = pygame.image.load("TIM_snake_face.png").convert_alpha()
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
    def __init__(self, x_pos, y_pos, keyboard, name, image):
        self.last_pause = 0
        self.block_counter = 0
        self.length = 4
        # This variable will help us attribute the good keys
        # (1 for player one, 2 for player 2)
        self.keyboard = keyboard
        self.name = name
        self.image = image
        self.blocks = [
            Position(x_pos - i * SIZE, y_pos, SIZE, "rect", self.image)
            for i in range(self.length)
        ]
        self.speed = 2
        self.vel = Velocity(self.speed, 0)
        self.block_vel = [Velocity(self.speed, 0) for _ in range(self.length)]
        self.score = self.length - 4

    def draw(self):
        corners = self.find_corner()
        for corner in corners:
            pygame.draw.rect(dis, GREEN, [corner[0], corner[1], SIZE, SIZE])
        self.blocks[0].draw(GREEN)
        for i in range(1, len(self.blocks)):
            self.blocks[i].draw(GREEN)
        self.blocks[0].paint_head()

        score_text = LARGE_FONT.render(f"Player {self.name}: {self.score}", True, BLACK)
        score_rect = score_text.get_rect(center=(0, -10 + 25 * self.keyboard))
        score_rect.right = DIS_WIDTH - 10

        return score_text, score_rect

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
        self.score = self.length - 4
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
                return True
        if (
            self.blocks[0].x > DIS_WIDTH - SIZE
            or self.blocks[0].x < -2
            or self.blocks[0].y > DIS_HEIGHT - SIZE
            or self.blocks[0].y < 0
        ):
            return True
        return False

    def intersection(self, snake):
        for block1 in snake.blocks:
            dist_x = abs(block1.x - self.blocks[0].x)
            dist_y = abs(block1.y - self.blocks[0].y)
            if dist_x + dist_y <= SIZE:
                return True
        else:
            return False


class Scoreboard:
    def __init__(self, score1, name1, score2, name2, winner):
        self._score1 = score1
        self._name1 = name1
        self._score2 = score2
        self._name2 = name2
        self._winner = winner

    def render(self):
        dis.fill(BLACK)

        text_scoreboard = LARGE_FONT.render("Scoreboard", True, WHITE)
        text_scoreboard_rect = text_scoreboard.get_rect(center=(DIS_WIDTH / 2, 60))
        dis.blit(text_scoreboard, text_scoreboard_rect)

        text_score_one = LARGE_FONT.render(
            f"Player {[self._name1, self._name2][int(self._winner)-1]} wins!!!",
            True,
            WHITE,
        )
        text_score_one_rect = text_score_one.get_rect(center=(DIS_WIDTH / 2, 90))
        dis.blit(text_score_one, text_score_one_rect)

        text_score_one = LARGE_FONT.render(
            f"{self._name1}: {self._score1}", True, WHITE
        )
        text_score_one_rect = text_score_one.get_rect(center=(DIS_WIDTH / 2, 120))
        dis.blit(text_score_one, text_score_one_rect)

        text_score_two = LARGE_FONT.render(
            f"{self._name2}: {self._score2}", True, WHITE
        )
        text_score_two_rect = text_score_two.get_rect(center=(DIS_WIDTH / 2, 150))
        dis.blit(text_score_two, text_score_two_rect)

        text_score_two = LARGE_FONT.render(
            "Press SPACE to start a new game", True, WHITE
        )
        text_score_two_rect = text_score_two.get_rect(center=(DIS_WIDTH / 2, 250))
        dis.blit(text_score_two, text_score_two_rect)

    def set_score(self, score1, score2, winner):
        self._score1 = score1
        self._score2 = score2
        self._winner = winner
        self.render()


class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Startscreen:
    def __init__(self):
        self.text_snake = LARGE_FONT.render("SNAKE", True, WHITE)
        self.text_snake_rect = self.text_snake.get_rect(center=(DIS_WIDTH / 2, 60))
        self.text_author = LARGE_FONT.render(
            "by Charles Dezons and Tim Daffner", True, WHITE
        )
        self.text_author_rect = self.text_author.get_rect(center=(DIS_WIDTH / 2, 80))
        self.text_player_one = LARGE_FONT.render(
            "Please enter Name of Player 1:", True, WHITE
        )
        self.text_player_one_rect = self.text_player_one.get_rect(
            center=(DIS_WIDTH / 2, 140)
        )
        self.input_one = InputBox(DIS_WIDTH / 2 - 100, 160, 140, 32)
        self.text_player_two = LARGE_FONT.render(
            "Please enter Name of Player 2:", True, WHITE
        )
        self.text_player_two_rect = self.text_player_two.get_rect(
            center=(DIS_WIDTH / 2, 220)
        )
        self.input_two = InputBox(DIS_WIDTH / 2 - 100, 240, 140, 32)

        self.text_enter = LARGE_FONT.render("Press ENTER when ready", True, WHITE)
        self.text_enter_rect = self.text_enter.get_rect(center=(DIS_WIDTH / 2, 400))

    def render(self):
        dis.fill(BLACK)
        dis.blit(self.text_snake, self.text_snake_rect)
        dis.blit(self.text_author, self.text_author_rect)
        dis.blit(self.text_player_one, self.text_player_one_rect)
        self.input_one.draw(dis)
        self.input_one.update()
        dis.blit(self.text_player_two, self.text_player_two_rect)
        self.input_two.draw(dis)
        self.input_two.update()
        dis.blit(self.text_enter, self.text_enter_rect)


def play(score):
    player1.move()
    player2.move()

    dis.fill(WHITE)
    apple.draw()
    score_text_one, score_rect_one = player1.draw()
    score_text_two, score_rect_two = player2.draw()
    s = pygame.Surface(
        (DIS_WIDTH - min(score_rect_one.left, score_rect_two.left) + 10, 60)
    )  # the size of your rect
    s.set_alpha(128)  # alpha level
    s.fill(GREY)  # this fills the entire surface
    dis.blit(s, (min(score_rect_one.left, score_rect_two.left) - 10, 0))
    dis.blit(score_text_one, (score_rect_one.left, score_rect_one.top))
    dis.blit(score_text_two, (score_rect_two.left, score_rect_two.top))
    apple.collide(player1)
    apple.collide(player2)

    if player1.intersect() or player1.intersection(player2):
        score.set_score(player1.score, player2.score, 2)
        return True
    elif player2.intersect() or player2.intersection(player1):
        score.set_score(player1.score, player2.score, 1)
        return True
    return False


def game_loop():
    global start, game_play, gameover, player1, player2, apple, time, score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            player1.keys(event, time)
            player2.keys(event, time)

            if event.key == pygame.K_SPACE and gameover:
                initialize(start.input_one.text, start.input_two.text)

            if event.key == pygame.K_RETURN and not game_play:
                game_play = True
                initialize(start.input_one.text, start.input_two.text)
        if not game_play:
            start.input_one.handle_event(event)
            start.input_two.handle_event(event)

    if not gameover and not game_play:
        start.render()

    if not gameover and game_play:
        gameover = play(score)

    pygame.display.update()

    return False


def initialize(name_one="1", name_two="2"):
    global quit_game, gameover, player1, player2, apple, time, score
    quit_game = False
    gameover = False
    player1 = Snake(40, 100, 1, name_one, IMAGE1)
    player2 = Snake(40, DIS_HEIGHT - 120, 2, name_two, IMAGE2)
    apple = Apple()
    time = 0
    score = Scoreboard(player1.score, player1.name, player2.score, player2.name, 1)


start = Startscreen()
game_play = False
initialize()

while not quit_game:
    quit_game = game_loop()
    time += 1

pygame.quit()
quit()
