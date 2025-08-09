import pygame as pg
from pygame import RESIZABLE, Surface, FULLSCREEN
from pygame.display import set_caption, is_fullscreen
import numpy as np
from func_for_pg import power_lines, movement, button, vec, slider

# предварительное создание некоторых "физических" констант
x_list = np.array(())
y_list = np.array(())
q_list = np.array(())
m_list = np.array(())
vx_list = np.array(())
vy_list = np.array(())
sign_list = np.array(())
s_list = []
c_list = []
power_lines_simulation = True
movement_simulation = True
LKM_ONE = False

q = 10
m = 100
t = 0

# Инициализация пай гейм
pg.init()

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

f1 = pg.font.Font(size=22)
f2 = pg.font.Font(size=30)
f3 = pg.font.Font(size=28)

# Инструкция в интерфейсе
string_0 = f1.render('Управление: ', True, WHITE)
string_1 = f1.render('Добавить положительный заряд: ЛКМ', True, WHITE)
string_2 = f1.render('Добавить отрицательный заряд: ПКМ', True, WHITE)
string_3 = f1.render('Очистить экран от зарядов: ESC', True, WHITE)
string_4 = f1.render('Развернуть на полный экран: F', True, WHITE)
string_5 = f2.render('Модуль заряда', True, WHITE)
string_5_5 = f2.render('Масса', True, WHITE)
string_6 = f3.render('Количество линий на заряд', True, WHITE)
string_7 = f3.render('Количество итераций', True, WHITE)

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
PKM = False

# инициализация функции моделирования электрического поля для быстрого её запуска пользователем
segments = power_lines(number_of_lines, number_of_iterations, 1, np.array([457.]), np.array([366.]), np.array([10.]), np.array([1.]))

pg.display.update()


