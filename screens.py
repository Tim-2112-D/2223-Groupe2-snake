import pygame
import constants
from inputbox import InputBox

class Scoreboard:
    def __init__(self, score1, name1, score2, name2, winner):
        self._score1 = score1
        self._name1 = name1
        self._score2 = score2
        self._name2 = name2
        self._winner = winner

    def render(self, dis):
        dis.fill(constants.COLORS["BLACK"])

        text_scoreboard = constants.LARGE_FONT.render("Scoreboard", True, constants.COLORS["WHITE"])
        text_scoreboard_rect = text_scoreboard.get_rect(center=(constants.DIS_WIDTH / 2, 60))
        dis.blit(text_scoreboard, text_scoreboard_rect)

        text_score_one = constants.LARGE_FONT.render(
            f"Player {[self._name1, self._name2][int(self._winner)-1]} wins!!!",
            True,
            constants.COLORS["WHITE"],
        )
        text_score_one_rect = text_score_one.get_rect(center=(constants.DIS_WIDTH / 2, 90))
        dis.blit(text_score_one, text_score_one_rect)

        text_score_one = constants.LARGE_FONT.render(
            f"{self._name1}: {self._score1}", True, constants.COLORS["WHITE"]
        )
        text_score_one_rect = text_score_one.get_rect(center=(constants.DIS_WIDTH / 2, 120))
        dis.blit(text_score_one, text_score_one_rect)

        text_score_two = constants.LARGE_FONT.render(
            f"{self._name2}: {self._score2}", True, constants.COLORS["WHITE"]
        )
        text_score_two_rect = text_score_two.get_rect(center=(constants.DIS_WIDTH / 2, 150))
        dis.blit(text_score_two, text_score_two_rect)

        text_score_two = constants.LARGE_FONT.render(
            "Press SPACE to start a new game", True, constants.COLORS["WHITE"]
        )
        text_score_two_rect = text_score_two.get_rect(center=(constants.DIS_WIDTH / 2, 250))
        dis.blit(text_score_two, text_score_two_rect)

    def set_score(self, dis, score1, score2, winner):
        self._score1 = score1
        self._score2 = score2
        self._winner = winner
        self.render(dis)

    
class Startscreen:
    def __init__(self):
        self.text_snake = constants.LARGE_FONT.render("SNAKE", True, constants.COLORS["WHITE"])
        self.text_snake_rect = self.text_snake.get_rect(center=(constants.DIS_WIDTH / 2, 60))
        self.text_author = constants.LARGE_FONT.render(
            "by Charles Dezons and Tim Daffner", True, constants.COLORS["WHITE"]
        )
        self.text_author_rect = self.text_author.get_rect(center=(constants.DIS_WIDTH / 2, 80))
        self.text_player_one = constants.LARGE_FONT.render(
            "Please enter Name of Player 1:", True, constants.COLORS["WHITE"]
        )
        self.text_player_one_rect = self.text_player_one.get_rect(
            center=(constants.DIS_WIDTH / 2, 140)
        )
        self.input_one = InputBox(constants.DIS_WIDTH / 2 - 100, 160, 140, 32)
        self.text_player_two = constants.LARGE_FONT.render(
            "Please enter Name of Player 2:", True, constants.COLORS["WHITE"]
        )
        self.text_player_two_rect = self.text_player_two.get_rect(
            center=(constants.DIS_WIDTH / 2, 220)
        )
        self.input_two = InputBox(constants.DIS_WIDTH / 2 - 100, 240, 140, 32)

        self.text_enter = constants.LARGE_FONT.render("Press ENTER when ready", True, constants.COLORS["WHITE"])
        self.text_enter_rect = self.text_enter.get_rect(center=(constants.DIS_WIDTH / 2, 400))

    def render(self, dis):
        dis.fill(constants.COLORS["BLACK"])
        dis.blit(self.text_snake, self.text_snake_rect)
        dis.blit(self.text_author, self.text_author_rect)
        dis.blit(self.text_player_one, self.text_player_one_rect)
        self.input_one.draw(dis)
        self.input_one.update()
        dis.blit(self.text_player_two, self.text_player_two_rect)
        self.input_two.draw(dis)
        self.input_two.update()
        dis.blit(self.text_enter, self.text_enter_rect)
