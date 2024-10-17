import numpy as np


def power_lines(n, x_list, y_list, q_list, sign_list):

    ax = []
    ay = []
    ax_list = []
    ay_list = []
    R = 0.01

    for k in range(0, n):

        x_k = x_list[k]
        y_k = y_list[k]
        sign_k = sign_list[k]

        ax_list.append(ax)
        ay_list.append(ay)

        ax = []
        ay = []

        for l in range(0, 12):

            x_k1 = x_k + R * np.cos(2 * np.pi * l / 12)
            y_k1 = y_k + R * np.sin(2 * np.pi * l / 12)

            ax.append(np.nan)
            ay.append(np.nan)

            ax.append(x_k)
            ax.append(x_k1)
            ay.append(y_k)
            ay.append(y_k1)

            distance = list([10])
            d_dot_mid = ((x_k1 - sum(x_list) / n) ** 2 + (y_k1 - sum(y_list) / n) ** 2) ** (1 / 2)
            for m in range(0, n):

                if (m != l) and (n != 1):
                    d = ((x_k1 - x_list[m]) ** 2 + (y_k1 - y_list[m]) ** 2) ** (1 / 2)
                    distance.append(d)
                    if k == 0:
                        max_d = 3 * max(distance)

            i = 0

            while (round(min(distance), 3) >= 0.01) and \
                    (max_d > d_dot_mid) and (i <= 1000):
                E_x = 0
                E_y = 0

                try:
                    for o in range(0, n):
                        E_x = (E_x +
                               sign_k * q_list[o] * (x_k1 - x_list[o]) / (
                                       ((x_k1 - x_list[o]) ** 2 + (y_k1 - y_list[o]) ** 2) ** (3 / 2))
                               )

                        E_y = (E_y +
                               sign_k * q_list[o] * (y_k1 - y_list[o]) / (
                                       ((x_k1 - x_list[o]) ** 2 + (y_k1 - y_list[o]) ** 2) ** (3 / 2))
                               )

                    sin = (E_y / (E_y ** 2 + E_x ** 2) ** (1 / 2))
                    cos = (E_x / (E_y ** 2 + E_x ** 2) ** (1 / 2))
                    tg = E_y / E_x

                    if ((abs(tg) <= 1) and (sin >= 0) and (cos >= 0)) or \
                            ((abs(tg) <= 1) and (sin <= 0) and (cos >= 0)):
                        dx = 0.01
                        dy = (E_y / E_x) * dx
                        x_k1 = x_k1 + dx
                        y_k1 = y_k1 + dy
                    elif abs(tg) <= 1:
                        dx = -0.01
                        dy = (E_y / E_x) * dx
                        x_k1 = x_k1 + dx
                        y_k1 = y_k1 + dy
                    elif ((abs(tg) > 1) and (sin >= 0) and (cos >= 0)) or \
                            ((abs(tg) > 1) and (sin >= 0) and (cos <= 0)):
                        dy = 0.01
                        dx = (E_x / E_y) * dy
                        x_k1 = x_k1 + dx
                        y_k1 = y_k1 + dy
                    else:
                        dy = -0.01
                        dx = (E_x / E_y) * dy
                        x_k1 = x_k1 + dx
                        y_k1 = y_k1 + dy

                    i = i + 1

                    ax.append(x_k1)
                    ay.append(y_k1)

                    d_dot_mid = ((x_k1 - sum(x_list) / n) ** 2 + (y_k1 - sum(y_list) / n) ** 2) ** (1 / 2)
                    for s in range(0, n):

                        if s != l:
                            d = ((x_k1 - x_list[s]) ** 2 + (y_k1 - y_list[s]) ** 2) ** (1 / 2)
                            distance.append(d)

                except OverflowError:
                    pass

    ax_list.append(ax)
    ay_list.append(ay)

    return ax_list, ay_list
