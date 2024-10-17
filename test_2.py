import numpy as np
import matplotlib.pyplot as plt
import time


plt.ion()

n = int(input("Введите количество зарядов"))

x_list = []
y_list = []
q_list = []
c_list = []
sign_list = []
s_list = []

ax = []
ay = []

R = 0.01

for i in range(0, n):
    x = float(input(f"Введите координату x {i + 1}-го заряда"))
    y = float(input(f"Введите координату y {i + 1}-го заряда"))
    q = float(input(f"Введите величину q {i + 1}-го заряда"))

    if q > 0:
        c = (0.94, 0.19, 0.24)
        sign = 1
    else:
        c = (0.19, 0.5, 0.96)
        sign = -1

    s = abs(q) * 40

    x_list.append(x)
    y_list.append(y)
    q_list.append(q)
    c_list.append(c)
    sign_list.append(sign)
    s_list.append(s)

start = time.time()

fig = plt.figure(figsize=(7, 7), facecolor="#3c3f41")
axis = fig.add_subplot()
axis.set(facecolor="#2b2b2b")
fig.suptitle("Численное моделирование электрического поля точечных зарядов", c="w")
plt.xlabel("Ox, м", c="w")
plt.ylabel("Oy, м", c="w")
axis.spines['bottom'].set_color("w")
axis.spines['top'].set_color("w")
axis.spines['left'].set_color("w")
axis.spines['right'].set_color("w")
axis.tick_params(colors='w')

for k in range(0, n):

    x_k = x_list[k]
    y_k = y_list[k]
    q_k = q_list[k]
    z = sign_list[k]
    max_d = 4

    axis.scatter(x_list, y_list, s=s_list, c=c_list, zorder=1)
    axis.plot(ax, ay, linewidth=0.5, c="#00ffff7f", zorder=-1)
    plt.draw()
    plt.gcf().canvas.flush_events()

    ax = []
    ay = []

    for l in range(0, 9):

        x_k1 = x_k + R * np.cos(2 * np.pi * l / 9)
        y_k1 = y_k + R * np.sin(2 * np.pi * l / 9)

        dx = 0
        dy = 0

        ax = ax + list(reversed(ax))
        ay = ay + list(reversed(ay))

        ax.append(x_k)
        ax.append(x_k1)
        ay.append(y_k)
        ay.append(y_k1)

        i = 0

        distance = list([0.01])
        for m in range(0, n):

            if m != l:
                d = ((x_k1 - x_list[m]) ** 2 + (y_k1 - y_list[m]) ** 2) ** (1 / 2)
                distance.append(d)
                if k == 0:
                    max_d = 4 * max(distance)

        while (round(min(distance), 5) >= 0.01) and \
                (max_d > max(distance)) and (i <= 1000):
            E_x = 0
            E_y = 0

            for o in range(0, n):
                E_x = (E_x +
                       z * q_list[o] * (x_k1 - x_list[o]) / (
                                   ((x_k1 - x_list[o]) ** 2 + (y_k1 - y_list[o]) ** 2) ** (3 / 2))
                       )

                E_y = (E_y +
                       z * q_list[o] * (y_k1 - y_list[o]) / (
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
            for s in range(0, n):

                if s != l:
                    d = ((x_k1 - x_list[s]) ** 2 + (y_k1 - y_list[s]) ** 2) ** (1 / 2)
                    distance.append(d)

axis.plot(ax, ay, linewidth=0.5, c="#00ffff7f", zorder=-1)
axis.scatter(x_list, y_list, s=s_list, c=c_list, linewidths=0.4, edgecolors="w", zorder=1)
plt.ioff()

end = time.time()
print(end - start)

plt.show()
