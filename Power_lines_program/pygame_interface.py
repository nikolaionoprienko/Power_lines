import pygame as pg
from mpl_toolkits.mplot3d.proj3d import transform
from pygame import RESIZABLE, Surface, FULLSCREEN
from pygame.display import set_caption, is_fullscreen
import numpy as np
from func import power_lines


class Сharges:
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
number_of_lines = 12

GRAY = (60, 63, 65)
DARK_GRAY = (43, 43, 43)
RED = (240, 48, 61)
BLUE = (48, 128, 245)
WHITE = (255, 255, 255)
TURQUOISE = (0, 255, 255)

pg.init()

display = pg.display.set_mode((width, height), RESIZABLE)
virtual_display = Surface((width, height))
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
q = 1
q = slider(virtual_display, (900, 50), 100, 10, q, mouse, LKM, q)

pg.display.update()

while play:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            play = False
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                LKM = True
        if i.type == pg.MOUSEBUTTONUP:
            if i.button == 1:
                LKM = False
        if i.type == pg.VIDEORESIZE:
            current_size = i.size
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

    virtual_display.fill(GRAY)
    mouse = pg.mouse.get_pos()
    print(mouse)
    q = slider(virtual_display,  (330,  470), 260, 20, q, mouse, LKM, q)
    number_of_lines = slider(virtual_display, (330, 400), 260, 20, number_of_lines, mouse,
                             LKM, number_of_lines)

    scaled_display = pg.transform.scale(virtual_display, current_size)
    display.blit(scaled_display, (0, 0))

    clock.tick(FPS)
    pg.display.update()
