import random
import pygame

import py_files.constants as const


class Velocity:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Position:
    def __init__(self, x: int, y: int, width: int, form: str = "rect", image=None):
        self.x = x
        self.y = y
        self.width = width
        self.form = form
        self.object: None | pygame.Rect = None
        self.image = image

    def draw(self, color: str | pygame.Color):
        if self.form == "rect":
            self.object = pygame.draw.rect(
                const.DISPLAY, color, [self.x, self.y, self.width, self.width]
            )
        elif self.form == "circle":
            self.object = pygame.draw.circle(
                const.DISPLAY, color, [self.x, self.y], self.width
            )

    def paint_head(self):
        const.DISPLAY.blit(self.image, self.object)


class Apple:
    def __init__(self):
        self.circle: Position = Position(
            random.randint(const.SIZE, const.DIS_WIDTH - const.SIZE),
            random.randint(const.SIZE, const.DIS_WIDTH - const.SIZE),
            const.SIZE / 2,
            "circle",
        )

    def draw(self):
        self.circle.draw(const.COLORS["RED"])

    def move(self):
        self.circle.x = random.randint(const.SIZE, const.DIS_WIDTH - const.SIZE)
        self.circle.y = random.randint(const.SIZE, const.DIS_WIDTH - const.SIZE)

    def collide(self, player):
        x_dist: int = min(
            [
                player.blocks[0].x + player.blocks[0].width - self.circle.x,
                player.blocks[0].x - self.circle.x,
            ],
            key=abs,
        )
        y_dist: int = min(
            [
                player.blocks[0].y + player.blocks[0].width - self.circle.y,
                player.blocks[0].y - self.circle.y,
            ],
            key=abs,
        )
        distance: int = pow(x_dist, 2) + pow(y_dist, 2)
        if distance <= pow(self.circle.width, 2):
            self.move()
            player.grow()


