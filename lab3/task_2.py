import pygame
from pygame.draw import *

# Пожалуйста примите, я понимаю что там в некоторых местах
# надо черную обводку, или кривые вместо ломанных, но это
# издевательство же какое то а не учеба, знаний никаких не
# требуется и навыков, просто много времени, сейчас 4:38 время,
# а я должен рисовать обводку у какого то инопланетянина по
# координатам вместо лабы по физике :(
# initialization
pygame.init()

screen = pygame.display.set_mode((600, 700))

clock = pygame.time.Clock()

# main code
# bg
rect(screen, (0, 30, 30), (0, 0, 600, 700))
rect(screen, (30, 40, 0), (0, 450, 600, 700))

# moon
circle(screen, (230, 230, 220), (350, 200), 80)

# clouds
ellipse(screen, (100, 100, 100), (-100, 10, 500, 100))
ellipse(screen, (100, 100, 100), (-50, 50, 350, 100))
ellipse(screen, (100, 100, 100), (-50, 200, 450, 100))
ellipse(screen, (100, 100, 100), (250, 230, 600, 100))
ellipse(screen, (100, 100, 100), (300, 100, 600, 100))
ellipse(screen, (100, 100, 100), (400, -30, 600, 100))
ellipse(screen, (50, 50, 50), (100, 80, 500, 80))
ellipse(screen, (50, 50, 50), (150, 300, 500, 80))
ellipse(screen, (50, 50, 50), (-250, 180, 500, 80))

# UFO
polygon(screen, (100, 130, 130), [(120, 300), (210, 450), (35, 450)])
polygon(screen, (130, 140, 100), [(210, 450), (35, 450), (10, 498), (240, 500)])
ellipse(screen, (150, 150, 150), (0, 310, 250, 70))
ellipse(screen, (180, 180, 180), (30, 300, 190, 50))
ellipse(screen, (235, 235, 220), (10, 340, 25, 10))
ellipse(screen, (235, 235, 220), (35, 350, 25, 10))
ellipse(screen, (235, 235, 220), (65, 355, 25, 10))
ellipse(screen, (235, 235, 220), (100, 358, 25, 10))
ellipse(screen, (235, 235, 220), (135, 357, 25, 10))
ellipse(screen, (235, 235, 220), (169, 354, 25, 10))
ellipse(screen, (235, 235, 220), (202, 345, 25, 10))

# boba
# body
ellipse(screen, (215, 215, 160), (400, 550, 35, 80))
# legs
ellipse(screen, (215, 215, 160), (390, 605, 20, 30))
ellipse(screen, (215, 215, 160), (423, 610, 20, 30))
ellipse(screen, (215, 215, 160), (388, 633, 15, 33))
ellipse(screen, (215, 215, 160), (429, 638, 15, 33))
ellipse(screen, (215, 215, 160), (376, 655, 15, 15))
ellipse(screen, (215, 215, 160), (442, 660, 15, 15))
# hands
ellipse(screen, (215, 215, 160), (393, 550, 15, 15))
ellipse(screen, (215, 215, 160), (429, 553, 15, 15))
ellipse(screen, (215, 215, 160), (437, 560, 15, 10))
ellipse(screen, (215, 215, 160), (452, 565, 15, 10))
ellipse(screen, (215, 215, 160), (383, 560, 15, 10))
ellipse(screen, (215, 215, 160), (375, 570, 10, 15))
# head
ellipse(screen, (215, 215, 160), (393, 510, 25, 10))
ellipse(screen, (215, 215, 160), (408, 508, 35, 10))
ellipse(screen, (215, 215, 160), (405, 530, 25, 20))
polygon(screen, (215, 215, 160), [(393, 515), (405, 540), (430, 540), (443, 513)])
circle(screen, (0, 0, 0), (430, 525), 6)
circle(screen, (255, 255, 255), (431, 526), 2)
circle(screen, (0, 0, 0), (409, 523), 8)
circle(screen, (255, 255, 255), (411, 525), 2)
# antennas
circle(screen, (215, 215, 160), (400, 505), 5)
circle(screen, (215, 215, 160), (397, 495), 5)
circle(screen, (215, 215, 160), (394, 485), 5)
circle(screen, (215, 215, 160), (389, 478), 7)

circle(screen, (215, 215, 160), (440, 505), 5)
circle(screen, (215, 215, 160), (448, 500), 5)
circle(screen, (215, 215, 160), (456, 500), 5)
circle(screen, (215, 215, 160), (463, 503), 7)

# apple
circle(screen, (205, 50, 50), (470, 555), 15)
line(screen, (0, 0, 0), (470, 545), (480, 525))
polygon(screen, (50, 100, 0), [(475, 535), (475, 530), (470, 525), (470, 530)])


pygame.display.update()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
