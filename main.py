import pygame

pygame.init()

dis_width = 600
dis_height = 600
green = "#32CD32"

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()


class Snake:
    def __init__(self, xpos, ypos):
        self.pos = [xpos, ypos]
        self.vel = [20, 0]

    def draw(self):
        pygame.draw.rect(dis, green, [self.pos[0], self.pos[1], 20, 20])

    def keys(self, event):
        if event.key == pygame.K_LEFT and self.vel[0] != 20:
            self.vel[0] = -20
            self.vel[1] = 0
        elif event.key == pygame.K_RIGHT and self.vel[0] != -20:
            self.vel[0] = 20
            self.vel[1] = 0
        elif event.key == pygame.K_UP and self.vel[1] != 20:
            self.vel[0] = 0
            self.vel[1] = -20
        elif event.key == pygame.K_DOWN and self.vel[0] != 20:
            self.vel[0] = 0
            self.vel[1] = 20

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.pos[0] >= dis_width - 20 and self.vel[0] > 0:
            self.pos[0] = -20
        elif self.pos[1] >= dis_height - 20 and self.vel[1] > 0:
            self.pos[1] = -20
        elif self.pos[0] <= -20 and self.vel[0] < 0:
            self.pos[0] = dis_width - 20
        elif self.pos[1] <= -20 and self.vel[1] < 0:
            self.pos[1] = dis_height - 20
        clock.tick(2)


def game_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            player.keys(event)
    player.move()

    dis.fill("#FFFFFF")
    player.draw()
    pygame.display.update()
    return False


game_over = False
player = Snake(40, 40)
while not game_over:
    game_over = game_loop()

pygame.quit()
quit()
