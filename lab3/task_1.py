import pygame
from pygame.draw import *

# initialization
pygame.init()

screen = pygame.display.set_mode((300, 200))

clock = pygame.time.Clock()

# main code

pygame.display.update()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
