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


class Particle:
    def __init__(self, screen: pygame.Surface, life, x, y, color):
        self.x = x
        self.y = y
        self.screen = screen
        self.life = life
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.life)


class Ball:
    def __init__(self, screen: pygame.Surface, x, y, type):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.min_y = y + 12
        self.r = 2
        self.vx = 0
        self.vy = 0
        self.color = BLACK
        self.live = 30
        self.type = type

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        if self.type == 1:
            self.x += self.vx

            if self.y - self.vy < self.min_y - self.r:
                self.y -= self.vy
            else:
                self.vy *= -0.6
                self.vx *= 0.6
            self.vy -= 1
        else:
            self.x += self.vx
            self.y += self.vy
            self.vx *= 1.03
            self.vy *= 1.03

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
    def __init__(self, screen: pygame.Surface, x, y):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.x = x
        self.y = y
        self.color = BLACK

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event, proj_type):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        new_ball = Ball(self.screen, self.x + 30*math.cos(self.an), self.y + 30*math.sin(self.an), proj_type)
        new_ball.r += 5
        if proj_type == 1:
            new_ball.vx = self.f2_power * math.cos(self.an)
            new_ball.vy = - self.f2_power * math.sin(self.an)
        else:
            new_ball.vx = 2 * math.cos(self.an)
            new_ball.vy = 2 * math.sin(self.an)
            new_ball.live = 300
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, x, y):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if x-self.x > 0:
                self.an = math.atan((y-self.y) / (x-self.x))
            elif x-self.x < 0:
                self.an = math.atan((y - self.y) / (x - self.x)) + math.pi
            elif y >= self.y:
                self.an = math.pi / 2
            else:
                self.an = math.pi * 3 / 2
        if self.f2_on:
            self.color = ORANGE
        else:
            self.color = BLACK

    def draw(self):
        # FIXIT don't know how to do it
        draw_an = self.an
        pygame.draw.polygon(self.screen, self.color, (
            (self.x + 5 * math.cos(draw_an + math.pi * (3 / 4)), self.y + 5 * math.sin(draw_an + math.pi * (3 / 4))),
            (self.x + 5 * math.cos(draw_an + math.pi * (5 / 4)), self.y + 5 * math.sin(draw_an + math.pi * (5 / 4))),
            (self.x + ((25 / 2 + (self.f2_power ** 2) / 2) ** 0.5) * math.cos(draw_an - math.atan(5 / self.f2_power)),
             self.y + ((25 / 2 + (self.f2_power ** 2) / 2) ** 0.5) * math.sin(draw_an - math.atan(5 / self.f2_power))),
            (self.x + ((25 / 2 + (self.f2_power ** 2) / 2) ** 0.5) * math.cos(draw_an + math.atan(5 / self.f2_power)),
             self.y + ((25 / 2 + (self.f2_power ** 2) / 2) ** 0.5) * math.sin(draw_an + math.atan(5 / self.f2_power))),
        ), 0)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 30:
                self.f2_power += 1
            self.color = ORANGE
        else:
            self.color = BLACK


class Tank:
    def __init__(self, screen: pygame.Surface, color, x, y):
        self.screen = screen
        self.gun = Gun(screen, x, y)
        self.x = x
        self.y = y
        self.an = 0
        self.color = color
        self.fwd_spd = 1.6
        self.trn_spd = (1/36) * math.pi
        self.health = 3
        self.proj_type = 1

    def draw(self):
        d_an = math.atan(0.5)
        diag = 500**0.5
        p1 = (self.x + diag*math.cos(self.an + d_an), self.y + diag*math.sin(self.an + d_an))
        p2 = (self.x + diag * math.cos(self.an - d_an + math.pi), self.y + diag*math.sin(self.an - d_an + math.pi))
        p3 = (self.x + diag * math.cos(self.an + d_an + math.pi), self.y + diag*math.sin(self.an + d_an + math.pi))
        p4 = (self.x + diag * math.cos(self.an - d_an), self.y + diag*math.sin(self.an - d_an))
        pygame.draw.polygon(self.screen, self.color, (p1, p2, p3, p4), 2)
        self.gun.draw()

    def move(self, fwd, turn):
        new_x = self.x + self.fwd_spd * math.cos(self.an) * fwd
        new_y = self.y + self.fwd_spd * math.sin(self.an) * fwd

        self.an += self.trn_spd * turn
        if self.an > math.pi * 2:
            self.an -= math.pi * 2
        elif self.an < 0:
            self.an += math.pi * 2

        if 500**0.5 < new_x < 800 - 500**0.5:
            self.x = new_x
            self.gun.x = new_x
        if 300 + 500**0.5 < new_y < 600 - 500**0.5:
            self.y = new_y
            self.gun.y = new_y

        self.gun.targetting(last_mouse_pos[0], last_mouse_pos[1])


