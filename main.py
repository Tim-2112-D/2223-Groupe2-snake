import pygame

from items import Apple, Snake
from screens import Scoreboard, Startscreen
import constants

pygame.init()

dis = pygame.display.set_mode((constants.DIS_WIDTH, constants.DIS_HEIGHT))
pygame.display.set_caption("Snake")

programIcon = pygame.image.load("icon.png")
pygame.display.set_icon(programIcon)

IMAGE1 = pygame.image.load("Charles_face.png").convert_alpha()
IMAGE1 = pygame.transform.scale(IMAGE1, (constants.SIZE, constants.SIZE))

IMAGE2 = pygame.image.load("TIM_snake_face.png").convert_alpha()
IMAGE2 = pygame.transform.scale(IMAGE2, (constants.SIZE, constants.SIZE))


def play(score):
    player1.move()
    player2.move()

    dis.fill(constants.COLORS["WHITE"])
    apple.draw(dis)
    score_text_one, score_rect_one = player1.draw(dis)
    score_text_two, score_rect_two = player2.draw(dis)
    s = pygame.Surface(
        (constants.DIS_WIDTH - min(score_rect_one.left, score_rect_two.left) + 10, 60)
    )  # the constants.SIZE of your rect
    s.set_alpha(128)  # alpha level
    s.fill(constants.COLORS["GREY"])  # this fills the entire surface
    dis.blit(s, (min(score_rect_one.left, score_rect_two.left) - 10, 0))
    dis.blit(score_text_one, (score_rect_one.left, score_rect_one.top))
    dis.blit(score_text_two, (score_rect_two.left, score_rect_two.top))
    apple.collide(player1)
    apple.collide(player2)

    if player1.intersect() or player1.intersection(player2):
        score.set_score(dis, player1.score, player2.score, 2)
        return True
    elif player2.intersect() or player2.intersection(player1):
        score.set_score(dis, player1.score, player2.score, 1)
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
        start.render(dis)

    if not gameover and game_play:
        gameover = play(score)

    pygame.display.update()

    return False


def initialize(name_one="1", name_two="2"):
    global quit_game, gameover, player1, player2, apple, time, score
    quit_game = False
    gameover = False
    player1 = Snake(40, 100, 1, name_one, IMAGE1)
    player2 = Snake(40, constants.DIS_HEIGHT - 120, 2, name_two, IMAGE2)
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
