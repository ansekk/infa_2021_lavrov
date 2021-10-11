import pygame
from pygame.draw import *

# initialization
pygame.init()

screen = pygame.display.set_mode((300, 200))

clock = pygame.time.Clock()

# main code
# bg
rect(screen, (255, 255, 255), (0, 0, 300, 200))

# face
circle(screen, (200, 200, 30), (150, 100), 50)
circle(screen, (0, 0, 0), (150, 100), 50, 1)

# eye1
circle(screen, (255, 0, 0), (130, 90), 10)
circle(screen, (0, 0, 0), (130, 90), 10, 1)
circle(screen, (0, 0, 0), (130, 90), 3)

# eye2
circle(screen, (255, 0, 0), (170, 90), 10)
circle(screen, (0, 0, 0), (170, 90), 10, 1)
circle(screen, (0, 0, 0), (170, 90), 3)

# eyebrow1
polygon(screen, (0, 0, 0), [(140, 85), (140, 80), (120, 70), (115, 75)])

# eyebrow2
polygon(screen, (0, 0, 0), [(160, 85), (160, 80), (170, 70), (185, 73), (180, 78), (170, 75)])

# mouth
polygon(screen, (0, 0, 0), [(180, 115), (180, 120), (120, 130), (115, 125)])

pygame.display.update()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
