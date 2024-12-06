import numpy as np
import matplotlib.pyplot as plt
import time
from func import power_lines


print("\033[33m{}\033[0m".format("Вас приветствует программа по численному моделированию электростатического поля нескольких точечных зарядов. \n"))

n = 0

check_1 = 0  # Переменная и цикл для проверки правильности введённого значения
while check_1 == 0:
    # noinspection PyBroadException
    try:
        n = int(input("Введите количество зарядов: "))
        check_1 = 1
        if n < 0:
            check_1 = 0
            print("Введите положительное число.")
    except:
        print("Можно вводить только натуральные числа, попробуйте ещё раз.")

x_list = np.zeros(n, dtype=np.float64)     # Строка с координатами зарядов по оси Ох
y_list = np.zeros(n, dtype=np.float64)     # Строка с координатами зарядов по оси Оу
q_list = np.zeros(n, dtype=np.float64)      # Строка со значениями заряда
sign_list = np.zeros(n, dtype=np.float64)   # Строка со знаками зарядов
s_list = np.zeros(n, dtype=np.float64)      # Строка с видимыми размерами заряда (чтобы отличать на графике какой заряд больше по модулю, какой меньше)
c_list = []      # Строка с цветами зарядов (красный -- положительный, синий -- отрицательный)

print("\033[31m\033[4m{}".format("Пока что не следует вводить значения координат такие, чтобы расстояние между зарядами превышало 10 м."), "\033[0m\n")

for i in range(0, n):  # цикл для заполнения начальных условий (заполняются строки с 10 строчки кода по 15)

    check_2 = 0  # Переменная и цикл для проверки правильности введённого значения
    while check_2 == 0:
        # noinspection PyBroadException
        try:
            x = float(input(f"Введите координату x {i + 1}-го заряда: "))
            y = float(input(f"Введите координату y {i + 1}-го заряда: "))
            q = float(input(f"Введите величину q {i + 1}-го заряда: "))
            check_2 = 1
        except:
            print("Можно вводить только действительные числа, попробуйте ещё раз.")

    print("")

    if q > 0:
        c = (0.94, 0.19, 0.24)
        sign = 1
    else:
        c = (0.19, 0.5, 0.96)
        sign = -1

    s = abs(q) * 40

    x_list[i] = x
    y_list[i] = y
    q_list[i] = q
    sign_list[i] = sign
    s_list[i] = s
    c_list.append(c)

# Параметры графики

number_of_lines = 12
number_of_iterations = 1000
drawing_range = 100
x_mid, y_mid = np.sum(x_list) / n, np.sum(y_list) / n
max_distance = (drawing_range**2) * np.amax((x_list - x_mid)**2 + (y_list - y_mid)**2)

start = time.time()  # Начало отсчёта времени выполнения вычислений

fig = plt.figure(figsize=(9, 9), facecolor="#3c3f41")  # Формат фигуры (окна) в котором рисуется график
axis = fig.add_subplot()  # создание осей
axis.set_aspect("equal", adjustable='box')  # Соотношение сторон
axis.set(facecolor="#2b2b2b")  # Цвет фона графика
fig.suptitle("Численное моделирование электрического поля точечных зарядов", c="w")  # Заголовок
plt.xlabel("Ox, м", c="w")  # Подписи осей
plt.ylabel("Oy, м", c="w")
axis.spines['bottom'].set_color("w")  # Изменение цвета осей
axis.spines['top'].set_color("w")
axis.spines['left'].set_color("w")
axis.spines['right'].set_color("w")
axis.tick_params(colors='w')  # Окрашивание рисок

def_time_start = time.time()

ax_list, ay_list = power_lines(number_of_lines, number_of_iterations, n, x_list, y_list, q_list, sign_list,
                               x_mid, y_mid, max_distance)

def_time_end = time.time()
def_time = def_time_end - def_time_start

axis.scatter(x_list, y_list, s=s_list, c=c_list, edgecolors="w", zorder=1)
axis.plot(ax_list, ay_list, linewidth=0.5, c="#00ffff7f", zorder=-1)
end = time.time()  # Конец отсчёта времени выполнения вычислений
print(f"На вычисления было затрачено {round(end - start, 4)} с."
      f" Из них {round(def_time/(end - start) * 100, 1)} % на вычисления координат.")

plt.show()


