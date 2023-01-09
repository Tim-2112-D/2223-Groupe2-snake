import pygame

from items import *
from colors import *

pygame.init()

BLINK_EVENT = pygame.USEREVENT + 0

COLOR_INACTIVE = pygame.Color("lightskyblue3")
COLOR_ACTIVE = pygame.Color("dodgerblue2")

LARGE_FONT = pygame.font.SysFont("arial", 20)
FONT = pygame.font.Font(None, 32)


dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption("Snake")

programIcon = pygame.image.load("icon.png")
pygame.display.set_icon(programIcon)

IMAGE1 = pygame.image.load("Charles_face.png").convert_alpha()
IMAGE1 = pygame.transform.scale(IMAGE1, (SIZE, SIZE))

IMAGE2 = pygame.image.load("TIM_snake_face.png").convert_alpha()
IMAGE2 = pygame.transform.scale(IMAGE2, (SIZE, SIZE))


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
    apple.draw(dis)
    score_text_one, score_rect_one = player1.draw(dis, LARGE_FONT)
    score_text_two, score_rect_two = player2.draw(dis, LARGE_FONT)
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