class Snake:
    def __init__(
        self, x_pos: int, y_pos: int, keyboard: int, name: str, image: pygame.Surface
    ):
        self.last_pause: int = 0
        self.block_counter: int = 0
        self.length: int = 4
        # This variable will help us attribute the good keys
        # (1 for player one, 2 for player 2)
        self.keyboard = keyboard
        self.name = name
        self.image = image
        self.blocks: list[Position] = [
            Position(x_pos - i * const.SIZE, y_pos, const.SIZE, "rect", self.image)
            for i in range(self.length)
        ]
        self.speed: int = 2
        self.vel: Velocity = Velocity(self.speed, 0)
        self.block_vel: list[Velocity] = [
            Velocity(self.speed, 0) for _ in range(self.length)
        ]
        self.score: int = self.length - 4

    def draw(self) -> tuple[pygame.Surface, pygame.Rect]:
        corners: set = self.find_corner()
        for corner in corners:
            pygame.draw.rect(
                const.DISPLAY,
                const.COLORS["GREEN"],
                [corner[0], corner[1], const.SIZE, const.SIZE],
            )
        self.blocks[0].draw(const.COLORS["GREEN"])
        for i in range(1, len(self.blocks)):
            self.blocks[i].draw(const.COLORS["GREEN"])
        self.blocks[0].paint_head()

        score_text: pygame.Surface = const.FONTS["NORMAL"].render(
            f"Player {self.name}: {self.score}", True, const.COLORS["BLACK"]
        )
        score_rect: pygame.Rect = score_text.get_rect(
            center=(0, -10 + 25 * self.keyboard)
        )
        score_rect.right = const.DIS_WIDTH - 10

        return score_text, score_rect

    def find_corner(self) -> set:
        corner_pos: set = set(())
        for i in range(1, len(self.blocks)):
            vec1: list[int] = [
                1 if self.block_vel[i - 1].x == 0 else 0,
                1 if self.block_vel[i - 1].y == 0 else 0,
            ]
            vec2: list[int] = [
                1 if self.block_vel[i].x == 0 else 0,
                1 if self.block_vel[i].y == 0 else 0,
            ]
            pos: tuple = (
                vec1[0] * self.blocks[i - 1].x + vec2[0] * self.blocks[i].x,
                vec1[1] * self.blocks[i - 1].y + vec2[1] * self.blocks[i].y,
            )
            if (vec1[0] + vec2[0]) * (vec1[1] + vec2[1]) != 0:
                corner_pos.add(pos)
        return corner_pos

    # Gives the good key depending on the snake (int keyboard)
    def keys(self, event: pygame.event, counter: int, apple: Apple, player: any):
        if counter - self.last_pause <= const.FPS / 5:
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
        if self.block_counter >= const.SIZE / self.speed:
            self.block_vel.pop(-1)
            self.block_vel = [Velocity(self.vel.x, self.vel.y)] + self.block_vel
            self.block_counter = 0

        for i in range(self.length):
            self.blocks[i].x += self.block_vel[i].x
            self.blocks[i].y += self.block_vel[i].y

        const.CLOCK.tick(const.FPS)

    def grow(self):
        self.length += 1
        self.blocks.append(
            Position(
                self.blocks[-1].x - self.block_vel[-1].x / self.speed * const.SIZE,
                self.blocks[-1].y - self.block_vel[-1].y / self.speed * const.SIZE,
                const.SIZE,
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
                    velocity.x = int(velocity.x / abs(velocity.x) * self.speed)
                if velocity.y != 0:
                    velocity.y = int(velocity.y / abs(velocity.y) * self.speed)

    def intersect(self) -> bool:
        # We check if the head connects with the body.
        # We check the intersection after the third block because when the snake turns,
        # the second and third block touch the first one
        for i in range(3, self.length):
            if (
                self.blocks[i].x - const.SIZE
                < self.blocks[0].x
                < self.blocks[i].x + const.SIZE
                and self.blocks[i].y - const.SIZE
                < self.blocks[0].y
                < self.blocks[i].y + const.SIZE
            ):
                return True
        if (
            self.blocks[0].x > const.DIS_WIDTH - const.SIZE
            or self.blocks[0].x < -2
            or self.blocks[0].y > const.DIS_HEIGHT - const.SIZE
            or self.blocks[0].y < 0
        ):
            return True
        return False

    def intersection(self, snake) -> bool:
        for block1 in snake.blocks:
            dist_x: int = abs(block1.x - self.blocks[0].x)
            dist_y: int = abs(block1.y - self.blocks[0].y)
            if dist_x + dist_y <= const.SIZE:
                return True
        else:
            return False


class BaseAISnake(Snake):
    NAME: str

    def keys(self, event: pygame.event, counter: int, goal: Position, player: Snake):
        if counter - self.last_pause <= const.FPS:
            pass
        else:
            self.aim(goal, counter)

    def aim(self, goal: Position, counter: int):
        dist = [
            self.blocks[0].x + self.blocks[0].width / 2 - goal.x,
            self.blocks[0].y + self.blocks[0].width / 2 - goal.y,
        ]
        # signs were the other way around, but actually works better like this,
        # since not as predictable
        if dist[0] > -goal.width and self.vel.x == 0:
            self.vel.x = -self.speed
            self.vel.y = 0
            self.last_pause = counter
        elif dist[0] < goal.width and self.vel.x == 0:
            self.vel.x = self.speed
            self.vel.y = 0
            self.last_pause = counter
        elif dist[1] > -goal.width and self.vel.y == 0:
            self.vel.x = 0
            self.vel.y = -self.speed
            self.last_pause = counter
        elif dist[1] < goal.width and self.vel.y == 0:
            self.vel.x = 0
            self.vel.y = self.speed
            self.last_pause = counter


class PacifistAI(BaseAISnake):
    NAME: str = "AI-PACIFIST"

    def keys(self, event: pygame.event, counter: int, apple: Apple, player: Snake):
        if counter - self.last_pause <= const.FPS:
            pass
        else:
            self.aim(apple.circle, counter)


class KamikazeAI(BaseAISnake):
    NAME = "AI-KAMIKAZE"

    def keys(self, event: pygame.event, counter: int, apple: Apple, player: Snake):
        if counter - self.last_pause <= const.FPS:
            pass
        else:
            self.aim(player.blocks[0], counter)


class FollowerAI(BaseAISnake):
    NAME = "AI-FOLLOW"

    def keys(self, event: pygame.event, counter: int, apple: Apple, player: Snake):
        if counter - self.last_pause <= const.FPS:
            pass
        else:
            self.aim(player.blocks[-1], counter)


class MurderAI(BaseAISnake):
    NAME = "AI-MURDER"

    def keys(self, event: pygame.event, counter: int, apple: Apple, player: Snake):
        if counter - self.last_pause <= const.FPS:
            pass
        else:
            goal = Position(
                player.blocks[0].x + 200 * player.block_vel[0].x,
                player.blocks[0].y + 200 * player.block_vel[0].y,
                player.blocks[0].width,
            )
            self.aim(goal, counter)


class RandomAI(BaseAISnake):
    NAME = "AI-RANDOM"

    def keys(self, event: pygame.event, counter: int, apple: Apple, player: Snake):
        if counter - self.last_pause <= const.FPS:
            pass
        else:
            self.aim(
                Position(
                    random.randint(0, const.DIS_WIDTH),
                    random.randint(0, const.DIS_HEIGHT),
                    1,
                ),
                counter,
            )


# User Input: AI-PACIFIST, AI-KAMIKAZE, AI-FOLLOW, AI-MURDER, AI-RANDOM
ALL_AIS: dict = {
    ai_class.NAME: ai_class
    for ai_class in [PacifistAI, KamikazeAI, MurderAI, FollowerAI, RandomAI]
}
