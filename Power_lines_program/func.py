import numpy as np


def tension_calculation(sign_k, q, x, y, x_k1, y_k1, e_x, e_y):
    e_x = (e_x +
           sign_k * q * (x_k1 - x) / (
                   ((x_k1 - x) ** 2 + (y_k1 - y) ** 2) ** (3 / 2))
           )

    e_y = (e_y +
           sign_k * q * (y_k1 - y) / (
                   ((x_k1 - x) ** 2 + (y_k1 - y) ** 2) ** (3 / 2))
           )

    return e_x, e_y


def point_calculation(x_k1, y_k1, e_x, e_y, i):
    sin = (e_y / (e_y ** 2 + e_x ** 2) ** (1 / 2))
    cos = (e_x / (e_y ** 2 + e_x ** 2) ** (1 / 2))
    tg = e_y / e_x

    if ((abs(tg) <= 1) and (sin >= 0) and (cos >= 0)) or \
            ((abs(tg) <= 1) and (sin <= 0) and (cos >= 0)):
        dx = 0.01
        dy = tg * dx
        x_k1 = x_k1 + dx
        y_k1 = y_k1 + dy
    elif abs(tg) <= 1:
        dx = -0.01
        dy = tg * dx
        x_k1 = x_k1 + dx
        y_k1 = y_k1 + dy
    elif ((abs(tg) > 1) and (sin >= 0) and (cos >= 0)) or \
            ((abs(tg) > 1) and (sin >= 0) and (cos <= 0)):
        dy = 0.01
        dx = (1 / tg) * dy
        x_k1 = x_k1 + dx
        y_k1 = y_k1 + dy
    else:
        dy = -0.01
        dx = (1 / tg) * dy
        x_k1 = x_k1 + dx
        y_k1 = y_k1 + dy

    i = i + 1

    return x_k1, y_k1, i


def power_lines(n, x_list, y_list, q_list, sign_list):
    ax = np.array([], dtype=np.float64)
    ay = np.array([], dtype=np.float64)
    ax_list = np.array([], dtype=np.float64)
    ay_list = np.array([], dtype=np.float64)
    R = 0.01

    for k in range(0, n):

        x_k = x_list[k]
        y_k = y_list[k]
        sign_k = sign_list[k]

        ax_list = np.append(ax_list, ax)
        ay_list = np.append(ay_list, ay)

        ax = np.array([], dtype=np.float64)
        ay = np.array([], dtype=np.float64)

        for l in range(0, 12):

            x_k1 = x_k + R * np.cos(2 * np.pi * l / 12)
            y_k1 = y_k + R * np.sin(2 * np.pi * l / 12)

            ax = np.append(ax, np.nan)
            ay = np.append(ay, np.nan)

            ax = np.append(ax, x_k)
            ax = np.append(ax, x_k1)
            ay = np.append(ay, y_k)
            ay = np.append(ay, y_k1)

            distance = np.array([10], dtype=np.float64)
            d_dot_mid = ((x_k1 - sum(x_list) / n) ** 2 + (y_k1 - sum(y_list) / n) ** 2) ** (1 / 2)
            for m in range(0, n):

                if (m != l) and (n != 1):
                    d = ((x_k1 - x_list[m]) ** 2 + (y_k1 - y_list[m]) ** 2) ** (1 / 2)
                    distance = np.append(distance, d)
                    if k == 0:
                        max_d = 3 * np.max(distance)

            i = 0

            while (round(np.min(distance), 3) >= 0.01) and \
                    (max_d > d_dot_mid) and (i <= 1000):

                E_x = 0
                E_y = 0

                try:
                    for o in range(0, n):
                        q_o = q_list[o]
                        x_o = x_list[o]
                        y_o = y_list[o]

                        E_x, E_y = tension_calculation(sign_k, q_o, x_o, y_o, x_k1, y_k1, E_x, E_y)

                    x_k1, y_k1, i = point_calculation(x_k1, y_k1, E_x, E_y, i)

                    ax = np.append(ax, x_k1)
                    ay = np.append(ay, y_k1)

                    d_dot_mid = ((x_k1 - sum(x_list) / n) ** 2 + (y_k1 - sum(y_list) / n) ** 2) ** (1 / 2)
                    for s in range(0, n):

                        if s != l:
                            d = ((x_k1 - x_list[s]) ** 2 + (y_k1 - y_list[s]) ** 2) ** (1 / 2)
                            distance = np.append(distance, d)

                except OverflowError:
                    pass

    ax_list = np.append(ax_list, ax)
    ay_list = np.append(ay_list, ay)
    return ax_list, ay_list
