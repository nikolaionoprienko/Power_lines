import numpy as np
from numba import jit, prange
import time


@jit(fastmath=True, nopython=True)
def tension(number_of_iterations, x_list, y_list, q_list, sign_list,
            x_mid, y_mid, max_distance, distance_sqr, distance_point_mid_sqr, i, ax, ay, k, x, y, l):

    while (np.round(np.amin(distance_sqr), 3) >= 0.001) and \
            (distance_point_mid_sqr <= max_distance) and \
            (i <= number_of_iterations):

        # with objmode(start='f8'):
        #     start = time.perf_counter()

        # Пропуск любых возможных ошибок
        try:
            E_x = sign_list[k] * np.sum(
                (q_list * (x - x_list)) / (((x - x_list) ** 2 + (y - y_list) ** 2) ** (3 / 2)))
            E_y = sign_list[k] * np.sum(
                (q_list * (y - y_list)) / (((x - x_list) ** 2 + (y - y_list) ** 2) ** (3 / 2)))

            tg = E_y/E_x

            if abs(tg) <= 1:
                dx = np.sign(E_x) * 0.01
                x = x + dx
                y = y + tg * dx

            else:
                dy = np.sign(E_y) * 0.01
                x = x + (1 / tg) * dy
                y = y + dy
        except:
            pass

        # with objmode(time_if='f8'):
        #     time_if = time_if + time.perf_counter() - start

        # with objmode(start='f8'):
        #     start = time.perf_counter()

        index = 2 * number_of_iterations * l + 2 + i

        ax[index] = x
        ay[index] = y

        distance_sqr = ((x_list - x) ** 2 + (y_list - y) ** 2) ** (1 / 2)
        distance_point_mid_sqr = ((x_mid - x) ** 2 + (y_mid - y) ** 2) ** (1 / 2)

        i = i + 1

        # with objmode(time_ind='f8'):
        #     time_ind = time_ind + time.perf_counter() - start

    return ax, ay
        # , time_E, time_if, time_ind


def power_lines(number_of_lines, number_of_iterations, n, x_list, y_list, q_list, sign_list,
                x_mid, y_mid, max_distance):
    ax = np.full(2 * number_of_iterations, np.nan, dtype=np.float64)
    ay = np.full(2 * number_of_iterations, np.nan, dtype=np.float64)

    ax_list = np.full(2 * number_of_lines * number_of_iterations * (n + 1), np.nan, dtype=np.float64)
    ay_list = np.full(2 * number_of_lines * number_of_iterations * (n + 1), np.nan, dtype=np.float64)

    # time_E, time_if, time_ind = 0, 0, 0

    R = 0.01
    time_f = 0
    for k in prange(n):

        for_slice = 2 * number_of_lines * number_of_iterations * k
        ax_list[for_slice:(for_slice + np.size(ax))] = ax
        ay_list[(2 * number_of_lines * number_of_iterations * k):(for_slice + np.size(ay))] = ay

        ax = np.full(2 * number_of_iterations * number_of_lines, np.nan, dtype=np.float64)
        ay = np.full(2 * number_of_iterations * number_of_lines, np.nan, dtype=np.float64)

        for l in prange(number_of_lines):
            ax[2 * number_of_iterations * l] = np.nan
            ay[2 * number_of_iterations * l] = np.nan

            x = x_list[k] + R * np.cos(2 * np.pi * l / number_of_lines)
            y = y_list[k] + R * np.sin(2 * np.pi * l / number_of_lines)

            ax[2 * number_of_iterations * l + 1] = x_list[k]
            ay[2 * number_of_iterations * l + 1] = y_list[k]
            ax[2 * number_of_iterations * l + 2] = x
            ay[2 * number_of_iterations * l + 2] = y

            distance_sqr = ((x_list - x) ** 2 + (y_list - y) ** 2) ** (1 / 2)
            distance_point_mid_sqr = ((x_mid - x) ** 2 + (y_mid - y) ** 2) ** 2

            i = 0

            start = time.time()
            ax, ay = tension(number_of_iterations, x_list, y_list, q_list, sign_list,
                             x_mid, y_mid, max_distance, distance_sqr, distance_point_mid_sqr, i, ax, ay, k, x, y, l)
            end = time.time()
            time_f = time_f + (end - start)

    for_slice = 2 * number_of_lines * number_of_iterations * n
    ax_list[for_slice:(for_slice + np.size(ax))] = ax
    ay_list[for_slice:(for_slice + np.size(ax))] = ay
    print(time_f)

    # print(time_E)
    # print(time_if)
    # print(time_ind)

    return ax_list, ay_list
