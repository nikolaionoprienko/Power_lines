import numpy as np
from numba import jit, prange

# одна силовая линия
@jit(fastmath=True, nopython=True, cache=True)
def tension(number_of_iterations, x_list, y_list, q_list, sign_list,
            distance_sqrt, ax, ay, k, x, y):

    i = 0

    while np.amin(distance_sqrt) >= 1 and \
            i < number_of_iterations:

        E_x = sign_list[k] * np.sum(
                (q_list * (x - x_list)) / (distance_sqrt ** 3))
        E_y = sign_list[k] * np.sum(
                (q_list * (y - y_list)) / (distance_sqrt ** 3))

        if E_x != 0:
            tg = E_y/E_x
        else:
            tg = 10*6

        if abs(tg) <= 1:
            dx = np.sign(E_x) * 2
            x = x + dx
            y = y + tg * dx

        else:
            dy = np.sign(E_y) * 2
            x = x + (1 / tg) * dy
            y = y + dy

        ax[i + 2] = x
        ay[i + 2] = y

        distance_sqrt = ((x_list - x) ** 2 + (y_list - y) ** 2) ** (1 / 2)

        i = i + 1

    return ax, ay


# электрическое поле всех зарядов
def power_lines(number_of_lines, number_of_iterations, n, x_list, y_list, q_list, sign_list):

    segments = np.full((number_of_lines * n + n, number_of_iterations + 2, 2), np.nan, dtype=np.float64)
    R = 2
    iteration = -1

    for k in range(n):
        iteration += 1
        for l in range(number_of_lines):

            ax = np.full(number_of_iterations + 2, np.nan, dtype=np.float64)
            ay = np.full(number_of_iterations + 2, np.nan, dtype=np.float64)

            x = x_list[k] + R * np.cos(2 * np.pi * l / number_of_lines)
            y = y_list[k] + R * np.sin(2 * np.pi * l / number_of_lines)

            ax[0] = x_list[k]
            ay[0] = y_list[k]
            ax[1] = x
            ay[1] = y

            distance_sqrt = ((x_list - x) ** 2 + (y_list - y) ** 2) ** (1 / 2)

            ax, ay = tension(number_of_iterations, x_list, y_list, q_list, sign_list,
                             distance_sqrt, ax, ay, k, x, y)

            segments[iteration] = np.column_stack((ax, ay))

            iteration += 1

    return segments


# Движение всех зарядов
def movement(n, x_list, y_list, q_list, m_list, vx_list, vy_list, t):

    acceleration_x_list = np.zeros((n))
    acceleration_y_list = np.zeros((n))
    dt = 1/60

    for k in range(n):
        mask = np.arange(n) != k
        dist32 = ((x_list[mask] - x_list[k]) ** 2 + (y_list[mask] - y_list[k]) ** 2) ** (3 / 2)
        acceleration_x = ((-9 * q_list[k]) / m_list[k]) * np.sum((q_list[mask] * (x_list[mask] - x_list[k])) / dist32)
        acceleration_y = ((-9 * q_list[k]) / m_list[k]) * np.sum((q_list[mask] * (y_list[mask] - y_list[k])) / dist32)
        acceleration_x_list[k] = acceleration_x
        acceleration_y_list[k] = acceleration_y

    x_list = x_list + (vx_list * dt + acceleration_x_list * dt**2 / 2) * 1000
    y_list = y_list + (vy_list * dt + acceleration_y_list * dt**2 / 2) * 1000
    vx_list = vx_list + acceleration_x_list * dt
    vy_list = vy_list + acceleration_y_list * dt
    t = t + dt

    return x_list, y_list, vx_list, vy_list, t