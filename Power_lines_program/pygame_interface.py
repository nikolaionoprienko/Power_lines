import pygame as pg
from mpl_toolkits.mplot3d.proj3d import transform
from pygame import RESIZABLE, Surface, FULLSCREEN
from pygame.display import set_caption, is_fullscreen
import numpy as np
from func import power_lines

pg.init()

class Сharge:
    q = None
    x_q = None
    y_q = None
    color_q = None
    size = None

    def __init__(self, q, x_q, y_q, color_q, size):
        self.q = q
        self.x_q = x_q
        self.y_q = y_q
        self.color_q = color_q
        self.size = size

q = 1

def slider(display, position, slider_len, units, active_unit, mouse, LKM, variable):
    pg.draw.line(display, WHITE, position, (position[0] + slider_len, position[1]), 3)
    step = slider_len // units
    dist = np.linalg.norm(np.array(mouse) - np.array(position) - np.array((step * active_unit, 0)))
    if dist > 2 * step:
        pg.draw.circle(display, (0, 155, 255), (position[0] + step * active_unit, position[1]), 5)
    else:
        pg.draw.circle(display, TURQUOISE, (position[0] + step * active_unit, position[1]), 10)
        if LKM:
            if 1 <= (mouse[0] - position[0]) // step <= units:
                variable = (mouse[0] - position[0]) // step
    return variable


# Параметры графики и графические константы
FPS = 60
height = 720
width = 1280
height_field = 670
width_field = 860
number_of_lines = 12
number_of_iterations = 1

GRAY = (60, 63, 65)
DARK_GRAY = (43, 43, 43)
RED = (240, 48, 61)
BLUE = (48, 128, 245)
WHITE = (255, 255, 255)
TURQUOISE = (0, 255, 255)

f1 = pg.font.Font('cmunrm.ttf', 20)
f2 = pg.font.Font('cmunrm.ttf', 24)
f3 = pg.font.Font('cmunrm.ttf', 22)
string_0 = f1.render('Управление: ', True, WHITE)
string_1 = f1.render('Добавить положительный заряд: ЛКМ', True, WHITE)
string_2 = f1.render('Добавить отрицательный заряд: ПКМ', True, WHITE)
string_3 = f1.render('Очистить экран от зарядов: ESC', True, WHITE)
string_4 = f1.render('Развернуть на полный экран: F', True, WHITE)
string_5 = f2.render('Модуль заряда', True, WHITE)
string_6 = f3.render('Количество линий на заряд', True, WHITE)
string_7 = f3.render('Шаг моделирования', True, WHITE)

# Поверхности и их настройки
display = pg.display.set_mode((width, height), RESIZABLE)
virtual_display = Surface((width, height))
field = Surface((width_field, height_field))
field_rect = field.get_rect(topleft=(25, 25))

current_size = display.get_size()
info = pg.display.Info()
FULLSCREEN_SIZE = (info.current_w, info.current_h)
last_size = current_size
set_caption('Моделирование электростатического поля')
virtual_display.fill(GRAY)

clock = pg.time.Clock()
play = True
mouse = pg.mouse.get_pos()
LKM = False

pg.display.update()

while play:

    field.fill(DARK_GRAY)

    # Обработка событий
    for i in pg.event.get():

        # Выход из программы
        if i.type == pg.QUIT:
            play = False

        # События мыши
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                LKM = True

        if i.type == pg.MOUSEBUTTONUP:
            if i.button == 1:
                LKM = False
            if field_rect.collidepoint(mouse):
                if i.button == 1:
                    pg.draw.circle(field, RED, mouse, q * 10)
                    print(True)

        # События изменения размеров окна
        if i.type == pg.VIDEORESIZE:
            current_size = i.size

        # События клавиатуры
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_f:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    last_size = current_size
                    current_size = FULLSCREEN_SIZE
                    display = pg.display.set_mode(current_size, FULLSCREEN)
                else:
                    current_size = last_size
                    display = pg.display.set_mode(current_size, RESIZABLE)

    mouse = pg.mouse.get_pos()


    virtual_display.fill(GRAY)
    virtual_display.blit(field, (25, 25))
    virtual_display.blit(string_0, (905, 40))
    virtual_display.blit(string_1, (905, 65))
    virtual_display.blit(string_2, (905, 90))
    virtual_display.blit(string_3, (905, 115))
    virtual_display.blit(string_4, (905, 140))
    virtual_display.blit(string_5, (970, 195))
    virtual_display.blit(string_6, (918, 263))
    virtual_display.blit(string_7, (955, 330))

    string_8 = f3.render(str(q), True, TURQUOISE)
    string_9 = f3.render(str(number_of_lines), True, TURQUOISE)
    string_10 = f3.render(str(number_of_iterations), True, TURQUOISE)
    virtual_display.blit(string_8, (1200, 220))
    virtual_display.blit(string_9, (1200, 285))
    virtual_display.blit(string_10, (1200, 351))


    pg.draw.rect(virtual_display, WHITE, (25, 25, 860, 670), 3)

    scaled_display = pg.transform.scale(virtual_display, current_size)
    display.blit(scaled_display, (0, 0))

    # Слайдеры

    scal_x = current_size[0] / width
    scal_y = current_size[1] / height

    q = slider(display, [scal_x * 925, scal_y * 235], scal_x * 255, 20, q, mouse, LKM, q)

    number_of_lines = slider(display, [scal_x * 925, scal_y * 300], scal_x * 255, 20, number_of_lines, mouse,
                             LKM, number_of_lines)
    number_of_iterations = slider(display, [scal_x * 925, scal_y * 365], scal_x * 255, 20, number_of_iterations, mouse,
                             LKM, number_of_iterations)

    clock.tick(FPS)
    pg.display.update()
