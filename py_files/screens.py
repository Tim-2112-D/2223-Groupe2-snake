import pygame

import py_files.constants as const
import py_files.items as items
from py_files.inputbox import InputBox
from py_files.save_score import write_hs, get_hs


class Startscreen:
    def __init__(self):
        self.text_snake: pygame.Surface = const.FONTS["NORMAL"].render(
            "SNAKE", True, const.COLORS["WHITE"]
        )
        self.text_snake_rect: pygame.rect = self.text_snake.get_rect(
            center=(const.DIS_WIDTH / 2, 60)
        )
        self.text_author: pygame.Surface = const.FONTS["NORMAL"].render(
            "by Charles Dezons and Tim Daffner", True, const.COLORS["WHITE"]
        )
        self.text_author_rect: pygame.rect = self.text_author.get_rect(
            center=(const.DIS_WIDTH / 2, 80)
        )
        self.text_player_one: pygame.Surface = const.FONTS["NORMAL"].render(
            "Please enter Name of Player 1:", True, const.COLORS["WHITE"]
        )
        self.text_player_one_rect: pygame.rect = self.text_player_one.get_rect(
            center=(const.DIS_WIDTH / 2, 140)
        )
        self.input_one: InputBox = InputBox(
            const.DIS_WIDTH / 2 - 100, 160, 140, 32, "Tim"
        )
        self.text_player_two = const.FONTS["NORMAL"].render(
            "Please enter Name of Player 2:", True, const.COLORS["WHITE"]
        )
        self.text_player_two_rect: pygame.rect = self.text_player_two.get_rect(
            center=(const.DIS_WIDTH / 2, 220)
        )
        self.input_two: InputBox = InputBox(
            const.DIS_WIDTH / 2 - 100, 240, 140, 32, "Charles"
        )

        self.text_enter: pygame.Surface = const.FONTS["NORMAL"].render(
            "Press ENTER when ready", True, const.COLORS["WHITE"]
        )
        self.text_enter_rect: pygame.rect = self.text_enter.get_rect(
            center=(const.DIS_WIDTH / 2, 500)
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

        text_highscore_title: pygame.Surface = const.FONTS["NORMAL"].render(
            "HIGHSCORES", True, const.COLORS["WHITE"]
        )
        text_highscore_title_rect: pygame.rect = text_highscore_title.get_rect(
            center=(const.DIS_WIDTH / 2, 330)
        )
        const.DISPLAY.blit(text_highscore_title, text_highscore_title_rect)

        highscores: dict[str, int] = get_hs()
        for i, (name, score) in enumerate(highscores.items()):
            if i > 2:
                break
            text_highscore: pygame.Surface = const.FONTS["NORMAL"].render(
                f"{name}: {score}", True, const.COLORS["WHITE"]
            )
            text_highscore_rect: pygame.rect = text_highscore.get_rect(
                center=(const.DIS_WIDTH / 2, 360 + i * 30)
            )
            const.DISPLAY.blit(text_highscore, text_highscore_rect)

        const.DISPLAY.blit(self.text_enter, self.text_enter_rect)


class Game:
    def __init__(self, name_one: str = "1", name_two: str = "2"):
        self.quit_game: bool = False
        self.gameover: bool = False
        player_class1 = items.ALL_AIS.get(name_one, items.Snake)
        self.player1: items.Snake = player_class1(
            40, 100, 1, name_one, const.IMAGES["CHARLES"]
        )
        player_class2 = items.ALL_AIS.get(name_two, items.Snake)
        self.player2: items.Snake = player_class2(
            40, const.DIS_HEIGHT - 120, 2, name_two, const.IMAGES["TIM"]
        )

        self.apple: items.Apple = items.Apple()
        self.time: int = 0
        self.score: Scoreboard = Scoreboard(
            self.player1.score,
            self.player1.name,
            self.player2.score,
            self.player2.name,
            1,
        )

    def play(self) -> bool:
        self.player1.move()
        self.player2.move()

        const.DISPLAY.fill(const.COLORS["WHITE"])
        self.apple.draw()
        score_text_one, score_rect_one = self.player1.draw()
        score_text_two, score_rect_two = self.player2.draw()
        s: pygame.Surface = pygame.Surface(
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
    def __init__(self, score1: int, name1: str, score2: int, name2: str, winner: int):
        self._score1 = score1
        self._name1 = name1
        self._score2 = score2
        self._name2 = name2
        self._winner = winner

    def render(self):
        const.DISPLAY.fill(const.COLORS["BLACK"])

        text_scoreboard: pygame.Surface = const.FONTS["NORMAL"].render(
            "Scoreboard", True, const.COLORS["WHITE"]
        )
        text_scoreboard_rect: pygame.Rect = text_scoreboard.get_rect(
            center=(const.DIS_WIDTH / 2, 60)
        )
        const.DISPLAY.blit(text_scoreboard, text_scoreboard_rect)

        text_winner: pygame.Surface = const.FONTS["NORMAL"].render(
            f"Player {[self._name1, self._name2][self._winner-1]} wins!!!",
            True,
            const.COLORS["WHITE"],
        )
        text_winner_rect: pygame.Rect = text_winner.get_rect(
            center=(const.DIS_WIDTH / 2, 90)
        )
        const.DISPLAY.blit(text_winner, text_winner_rect)

        text_score_one: pygame.Surface = const.FONTS["NORMAL"].render(
            f"{self._name1}: {self._score1}", True, const.COLORS["WHITE"]
        )
        text_score_one_rect: pygame.Rect = text_score_one.get_rect(
            center=(const.DIS_WIDTH / 2, 120)
        )
        const.DISPLAY.blit(text_score_one, text_score_one_rect)

        text_score_two: pygame.Surface = const.FONTS["NORMAL"].render(
            f"{self._name2}: {self._score2}", True, const.COLORS["WHITE"]
        )
        text_score_two_rect: pygame.Rect = text_score_two.get_rect(
            center=(const.DIS_WIDTH / 2, 150)
        )
        const.DISPLAY.blit(text_score_two, text_score_two_rect)

        text_space: pygame.Surface = const.FONTS["NORMAL"].render(
            "Press SPACE to start a new game", True, const.COLORS["WHITE"]
        )
        text_space_rect: pygame.Rect = text_space.get_rect(
            center=(const.DIS_WIDTH / 2, 250)
        )
        const.DISPLAY.blit(text_space, text_space_rect)

        text_highscore_title: pygame.Surface = const.FONTS["NORMAL"].render(
            "HIGHSCORES", True, const.COLORS["WHITE"]
        )
        text_highscore_title_rect: pygame.Rect = text_highscore_title.get_rect(
            center=(const.DIS_WIDTH / 2, 350)
        )
        const.DISPLAY.blit(text_highscore_title, text_highscore_title_rect)

        highscores: dict = get_hs()
        for i, (name, score) in enumerate(highscores.items()):
            if i > 2:
                break
            text_highscore: pygame.Surface = const.FONTS["NORMAL"].render(
                f"{name}: {score}", True, const.COLORS["WHITE"]
            )
            text_highscore_rect: pygame.Rect = text_highscore.get_rect(
                center=(const.DIS_WIDTH / 2, 380 + i * 30)
            )
            const.DISPLAY.blit(text_highscore, text_highscore_rect)

    def set_score(self, score1: int, score2: int, winner: int):
        self._score1 = score1
        self._score2 = score2
        self._winner = winner
        write_hs(self._name1, self._score1)
        write_hs(self._name2, self._score2)
        self.render()
