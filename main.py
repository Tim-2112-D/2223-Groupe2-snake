import pygame

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake')

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
