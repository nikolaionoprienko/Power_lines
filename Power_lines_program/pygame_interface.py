import pygame as pg
from pygame import RESIZABLE, Surface, FULLSCREEN
from pygame.display import set_caption, is_fullscreen
import numpy as np
from func_for_pg import power_lines


pg.init()

x_list = np.array(())
y_list = np.array(())
q_list = np.array(())
sign_list = np.array(())
s_list = []
c_list = []

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
number_of_iterations = 1000

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

    display.fill(GRAY)

    # Обработка событий
    for i in pg.event.get():

        # Выход из программы
        if i.type == pg.QUIT:
            play = False

        # События мыши
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                LKM = True
            if field_rect.collidepoint(mouse):
                if i.button == 1:
                    x_list = np.append(x_list, mouse[0] - scal_x * 25)
                    y_list = np.append(y_list, mouse[1] - scal_y * 25)
                    q_list = np.append(q_list, q)
                    sign_list = np.append(sign_list, 1)
                    s_list.append(q * 4)
                    c_list.append(RED)
                if i.button == 3:
                    x_list = np.append(x_list, mouse[0] - scal_x * 25)
                    y_list = np.append(y_list, mouse[1] - scal_y * 25)
                    q_list = np.append(q_list, -1 * q)
                    sign_list = np.append(sign_list, -1)
                    s_list.append(q * 4)
                    c_list.append(BLUE)

        if i.type == pg.MOUSEBUTTONUP:
            if i.button == 1:
                LKM = False




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
            if i.key == pg.K_ESCAPE:
                x_list = np.array(())
                y_list = np.array(())
                q_list = np.array(())
                sign_list = np.array(())
                s_list = []
                c_list = []


    mouse = pg.mouse.get_pos()

    # Отображение текстов
    virtual_display.fill(GRAY)
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

    # Отображение на дисплей других элементов
    scal_x = current_size[0] / width
    scal_y = current_size[1] / height

    pg.draw.rect(virtual_display, WHITE, (20, 20, 870, 680), 7)
    field = pg.transform.scale(field, (width_field * scal_x, height_field * scal_y))
    scaled_display = pg.transform.scale(virtual_display, current_size)
    display.blit(scaled_display, (0, 0))
    display.blit(field, (25 * scal_x, 25 * scal_y))
    field_rect = field.get_rect(topleft=(25 * scal_x, 25 * scal_y))
    field.fill(DARK_GRAY)


    # Слайдеры
    q = slider(display, [scal_x * 925, scal_y * 235], scal_x * 255, 20, q, mouse, LKM, q)

    number_of_lines = int(slider(display, [scal_x * 925, scal_y * 300], scal_x * 255, 20, number_of_lines, mouse,
                             LKM, number_of_lines))
    number_of_iterations = int(slider(display, [scal_x * 925, scal_y * 365], scal_x * 255, 20, number_of_iterations//1000, mouse,
                             LKM, number_of_iterations/1000) * 1000)

    # Отображение зарядов и линий
    for i in range(len(q_list)):
        pg.draw.circle(field, c_list[i], [x_list[i], y_list[i]], s_list[i])
        pg.draw.circle(field, WHITE, [x_list[i], y_list[i]], s_list[i], 2)

    n = len(q_list)
    x_list = np.array(x_list)
    y_list = np.array(y_list)
    q_list = np.array(q_list)
    sign_list = np.array(sign_list)
    x_mid, y_mid = 0, 0
    max_distance = 10000
    ax, ay = power_lines(number_of_lines, number_of_iterations, n, x_list, y_list, q_list, sign_list,
                x_mid, y_mid, max_distance)

    points = np.column_stack((ax, ay))
    points = points[~np.isnan(points).any(axis=1)]


    if points.shape[0] >= 2:
            pg.draw.aalines(field, TURQUOISE, False, points)



    clock.tick(FPS)
    pg.display.update()
