import pygame

from py_files.items import Apple, Snake
from py_files.screens import Scoreboard, Startscreen, Game
import py_files.constants as const

pygame.init()

pygame.display.set_caption("Snake")
pygame.display.set_icon(const.IMAGES["ICON"])


def game_loop():
    global game_play

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            game.player1.keys(event, game.time)
            game.player2.keys(event, game.time)

            if event.key == pygame.K_SPACE and game.gameover:
                game.__init__(start.input_one.text, start.input_two.text)

            if event.key == pygame.K_RETURN and not game_play:
                game_play = True
                game.__init__(start.input_one.text, start.input_two.text)
        if not game_play:
            start.input_one.handle_event(event)
            start.input_two.handle_event(event)

    if not game.gameover and not game_play:
        start.render()

    if not game.gameover and game_play:
        game.gameover = game.play()

    pygame.display.update()

    return False


start = Startscreen()
game = Game()
game_play = False

while not game.quit_game:
    game.quit_game = game_loop()
    game.time += 1

pygame.quit()
quit()
