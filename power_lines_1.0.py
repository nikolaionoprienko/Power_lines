import numpy as np
import matplotlib.pyplot as plt
import time


x_1 = float(input("Координата x_1: "))
y_1 = float(input("Координата y_1: "))
q_1 = float(input("Заряд q_1"))
if q_1 > 0:
    color_1 = "r"
else:
    color_1 = "b"

x_2 = float(input("Координата x_2: "))
y_2 = float(input("Координата y_2: "))
q_2 = float(input("Заряд q_2"))
if q_2 > 0:
    color_2 = "r"
else:
    color_2 = "b"

R = 0.01

plt.ion()

list_x = []
list_y = []

for k in range(0, 10):
    x = x_1 + R * np.cos(2 * np.pi * k / 9)
    y = y_1 + R * np.sin(2 * np.pi * k / 9)
    dx = 0
    dy = 0
    list_x = list_x + list(reversed(list_x))
    list_y = list_y + list(reversed(list_y))
    list_x.append(x_1)
    list_x.append(x)
    list_y.append(y_1)
    list_y.append(y)
    i = 0
    while (((x - x_2) ** 2 + (y - y_2) ** 2) > R**2) \
            and (i <= 250) \
            and ((x-(x_2+x_1)/2)**2 + (x-(x_2+x_1)/2)**2) <= 4*(x_1 - x_2)**2:

        x = x + dx
        y = y + dy
        plt.clf()
        plt.plot(list_x, list_y)
        plt.scatter(x_1, y_1, s=100, c=color_1)
        plt.scatter(x_2, y_2, s=100, c=color_2)
        plt.draw()
        plt.gcf().canvas.flush_events()

        E_x = (q_1 * (x - x_1) / (((x - x_1) ** 2 + (y - y_1) ** 2) ** (3 / 2)) +
               q_2 * (x - x_2) / (((x - x_2) ** 2 + (y - y_2) ** 2) ** (3 / 2))
               )
        E_y = (q_1 * (y - y_1) / (((x - x_1) ** 2 + (y - y_1) ** 2) ** (3 / 2)) +
               q_2 * (y - y_2) / (((x - x_2) ** 2 + (y - y_2) ** 2) ** (3 / 2))
               )

        sin = (E_y / (E_y ** 2 + E_x ** 2) ** (1 / 2))
        cos = (E_x / (E_y ** 2 + E_x ** 2) ** (1 / 2))
        tg = E_y/E_x

        if ((abs(tg) <= 1) and (sin >= 0) and (cos >= 0)) or \
                ((abs(tg) <= 1) and (sin <= 0) and (cos >= 0)):
            dx = 0.01
            dy = (E_y/E_x) * dx
            x = x + dx
            y = y + dy
        elif abs(tg) <= 1:
            dx = -0.01
            dy = (E_y/E_x) * dx
            x = x + dx
            y = y + dy
        elif ((abs(tg) >= 1) and (sin > 0) and (cos > 0)) or \
                ((abs(tg) >= 1) and (sin > 0) and (cos < 0)):
            dy = 0.01
            dx = (E_x/E_y) * dy
            x = x + dx
            y = y + dy
        else:
            dy = -0.01
            dx = (E_x/E_y) * dy
            x = x + dx
            y = y + dy

        i = i+1

        list_x.append(x)
        list_y.append(y)


plt.ioff()
plt.show()
