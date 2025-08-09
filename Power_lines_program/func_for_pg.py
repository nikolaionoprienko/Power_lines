import numpy as np
from numba import jit, prange
import pygame as pg

# физические функции:

# одна силовая линия
@jit(fastmath=True, nopython=True, cache=True)
def tension(number_of_iterations, x_list, y_list, q_list, sign_list,
            distance_sqr, ax, ay, k, x, y, l):

    i = 0

    while np.amin(distance_sqr) >= 1 and \
            i < number_of_iterations:

        try:
            E_x = sign_list[k] * np.sum(
                (q_list * (x - x_list)) / (((x - x_list) ** 2 + (y - y_list) ** 2) ** (3 / 2)))
            E_y = sign_list[k] * np.sum(
                (q_list * (y - y_list)) / (((x - x_list) ** 2 + (y - y_list) ** 2) ** (3 / 2)))

            tg = E_y/E_x

            if abs(tg) <= 1:
                dx = np.sign(E_x) * 2
                x = x + dx
                y = y + tg * dx

            else:
                dy = np.sign(E_y) * 2
                x = x + (1 / tg) * dy
                y = y + dy
        except:
            pass

        ax[i + 2] = x
        ay[i + 2] = y

        distance_sqr = ((x_list - x) ** 2 + (y_list - y) ** 2) ** (1 / 2)

        i = i + 1

    return ax, ay


# электрическое поле всех зарядов
def power_lines(number_of_lines, number_of_iterations, n, x_list, y_list, q_list, sign_list):

    segments = np.full((number_of_lines * n + n, number_of_iterations + 2, 2), np.nan, dtype=np.float64)
    R = 2
    iteration = -1

    for k in prange(n):
        iteration += 1
        for l in prange(number_of_lines):

            ax = np.full(number_of_iterations + 2, np.nan, dtype=np.float64)
            ay = np.full(number_of_iterations + 2, np.nan, dtype=np.float64)

            x = x_list[k] + R * np.cos(2 * np.pi * l / number_of_lines)
            y = y_list[k] + R * np.sin(2 * np.pi * l / number_of_lines)

            ax[0] = x_list[k]
            ay[0] = y_list[k]
            ax[1] = x
            ay[1] = y

            distance_sqr = ((x_list - x) ** 2 + (y_list - y) ** 2) ** (1 / 2)

            ax, ay = tension(number_of_iterations, x_list, y_list, q_list, sign_list,
                             distance_sqr, ax, ay, k, x, y, l)

            segments[iteration] = np.column_stack((ax, ay))

            iteration += 1

    return segments


# Движение всех зарядов
def movement(n, x_list, y_list, q_list, m_list,vx_list, vy_list, t):

    # Считаем, что q - в мкКл, масса в г. Таким образом коэффициент в законе Кулона будет численно равен 9

    acceleration_x_list = np.array(())
    acceleration_y_list = np.array(())
    dt = 1/60

    for k in range(n):

        q_list_not_k = np.delete(q_list, k)
        x_list_not_k = np.delete(x_list, k)
        y_list_not_k = np.delete(y_list, k)

        acceleration_x = ((-9 * q_list[k]) / m_list[k]) * np.sum((q_list_not_k * (x_list_not_k - x_list[k])) / (
                    ((x_list_not_k - x_list[k]) ** 2 + (y_list_not_k - y_list[k]) ** 2) ** (3 / 2)))

        acceleration_y = ((-9 * q_list[k]) / m_list[k]) * np.sum((q_list_not_k * (y_list_not_k - y_list[k])) / (
                    ((x_list_not_k - x_list[k]) ** 2 + (y_list_not_k - y_list[k]) ** 2) ** (3 / 2)))

        acceleration_x_list = np.append(acceleration_x_list, acceleration_x)
        acceleration_y_list = np.append(acceleration_y_list, acceleration_y)

    x_list = x_list + (vx_list * dt + acceleration_x_list * dt**2 / 2) * 1000
    y_list = y_list + (vy_list * dt + acceleration_y_list * dt**2 / 2) * 1000

    vx_list = vx_list + acceleration_x_list * dt
    vy_list = vy_list + acceleration_y_list * dt

    t = t + dt

    return x_list, y_list, vx_list, vy_list, t


#Графические функции:


#Кнопка
def button(display, pos, width, height, var, LKM, buttonText=' '):
    fillColors = {
        'normal': (240, 48, 61),
        'hover': var * np.array([100, 163, 102]) + (not var) * np.array([163, 100, 100]),
        'pressed': (63, 204, 68)
    }
    mousePos = pg.mouse.get_pos()
    buttonSurface = pg.Surface((width, height))
    buttonRect = pg.Rect(pos[0], pos[1], width, height)
    font = pg.font.Font(size=22)
    buttonSurf = font.render(buttonText, True, (255, 255, 255))

    if var:
        buttonSurface.fill(fillColors['pressed'])
    else:
        buttonSurface.fill(fillColors['normal'])

    if buttonRect.collidepoint(mousePos):
        buttonSurface.fill(fillColors['hover'])
        if LKM:
            if var:
                var = False
                buttonSurface.fill(fillColors['normal'])
            else:
                var = True
                buttonSurface.fill(fillColors['pressed'])

    buttonSurface.blit(buttonSurf, [
        buttonRect.width / 2 - buttonSurf.get_rect().width / 2,
        buttonRect.height / 2 - buttonSurf.get_rect().height / 2
    ])
    display.blit(buttonSurface, buttonRect)
    pg.draw.rect(display, (255, 255, 255), (pos[0], pos[1], width, height), 2)
    return var

# cлайдeр / ползунок
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

# вектор
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




