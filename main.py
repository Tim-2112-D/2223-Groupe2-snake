import pygame

pygame.init()

dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()


def game_loop():
    pass


game_over = False
while not game_over:
    for event in pygame.event.get():

        game_loop()
        pygame.display.update()

        if event.type == pygame.QUIT:
            game_over = True

pygame.quit()
quit()
