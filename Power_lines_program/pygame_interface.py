import pygame as pg
from pygame.display import set_caption
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
    dist = np.linalg.norm(np.array(mouse) - np.array(position) + np.array((step * active_unit, 0)))
    print(dist, np.array(np.array(mouse) - np.array(position) + np.array((step * active_unit, 0))))
    if dist > 20:
        pg.draw.circle(display, (0, 155, 255), (position[0] + step * active_unit, position[1]), 5)
    else:
        pg.draw.circle(display, TURQUOISE, (position[0] + step * active_unit, position[1]), 10)
        if LKM:
            if 1 <= (mouse[0] - position[0]) // step <= units:
                variable = (mouse[0] - position[0]) // step
    return variable


# Параметры графики и графические константы
FPS = 60
height = 600
width = 1024

GRAY = (30, 30, 30)
RED = (240, 48, 61)
BLUE = (48, 128, 245)
WHITE = (255, 255, 255)
TURQUOISE = (0, 255, 255)

pg.init()
display = pg.display.set_mode((width, height))
set_caption('Моделирование элетростатического поля')
display.fill(GRAY)

clock = pg.time.Clock()
play = True
mouse = pg.mouse.get_pos()
LKM = False
q = 2
q = slider(display, (900, 50), 100, 50, q, mouse, LKM, q)
pg.display.update()

while play:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            play = False
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                LKM = True
    display.fill(GRAY)
    mouse = pg.mouse.get_pos()
    q = slider(display, (900, 50), 100, 50, 1, mouse, LKM, q)
    clock.tick(FPS)
    pg.display.update()
