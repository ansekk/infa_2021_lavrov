# Импорт библиотек
import pygame
from pygame.draw import *
from random import randint
from random import random

# Инициализация
pygame.init()

FPS = 60
screen = pygame.display.set_mode((1200, 600))

# Задаем цвета
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, WHITE]


# Задаем функции
def __func_sort(x):
    """Функция для сортировки таблицы счета, для внутреннего использования"""
    return -int(x[1])


def new_ball():
    """Создает новый шарик и возвращает массив с данными о нем в таком виде:
    [x центра, y центра, радиус, цвет, скорость по x, скорость по y,
    время существования, "цена" в очках, тип объекта]"""
    x = randint(100, 1100)
    y = randint(100, 500)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    vel_x = (random() * 2 - 1) * 3
    vel_y = (random() * 2 - 1) * 3
    lifetime = 360 + randint(-300, 300)
    value = round((12 - lifetime / 60) // 2 + (6 - r // 20))
    obj_type = "ball"
    return [x, y, r, color, vel_x, vel_y, lifetime, value, obj_type]


def new_square():
    """Создает новый квадрат и возвращает массив с данными о нем в таком виде:
    [x центра, y центра, половина длины стороны, цвет, скорость по x, скорость по y,
    время существования, "цена" в очках, тип объекта]"""
    x = randint(50, 1150)
    y = randint(50, 550)
    edge_len = randint(20, 40)
    color = COLORS[randint(0, 5)]
    vel_x = (random() + 4)
    vel_y = (random() + 4)
    if random() > 0.5:
        vel_x *= -1
    if random() > 0.5:
        vel_y *= -1
    lifetime = 660 + randint(-300, 300)
    value = round((12 - (lifetime - 300) / 60) + (6 - (edge_len * 2) // 10) + 100)
    obj_type = "square"
    return [x, y, edge_len / 2, color, vel_x, vel_y, lifetime, value, obj_type]


# Продолжение инициализации (первый апдейт экрана, создание счетчика времени, создание стандартного шрифта)
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)
# Логические переменые для перехода между меню
finished = False
start_menu = True
viewing_scoreboard = False

# Импорт таблицы счета из файла
scoreboard_f = open("scoreboard.txt", 'r')
scoreboard = []
for line in scoreboard_f:
    current = line.split()
    scoreboard.append([current[0], current[1]])

# Задаем переменные для игры
obj_list = []
plr_name = "player"
obj_spawn_delay = 0
score = 0
alphabet = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z',
            'x', 'c','v', 'b', 'n', 'm']

# Главный цикл
while not finished:
    clock.tick(FPS)

    # Стартовое меню
    if start_menu:

        rect(screen, WHITE, (0, 500, 1200, 100))
        write_your_name_text = font.render("Write your name:", True, [255, 255, 255])
        plr_name_text = font.render(plr_name, True, [255, 255, 255])
        confirm_text = font.render("Confirm", True, [0, 0, 0])
        screen.blit(write_your_name_text, (520, 200))
        screen.blit(plr_name_text, (580 - 4 * len(plr_name), 230))
        screen.blit(confirm_text, (550, 545))

        # Обработка событий (в т.ч. ввод имени)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(event.key)
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if event.pos[1] > 500:
                    start_menu = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and len(plr_name) > 0:
                plr_name = plr_name[:len(plr_name) - 1]
            elif event.type == pygame.KEYDOWN and 96 < event.key < 123:
                plr_name += chr(event.key)

    # Финальное меню со счетом
    elif viewing_scoreboard:
        scoreboard_text_arr = []
        for i in range(len(scoreboard)):
            cur_scoreboard_str = scoreboard[i][0] + "  " + str(scoreboard[i][1])
            cur_scoreboard_line = font.render(cur_scoreboard_str, True, [255, 255, 255])
            screen.blit(cur_scoreboard_line, (580 - 4 * len(cur_scoreboard_str), 10 + 15 * i))

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

    # Меню игры
    else:
        # Создание новых объектов
        if obj_spawn_delay == 0:
            if random() > 0.1:
                obj_list.append(new_ball())
            else:
                obj_list.append(new_square())
            obj_spawn_delay = randint(30, 90)
        else:
            obj_spawn_delay -= 1

        # Передвижение объектов и их рендеринг
        for obj in obj_list:
            if obj[8] == "square":
                obj[5] += 0.5

            if not (1200 - obj[2] > obj[0] + obj[4] > obj[2]):
                obj[4] *= -1
            obj[0] += obj[4]
            if not (600 - obj[2] > obj[1] + obj[5] > obj[2]):
                obj[5] *= -1
            obj[1] += obj[5]

            if obj[6] < 0:
                obj_list.remove(obj)
            else:
                obj[6] -= 1

            if obj[8] == "ball":
                circle(screen, obj[3], (obj[0], obj[1]), obj[2])
            else:
                rect(screen, obj[3], (obj[0] - obj[2], obj[1] - obj[2], 2 * obj[2], 2 * obj[2]))

        # Обработка эвентов
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            # Проверка на попадание по шарику
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]

                hit_something = False
                for obj in obj_list:
                    if obj[8] == "ball":
                        if ((obj[0] - mouse_x) ** 2 + (obj[1] - mouse_y) ** 2) ** 0.5 < obj[2]:
                            score += obj[7]
                            obj_list.remove(obj)
                            hit_something = True
                    else:
                        if abs(obj[0] - mouse_x) < obj[2] and abs(obj[1] - mouse_y) < obj[2]:
                            score += obj[7]
                            obj_list.remove(obj)
                            hit_something = True

                if not hit_something:
                    score -= 10
            # Проверка нажатия escape
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                viewing_scoreboard = True

        # Отрисовка текста
        score_text = font.render("Your score: " + str(score), True, [255, 255, 255])
        exit_text = font.render("Press escape to finish game and view scoreboard", True, [255, 255, 255])
        screen.blit(score_text, (10, 10))
        screen.blit(exit_text, (10, 25))

    # Обновление экрана
    pygame.display.update()
    screen.fill(BLACK)

# Добавление текущего счета в таблицу, ее сортировка и запись в файл, выход из программы
scoreboard.append([plr_name, str(score)])
scoreboard.sort(key=__func_sort)
scoreboard_f = open("scoreboard.txt", 'w')
for item in scoreboard:
    scoreboard_f.write(" ".join(item) + '\n')
pygame.quit()
