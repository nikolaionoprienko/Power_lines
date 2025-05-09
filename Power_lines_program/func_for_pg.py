import numpy as np
from numba import jit, prange


@jit(fastmath=True, nopython=True)
def tension(number_of_iterations, x_list, y_list, q_list, sign_list,
            x_mid, y_mid, max_distance, distance_sqr, distance_point_mid_sqr, ax, ay, k, x, y, l):

    i = 0

    while np.amin(distance_sqr) >= 1 and \
            i <= number_of_iterations:

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
        distance_point_mid_sqr = ((x_mid - x) ** 2 + (y_mid - y) ** 2) ** (1 / 2)

        i = i + 1

    return ax, ay



def power_lines(number_of_lines, number_of_iterations, n, x_list, y_list, q_list, sign_list,
                x_mid, y_mid, max_distance):

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
            distance_point_mid_sqr = ((x_mid - x) ** 2 + (y_mid - y) ** 2) ** 2

            ax, ay = tension(number_of_iterations, x_list, y_list, q_list, sign_list,
                             x_mid, y_mid, max_distance, distance_sqr, distance_point_mid_sqr, ax, ay, k, x, y, l)

            segments[iteration] = np.column_stack((ax, ay))

            iteration += 1

    return segments
