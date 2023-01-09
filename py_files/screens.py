import pygame

import py_files.constants as const
import py_files.items as items
from py_files.inputbox import InputBox


class Startscreen:
    def __init__(self):
        self.text_snake = const.FONTS["NORMAL"].render(
            "SNAKE", True, const.COLORS["WHITE"]
        )
        self.text_snake_rect = self.text_snake.get_rect(
            center=(const.DIS_WIDTH / 2, 60)
        )
        self.text_author = const.FONTS["NORMAL"].render(
            "by Charles Dezons and Tim Daffner", True, const.COLORS["WHITE"]
        )
        self.text_author_rect = self.text_author.get_rect(
            center=(const.DIS_WIDTH / 2, 80)
        )
        self.text_player_one = const.FONTS["NORMAL"].render(
            "Please enter Name of Player 1:", True, const.COLORS["WHITE"]
        )
        self.text_player_one_rect = self.text_player_one.get_rect(
            center=(const.DIS_WIDTH / 2, 140)
        )
        self.input_one = InputBox(const.DIS_WIDTH / 2 - 100, 160, 140, 32)
        self.text_player_two = const.FONTS["NORMAL"].render(
            "Please enter Name of Player 2:", True, const.COLORS["WHITE"]
        )
        self.text_player_two_rect = self.text_player_two.get_rect(
            center=(const.DIS_WIDTH / 2, 220)
        )
        self.input_two = InputBox(const.DIS_WIDTH / 2 - 100, 240, 140, 32)

        self.text_enter = const.FONTS["NORMAL"].render(
            "Press ENTER when ready", True, const.COLORS["WHITE"]
        )
        self.text_enter_rect = self.text_enter.get_rect(
            center=(const.DIS_WIDTH / 2, 400)
        )

    def render(self):
        const.DISPLAY.fill(const.COLORS["BLACK"])
        const.DISPLAY.blit(self.text_snake, self.text_snake_rect)
        const.DISPLAY.blit(self.text_author, self.text_author_rect)
        const.DISPLAY.blit(self.text_player_one, self.text_player_one_rect)
        self.input_one.draw(const.DISPLAY)
        self.input_one.update()
        const.DISPLAY.blit(self.text_player_two, self.text_player_two_rect)
        self.input_two.draw(const.DISPLAY)
        self.input_two.update()
        const.DISPLAY.blit(self.text_enter, self.text_enter_rect)


class Game:
    def __init__(self, name_one="1", name_two="2", ai=False):
        self.quit_game = False
        self.gameover = False
        if name_one == "AI":
            self.player1 = items.AI(40, 100, 1, name_one, const.IMAGES["CHARLES"])
        else:
            self.player1 = items.Snake(40, 100, 1, name_one, const.IMAGES["CHARLES"])
        if name_two == "AI":
            self.player2 = items.AI(
                40, const.DIS_HEIGHT - 120, 2, name_two, const.IMAGES["TIM"]
            )
        else:
            self.player2 = items.Snake(
                40, const.DIS_HEIGHT - 120, 2, name_two, const.IMAGES["TIM"]
            )
        self.apple = items.Apple()
        self.time = 0
        self.score = Scoreboard(
            self.player1.score,
            self.player1.name,
            self.player2.score,
            self.player2.name,
            1,
        )

    def play(self):
        self.player1.move()
        self.player2.move()

        const.DISPLAY.fill(const.COLORS["WHITE"])
        self.apple.draw()
        score_text_one, score_rect_one = self.player1.draw()
        score_text_two, score_rect_two = self.player2.draw()
        s = pygame.Surface(
            (const.DIS_WIDTH - min(score_rect_one.left, score_rect_two.left) + 10, 60)
        )  # the const.SIZE of your rect
        s.set_alpha(128)  # alpha level
        s.fill(const.COLORS["GREY"])  # this fills the entire surface
        const.DISPLAY.blit(s, (min(score_rect_one.left, score_rect_two.left) - 10, 0))
        const.DISPLAY.blit(score_text_one, (score_rect_one.left, score_rect_one.top))
        const.DISPLAY.blit(score_text_two, (score_rect_two.left, score_rect_two.top))
        self.apple.collide(self.player1)
        self.apple.collide(self.player2)

        if self.player1.intersect() or self.player1.intersection(self.player2):
            self.score.set_score(self.player1.score, self.player2.score, 2)
            return True
        elif self.player2.intersect() or self.player2.intersection(self.player1):
            self.score.set_score(self.player1.score, self.player2.score, 1)
            return True
        return False


class Scoreboard:
    def __init__(self, score1, name1, score2, name2, winner):
        self._score1 = score1
        self._name1 = name1
        self._score2 = score2
        self._name2 = name2
        self._winner = winner

    def render(self):
        const.DISPLAY.fill(const.COLORS["BLACK"])

        text_scoreboard = const.FONTS["NORMAL"].render(
            "Scoreboard", True, const.COLORS["WHITE"]
        )
        text_scoreboard_rect = text_scoreboard.get_rect(
            center=(const.DIS_WIDTH / 2, 60)
        )
        const.DISPLAY.blit(text_scoreboard, text_scoreboard_rect)

        text_score_one = const.FONTS["NORMAL"].render(
            f"Player {[self._name1, self._name2][int(self._winner)-1]} wins!!!",
            True,
            const.COLORS["WHITE"],
        )
        text_score_one_rect = text_score_one.get_rect(center=(const.DIS_WIDTH / 2, 90))
        const.DISPLAY.blit(text_score_one, text_score_one_rect)

        text_score_one = const.FONTS["NORMAL"].render(
            f"{self._name1}: {self._score1}", True, const.COLORS["WHITE"]
        )
        text_score_one_rect = text_score_one.get_rect(center=(const.DIS_WIDTH / 2, 120))
        const.DISPLAY.blit(text_score_one, text_score_one_rect)

        text_score_two = const.FONTS["NORMAL"].render(
            f"{self._name2}: {self._score2}", True, const.COLORS["WHITE"]
        )
        text_score_two_rect = text_score_two.get_rect(center=(const.DIS_WIDTH / 2, 150))
        const.DISPLAY.blit(text_score_two, text_score_two_rect)

        text_score_two = const.FONTS["NORMAL"].render(
            "Press SPACE to start a new game", True, const.COLORS["WHITE"]
        )
        text_score_two_rect = text_score_two.get_rect(center=(const.DIS_WIDTH / 2, 250))
        const.DISPLAY.blit(text_score_two, text_score_two_rect)

    def set_score(self, score1, score2, winner):
        self._score1 = score1
        self._score2 = score2
        self._winner = winner
        self.render()