class Bomb:
    def __init__(self, screen: pygame.Surface, x, y, v_0):
        self.x = x
        self.screen = screen
        self.y = y
        self.v_x = v_0
        self.v_y = 0
        if v_0 >= 0:
            self.an = 0
        else:
            self.an = math.pi

    def draw(self):
        diag = 250 ** 0.5
        d_an = math.atan(1/3)
        p1 = (self.x + 20 * math.cos(self.an), self.y + 20 * math.sin(self.an))
        p2 = (self.x + diag * math.cos(self.an + d_an), self.y + diag * math.sin(self.an + d_an))
        p3 = (self.x + diag * math.cos(self.an - d_an + math.pi), self.y + diag * math.sin(self.an - d_an + math.pi))
        p4 = (self.x + diag * math.cos(self.an + d_an + math.pi), self.y + diag * math.sin(self.an + d_an + math.pi))
        p5 = (self.x + diag * math.cos(self.an - d_an), self.y + diag * math.sin(self.an - d_an))
        pygame.draw.polygon(self.screen, BLACK, (p1, p2, p3, p4, p5), 2)

    def move(self):
        self.x += self.v_x
        self.y -= self.v_y

        self.v_y -= 0.05
        if self.v_x < 0:
            self.an = -math.atan(self.v_y / self.v_x) + math.pi
        else:
            self.an = -math.atan(self.v_y / self.v_x)


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self, screen: pygame.Surface, type, color):
        """ Инициализация новой цели. """
        self.points = 0
        self.type = type
        self.new_target()
        self.screen = screen
        self.color = color

    def new_target(self):
        self.x = rnd(50, 750)
        self.y = rnd(50, 150)
        self.r = rnd(5, 50)
        self.bmb_delay = rnd(60, 120)
        self.cur_bmb_delay = 120
        rand = random.random()
        if self.type == 1:
            self.vx = (rand + 1) * ((rand - 0.5) / abs(rand - 0.5))
        else:
            self.vx = 0
        self.vy = 0

    def move(self):
        if self.type == 1:
            if 800 - self.r > self.x + self.vx > self.r:
                self.x += self.vx
            else:
                self.vx *= -1
        else:
            if 800 - self.r > self.x + self.vx > self.r:
                self.x += self.vx
            else:
                self.vx *= -1
            if 200 - self.r > self.y + self.vy > self.r:
                self.y += self.vy
            else:
                self.vy *= -1

            self.vx += 0.4*random.random() - 0.2
            self.vy += 0.4 * random.random() - 0.2

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
balls = []
bombs = []
particles = []
font = pygame.font.Font(None, 20)
font_small = pygame.font.Font(None, 16)
target_spawn_delay = 0

last_mouse_pos = (0, 0)
vertical_axis = 0
horizontal_axis = 0
clock = pygame.time.Clock()
tank1 = Tank(screen, (150, 0, 0), 30, 450)
tank2 = Tank(screen, (0, 0, 150), 770, 450)
tank1_respawn_time = 0
tank2_respawn_time = 0
target = Target(screen, 1, RED)
target2 = Target(screen, 2, RED)
finished = False
selected_tank = tank1
cv1, cv2, cv3 = 4, -5, 4.5
c = [255, 0, 0]
health_text = font.render("Здоровье:", True, BLACK)
tank2_respawn_text = font.render("Танк 2 был уничтожен!", True, BLACK)
tank1_respawn_text = font.render("Танк 1 был уничтожен!", True, BLACK)
tank_selection_text = font.render("Выбор танка:", True, BLACK)
shell_selection_text = font.render("Выбор снаряда:", True, BLACK)
tank1_choise_text = font.render("Танк 1", True, BLACK)
tank2_choise_text = font.render("Танк 2", True, BLACK)
AP_shell_choise_text_1 = font_small.render("Броне-", True, BLACK)
AP_shell_choise_text_2 = font_small.render("-бойный", True, BLACK)
rocket_choise_text = font_small.render("Ракета", True, BLACK)

