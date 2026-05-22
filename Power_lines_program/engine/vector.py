import numpy as np
import pygame as pg

def vec(display, start, end, color, vec_size=10):
    pg.draw.aaline(display, color, start, end)

    if end[0] != start[0]:
        angle = np.arctan((end[1]-start[1])/(end[0]-start[0]))

        pg.draw.aaline(display, color, end,
        [end[0] - np.sign(end[0] - start[0]) * vec_size * np.cos(np.pi / 6 - angle),
                end[1] + np.sign(end[0] - start[0]) *  vec_size * np.sin(np.pi / 6 - angle)], 3)
        pg.draw.aaline(display, color, end,
        [end[0] - np.sign(end[0] - start[0]) * vec_size * np.cos(np.pi / 6 + angle),
                end[1] - np.sign(end[0] - start[0]) * vec_size * np.sin(np.pi / 6 + angle)], 3)
    else:
        pg.draw.aaline(display, color, end,
                          [end[0] - vec_size * np.sin(np.pi / 6),
                           end[1] - np.sign(end[1] - start[1]) * vec_size * np.cos(np.pi / 6)], 3)
        pg.draw.aaline(display, color, end,
                           [end[0] + vec_size * np.sin(np.pi / 6),
                            end[1] - np.sign(end[1] - start[1]) * vec_size * np.cos(np.pi / 6)], 3)