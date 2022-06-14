import pygame, sys
from pygame.locals import *


def run_example():
    screen_size = (256, 256)
    title = "Hello World"
    bg_color = (0, 0, 0)

    pygame.init()

    display_surf = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(title)

    clock = pygame.time.Clock()

    x = 0

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # clear screen
        display_surf.fill(bg_color)

        # update objects
        x += 1

        # draw objects to screen
        color = (255, 53, 184)
        pygame.draw.rect(display_surf, color, pygame.Rect(50 + x, 50, 25, 25))

        # update screen
        pygame.display.flip()
