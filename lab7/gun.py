import math
import random
from random import choice
from random import randint as rnd
import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
ORANGE = (255, 100, 15)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 90

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        if self.x + self.vx < 800 - self.r:
            self.x += self.vx
        else:
            self.vx *= -1
        if self.y - self.vy < 500 - self.r:
            self.y -= self.vy
        else:
            self.vy *= -0.6
            self.vx *= 0.6
        self.vy -= 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r,
            1
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.x = 20
        self.y = 450
        self.color = BLACK

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0]-20 != 0:
                self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
            elif event.pos[1] >= 450:
                self.an = math.pi * 3 / 2
            else:
                self.an = math.pi / 2
        if self.f2_on:
            self.color = ORANGE
        else:
            self.color = BLACK

    def draw(self):
        # FIXIT don't know how to do it
        pygame.draw.polygon(self.screen, self.color, (
            (self.x + 5 * math.cos(self.an + math.pi * (3 / 4)), self.y + 5 * math.sin(self.an + math.pi * (3 / 4))),
            (self.x + 5 * math.cos(self.an + math.pi * (5 / 4)), self.y + 5 * math.sin(self.an + math.pi * (5 / 4))),
            (self.x + ((25 / 2 + (self.f2_power ** 2) / 2) ** 0.5) * math.cos(self.an - math.atan(5 / self.f2_power)),
             self.y + ((25 / 2 + (self.f2_power ** 2) / 2) ** 0.5) * math.sin(self.an - math.atan(5 / self.f2_power))),
            (self.x + ((25 / 2 + (self.f2_power ** 2) / 2) ** 0.5) * math.cos(self.an + math.atan(5 / self.f2_power)),
             self.y + ((25 / 2 + (self.f2_power ** 2) / 2) ** 0.5) * math.sin(self.an + math.atan(5 / self.f2_power))),
        ), 0)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 60:
                self.f2_power += 1
            self.color = ORANGE
        else:
            self.color = BLACK


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self, screen: pygame.Surface):
        """ Инициализация новой цели. """
        self.points = 0
        self.new_target()
        self.screen = screen

        color = self.color = RED

    def new_target(self):
        self.x = rnd(600, 750)
        self.y = rnd(100, 450)
        self.r = rnd(5, 50)
        rand = random.random()
        self.v = (rand + 1) * ((rand - 0.5) / abs(rand - 0.5))

    def move(self):
        if 500 - self.r > self.y + self.v > self.r:
            self.y += self.v
        else:
            self.v *= -1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r,
            1
        )


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
shots = 0
balls = []
font = pygame.font.Font(None, 20)
target_spawn_delay = 0

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
target2 = Target(screen)
finished = False

while not finished:
    score_text = font.render(str(target.points + target2.points), True, BLACK)
    screen.fill(WHITE)
    gun.draw()
    screen.blit(score_text, (10, 15))
    if target_spawn_delay == 0:
        target.draw()
        target2.draw()
    else:
        screen.blit(delay_text, (280, 300))
        target_spawn_delay -= 1
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
            shots += 1
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        b.live -= 1
        if b.live <= 0:
            balls.remove(b)
        if b.hittest(target) and target_spawn_delay == 0:
            target.hit()
            target_spawn_delay = 90
            delay_text = font.render("Вы уничтожили цель за " + str(shots) + " выстрелов", True, BLACK)
            shots = 0
            target.new_target()
        if b.hittest(target2) and target_spawn_delay == 0:
            target2.hit()
            target_spawn_delay = 90
            delay_text = font.render("Вы уничтожили цель за " + str(shots) + " выстрелов", True, BLACK)
            shots = 0
            target2.new_target()
    if target_spawn_delay == 0:
        target.move()
        target2.move()
    gun.power_up()

pygame.quit()