# Основной цикл (Прорисовка каждого кадра)
while play:

    display.fill(GRAY)

    # Обработка событий
    for i in pg.event.get():

        # Выход из программы
        if i.type == pg.QUIT:
            play = False

        # События мыши:
        # Нажатия клавиши мыши
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                LKM = True
                LKM_ONE = True
            if field_rect.collidepoint(mouse):
                if i.button == 1:
                    # Добавление положительного заряда
                    x_list = np.append(x_list, mouse[0] - scal_x * 25)
                    y_list = np.append(y_list, mouse[1] - scal_y * 25)
                    q_list = np.append(q_list, q)
                    m_list = np.append(m_list, m)
                    sign_list = np.append(sign_list, 1)
                    s_list.append(m/100 + 6)
                    c_list.append((q + 155, 48, 68))

                    # Начало вектора начальной скорости
                    mouse_start = np.array(mouse)

                if i.button == 3:
                    # Добавление отрицательного заряда
                    x_list = np.append(x_list, mouse[0] - scal_x * 25)
                    y_list = np.append(y_list, mouse[1] - scal_y * 25)
                    q_list = np.append(q_list, -1 * q)
                    m_list = np.append(m_list, m)
                    sign_list = np.append(sign_list, -1)
                    s_list.append(m/100 + 6)
                    c_list.append((28, 48, q + 155))

                    PKM = True
                    # Начало вектора начальной скорости
                    mouse_start = np.array(mouse)

        # Отпускание клавиши мыши
        # Создание координаты конца вектора скорости и добавление модуля скорости заряда
        if i.type == pg.MOUSEBUTTONUP:
            if i.button == 1:
                LKM = False
                end_arrow = np.array(mouse)
                if field_rect.collidepoint(mouse):
                    try:
                        vx_list = np.append(vx_list, ((mouse - np.array(mouse_start))[0])/1000)
                        vy_list = np.append(vy_list, ((mouse - np.array(mouse_start))[1])/1000)
                    except:
                        pass
            if i.button == 3:
                PKM = False
                if field_rect.collidepoint(mouse):
                    try:
                        vx_list = np.append(vx_list, ((mouse - np.array(mouse_start))[0])/1000)
                        vy_list = np.append(vy_list, ((mouse - np.array(mouse_start))[1])/1000)
                    except:
                        pass


        # События изменения размеров окна
        if i.type == pg.VIDEORESIZE:
            current_size = i.size

        # События клавиатуры
        if i.type == pg.KEYDOWN:
            # Полноэкранный режим
            if i.key == pg.K_f:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    last_size = current_size
                    current_size = FULLSCREEN_SIZE
                    display = pg.display.set_mode(current_size, FULLSCREEN)
                else:
                    current_size = last_size
                    display = pg.display.set_mode(current_size, RESIZABLE)
            # Удаление всех зарядов
            if i.key == pg.K_ESCAPE:
                x_list = np.array(())
                y_list = np.array(())
                q_list = np.array(())
                m_list = np.array(())
                vx_list = np.array(())
                vy_list = np.array(())
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
    virtual_display.blit(string_5_5, (1020, 263))
    virtual_display.blit(string_6, (918, 330))
    virtual_display.blit(string_7, (950, 397))

    string_8 = f1.render(str(q) + ' мкКл', True, TURQUOISE)
    string_8_8 = f1.render(str(m) + ' г', True, TURQUOISE)
    string_9 = f1.render(str(number_of_lines), True, TURQUOISE)
    string_10 = f1.render(str(number_of_iterations), True, TURQUOISE)
    virtual_display.blit(string_8, (1200, 220))
    virtual_display.blit(string_8_8, (1200, 285))
    virtual_display.blit(string_9, (1200, 351))
    virtual_display.blit(string_10, (1200, 417))

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
    q = slider(display, [scal_x * 925, scal_y * 235], scal_x * 255, 50, q/2, mouse, LKM, q/2, 5) * 2

    m = round(slider(display, [scal_x * 925, scal_y * 300], scal_x * 255, 250, m/4, mouse, LKM, m/4, 20) * 4, 1)

    number_of_lines = int(slider(display, [scal_x * 925, scal_y * 365], scal_x * 255, 20, number_of_lines, mouse,
                             LKM, number_of_lines, 2))
    number_of_iterations = int(slider(display, [scal_x * 925, scal_y * 430], scal_x * 255, 20, number_of_iterations//200, mouse,
                             LKM, number_of_iterations/200, 2) * 200)

    # Кнопки
    button_1 = button(display, (scal_x * 925, scal_y * 480), scal_x * 255, scal_y * 25, power_lines_simulation, LKM_ONE, 'Симуляция электрического поля')
    power_lines_simulation = button_1

    button_2 = button(display, (scal_x * 925, scal_y * 510), scal_x * 255, scal_y * 25, movement_simulation, LKM_ONE,
                     'Симуляция движения')
    movement_simulation = button_2

    # Отображение векторов скорости, линий электрического поля и зарядов
    n = len(q_list)
    x_list = np.array(x_list)
    y_list = np.array(y_list)
    q_list = np.array(q_list)
    m_list = np.array(m_list)
    sign_list = np.array(sign_list)

    # Отображение моделирования электрического поля
    if power_lines_simulation:
        segments = power_lines(number_of_lines, number_of_iterations, n, x_list, y_list, q_list, sign_list)
        if segments.shape[0] >= 2:
            for segment in segments:
                pg.draw.aalines(field, TURQUOISE, False, segment)

    # Отображения зарядов
    for i in range(len(q_list)):
        pg.draw.circle(field, c_list[i], [x_list[i], y_list[i]], s_list[i])
        pg.draw.circle(field, WHITE, [x_list[i], y_list[i]], s_list[i], 2)

    # Отображение вектора
    if (LKM or PKM) and field_rect.collidepoint(mouse):
        try:
            vec(field, np.array(mouse_start) - np.array([25 * scal_x, 25 * scal_y]), mouse - np.array([25 * scal_x, 25 * scal_y]), WHITE, vec_size=10)
        except:
            pass
    # Моделирование движения зарядов
    elif movement_simulation:
        x_list, y_list, vx_list, vy_list, t = movement(n, x_list, y_list, q_list, m_list, vx_list, vy_list, t)
        time = f1.render(str(round(t, 1)) + ' c', True, DARK_GRAY, WHITE)
        field.blit(time, (5, 5))

    LKM_ONE = False
    clock.tick(FPS)
    pg.display.update()
