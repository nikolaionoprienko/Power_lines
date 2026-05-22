import numpy as np
import pygame as pg

def slider(display, position, slider_len, units, active_unit, mouse, LKM, variable, dist_mouse):
    pg.draw.line(display, (255, 255, 255), position, (position[0] + slider_len, position[1]), 3)
    step = slider_len // units
    dist = np.linalg.norm(np.array(mouse) - np.array(position) - np.array((step * active_unit, 0)))
    if dist > dist_mouse * step:
        pg.draw.circle(display, (0, 155, 255), (position[0] + step * active_unit, position[1]), 5)
    else:
        pg.draw.circle(display, (0, 255, 255), (position[0] + step * active_unit, position[1]), 10)
        if LKM:
            if 1 <= (mouse[0] - position[0]) // step <= units:
                variable = (mouse[0] - position[0]) // step
    return variable