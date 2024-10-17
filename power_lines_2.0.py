import numpy as np
import matplotlib.pyplot as plt

plt.ion()

n = int(input("Введите количество зарядов"))

x_list = []
y_list = []
q_list = []
c_list = []
sign_list = []

ax = []
ay = []

R = 0.01


for i in range(0, n):
    x = float(input(f"Введите координату x {i + 1}-го заряда"))
    y = float(input(f"Введите координату y {i + 1}-го заряда"))
    q = float(input(f"Введите величину q {i + 1}-го заряда"))

    if q > 0:
        c = "r"
        sign = 1
    else:
        c = "b"
        sign = -1

    x_list.append(x)
    y_list.append(y)
    q_list.append(q)
    c_list.append(c)
    sign_list.append(sign)

for k in range(0, len(x_list)):

    x_k = x_list[k]
    y_k = y_list[k]
    q_k = q_list[k]
    z = sign_list[k]

    for l in range(0, 4):

        x_k1 = x_k + R * np.cos(2 * np.pi * l / 4)
        y_k1 = y_k + R * np.sin(2 * np.pi * l / 4)

        dx = 0
        dy = 0

        ax = ax + list(reversed(ax))
        ay = ay + list(reversed(ay))

        ax.append(x_k)
        ax.append(x_k1)
        ay.append(y_k)
        ay.append(y_k1)

        i = 0

        distance = list([1000])

        for m in range(0, len(x_list)):

            if m != l:
                d = ((x_k1 - x_list[m])**2 + (y_k1 - y_list[m])**2)**(1/2)
                distance.append(d)
            else:
                print("Работаем_1", distance)

        while (min(distance) >= 0.01) and \
              (i <= 250):
            E_x = 0
            E_y = 0

            for o in range(0, len(q_list)):
                E_x = (E_x +
                       z * q_list[o] * (x_k1 - x_list[o]) / (((x_k1 - x_list[o]) ** 2 + (y_k1 - y_list[o]) ** 2) ** (3 / 2))
                       )

                E_y = (E_y +
                       z * q_list[o] * (y_k1 - y_list[o]) / (((x_k1 - x_list[o]) ** 2 + (y_k1 - y_list[o]) ** 2) ** (3 / 2))
                       )
                print(E_x, E_y)
                print(y_k1, y_list[0])

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
            elif ((abs(tg) >= 1) and (sin > 0) and (cos > 0)) or \
                    ((abs(tg) >= 1) and (sin > 0) and (cos < 0)):
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

            plt.clf()
            plt.plot(ax, ay)
            plt.scatter(x_list, y_list, s=100, c=c_list)
            plt.draw()
            plt.gcf().canvas.flush_events()

            for s in range(0, len(x_list)):

                if s != l:
                    d = ((x_k1 - x_list[s]) ** 2 + (y_k1 - y_list[s]) ** 2) ** (1 / 2)
                    distance.append(d)
                else:
                    print("Работаем_2")

            print(distance)


plt.ioff()
plt.show()