while not finished:
    # ======================= ОТРИСОВКА =======================
    if 1 <= c[0] + cv1 < 256:
        c[0] += cv1
    else:
        cv1 *= -1
    if 1 <= c[1] + cv2 < 256:
        c[1] += cv2
    else:
        cv2 *= -1
    if 1 <= c[2] + cv3 < 256:
        c[2] += cv3
    else:
        cv3 *= -1
    target2.color = (c[0], c[1], c[2])
    score_text = font.render(str(target.points + target2.points), True, BLACK)
    screen.fill(WHITE)
    pygame.draw.rect(screen, (170, 255, 170), (0, 300, 800, 300), 0)
    pygame.draw.rect(screen, (170, 190, 255), (0, 0, 800, 300), 0)

    if tank1_respawn_time == 0 and tank2_respawn_time == 0:
        tank1.draw()
        tank2.draw()
    else:
        if tank1_respawn_time > 0:
            tank1_respawn_time -= 1
            screen.blit(tank1_respawn_text, (350, 300))
        if tank2_respawn_time > 0:
            tank2_respawn_time -= 1
            screen.blit(tank2_respawn_text, (350, 300))

    if tank1_respawn_time == 0:
        for b in balls:
            b.draw()

    for b in bombs:
        b.draw()
    target.draw()
    target2.draw()

    for p in particles:
        p.draw()
        p.life -= 0.3
        if p.life < 0:
            particles.remove(p)

    pygame.draw.rect(screen, BLACK, (10, 45, 60, 10), 1)
    pygame.draw.rect(screen, RED, (11, 46, 20 * selected_tank.health - 2, 8), 0)

    pygame.draw.rect(screen, BLACK, (10, 500, 50, 50), 1)
    pygame.draw.rect(screen, BLACK, (60, 500, 50, 50), 1)
    if selected_tank == tank1:
        pygame.draw.rect(screen, ORANGE, (11, 501, 48, 48), 0)
        pygame.draw.rect(screen, WHITE, (61, 501, 48, 48), 0)
    else:
        pygame.draw.rect(screen, WHITE, (11, 501, 48, 48), 0)
        pygame.draw.rect(screen, ORANGE, (61, 501, 48, 48), 0)

    pygame.draw.rect(screen, BLACK, (120, 500, 50, 50), 1)
    pygame.draw.rect(screen, BLACK, (170, 500, 50, 50), 1)
    if selected_tank.proj_type == 1:
        pygame.draw.rect(screen, ORANGE, (121, 501, 48, 48), 0)
        pygame.draw.rect(screen, WHITE, (171, 501, 48, 48), 0)
    else:
        pygame.draw.rect(screen, WHITE, (121, 501, 48, 48), 0)
        pygame.draw.rect(screen, ORANGE, (171, 501, 48, 48), 0)

    screen.blit(health_text, (10, 30))
    screen.blit(score_text, (10, 15))
    screen.blit(tank_selection_text, (10, 485))
    screen.blit(shell_selection_text, (120, 485))
    screen.blit(tank1_choise_text, (15, 517))
    screen.blit(tank2_choise_text, (65, 517))
    screen.blit(AP_shell_choise_text_1, (121, 513))
    screen.blit(AP_shell_choise_text_2, (121, 527))
    screen.blit(rocket_choise_text, (177, 517))

    pygame.display.update()

    clock.tick(FPS)
    # ======================= ОБРАБОТКА ЭВЕНТОВ =======================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 10 <= event.pos[0] <= 60 and 500 <= event.pos[1] <= 550 and selected_tank == tank2:
                selected_tank = tank1
            elif 60 <= event.pos[0] <= 110 and 500 <= event.pos[1] <= 550  and selected_tank == tank1:
                selected_tank = tank2

            if 120 <= event.pos[0] <= 170 and 500 <= event.pos[1] <= 550 and selected_tank.proj_type == 2:
                selected_tank.proj_type = 1
            elif 170 <= event.pos[0] <= 220 and 500 <= event.pos[1] <= 550  and selected_tank.proj_type == 1:
                selected_tank.proj_type = 2

            if tank2_respawn_time + tank1_respawn_time == 0:
                selected_tank.gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if tank2_respawn_time + tank1_respawn_time == 0:
                selected_tank.gun.fire2_end(event, selected_tank.proj_type)
        elif event.type == pygame.MOUSEMOTION:
            selected_tank.gun.targetting(event.pos[0], event.pos[1])
            last_mouse_pos = (event.pos[0], event.pos[1])

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                vertical_axis += 1
            if event.key == pygame.K_s:
                vertical_axis -= 1
            if event.key == pygame.K_d:
                horizontal_axis += 1
            if event.key == pygame.K_a:
                horizontal_axis -= 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                vertical_axis -= 1
            if event.key == pygame.K_s:
                vertical_axis += 1
            if event.key == pygame.K_d:
                horizontal_axis -= 1
            if event.key == pygame.K_a:
                horizontal_axis += 1

    # ======================= ДВИЖЕНИЕ ОБЪЕКТОВ =======================
    for b in balls:
        b.move()
        if b.vx + b.vy < 0.5 and b.y > 300:
            b.live -= 1
        if b.live <= 0:
            balls.remove(b)
        if b.hittest(target):
            target.hit()
            shots = 0
            target.new_target()
            balls.remove(b)
        if b.hittest(target2):
            target2.hit()
            shots = 0
            target2.new_target()
            if balls.__contains__(b):
                balls.remove(b)
        if (b.x - tank1.x)**2 + (b.y - tank1.y)**2 < (b.r + 500**0.5)**2 and balls.__contains__(b):
            balls.remove(b)
            tank1.health -= 1
        if (b.x - tank2.x)**2 + (b.y - tank2.y)**2 < (b.r + 500**0.5)**2 and balls.__contains__(b):
            balls.remove(b)
            tank2.health -= 1
        if b.type == 2:
            particles.append(Particle(screen, random.randint(4, 7), b.x + 6*random.random() - 3, b.y + 6*random.random() - 3, GREY))

    for b in bombs:
        b.move()
        if b.y > 620 and bombs.__contains__(b):
            bombs.remove(b)
        if abs(b.y - tank1.y) < 35 and abs(b.x - tank1.x) < 25 and tank2_respawn_time + tank1_respawn_time == 0:
            tank1.health -= 1
            bombs.remove(b)
        if abs(b.y - tank2.y) < 35 and abs(b.x - tank2.x) < 25 and tank2_respawn_time + tank1_respawn_time == 0:
            tank2.health -= 1
            bombs.remove(b)

    if tank1.health == 0:
        tank1.health = 3
        tank1.x = 30
        tank1.y = 450
        tank1.gun.x = 30
        tank1.gun.y = 450
        tank1.an = 0
        tank1_respawn_time = 120

    if tank2.health == 0:
        tank2.health = 3
        tank2.x = 770
        tank2.y = 450
        tank2.gun.x = 770
        tank2.gun.y = 450
        tank2.an = 0
        tank2_respawn_time = 120

    if target.cur_bmb_delay > 0:
        target.cur_bmb_delay -= 1
    else:
        bombs.append(Bomb(screen, target.x, target.y, target.vx))
        target.cur_bmb_delay = target.bmb_delay

    if target2.cur_bmb_delay > 0:
        target2.cur_bmb_delay -= 1
    else:
        bombs.append(Bomb(screen, target2.x, target2.y, target2.vx))
        target2.cur_bmb_delay = target2.bmb_delay

    target.move()
    target2.move()

    if tank1_respawn_time == 0 and tank2_respawn_time == 0:
        selected_tank.move(vertical_axis, horizontal_axis)
        selected_tank.gun.power_up()

pygame.quit()
