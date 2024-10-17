import numpy as np
import matplotlib.pyplot as plt
import time

print("\033[33m{}\033[0m".format("Вас приветствует программа по численному моделированию электростатического поля нескольких точечных зарядов. \n"))

plt.ion()  # Включение интерактивного режима редактирования графиков

n = 0
check_1 = 0  # Переменная и цикл для проверки правильности введённого значения
while check_1 == 0:
    try:
        n = int(input("Введите количество зарядов: "))
        check_1 = 1
        if n < 0:
            check_1 = 0
            print("Введите положительное число.")
    except:
        print("Можно вводить только натуральные числа, попробуйте ещё раз.")

print("")

x_list = []     # Строка с координатами зарядов по оси Ох
y_list = []     # Строка с координатами зарядов по оси Оу
q_list = []     # Строка с значениями заряда
c_list = []     # Строка с цветами зарядов (красный -- положительный, синий -- отрицательный)
sign_list = []  # Строка со знаками зарядов
s_list = []     # Строка с видимыми размерами заряда (чтобы отличать на графике какой заряд больше по модулю, какой меньше)

ax = []  # Строка с координатами по Ох силовой линии электростатического поля
ay = []  # Строка с координатами по Оy силовой линии электростатического поля

R = 0.01  # Расстояние на которое необходимо подойти линии эл. поля, чтобы она закончила свою отрисовку
max_d = 4  # Установления максимального расстояния до которого будет строится линия

print("\033[31m\033[4m{}".format("Пока что, не следует вводить значения координат такие, чтобы расстояние между зарядами привышало 10 м."), "\033[0m\n")

for i in range(0, n):  # цикл для заполнения начальных условий (заполняются строки с 10 строчки кода по 15)

    check_2 = 0  # Переменная и цикл для проверки правильности введённого значения
    while check_2 == 0:
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

    x_list.append(x)
    y_list.append(y)
    q_list.append(q)
    c_list.append(c)
    sign_list.append(sign)
    s_list.append(s)

start = time.time()  # Начало отсчёта времени выполнения вычислений

fig = plt.figure(figsize=(7, 7), facecolor="#3c3f41")  # Формат фигуры (окна) в котором рисуется график
axis = fig.add_subplot()  # создание осей
axis.set(facecolor="#2b2b2b")  # Цвет фона графика
fig.suptitle("Численное моделирование электрического поля точечных зарядов", c="w")  # Заголовок
plt.xlabel("Ox, м", c="w")  # Подписи осей
plt.ylabel("Oy, м", c="w")
axis.spines['bottom'].set_color("w")  # Изменение цвета осей
axis.spines['top'].set_color("w")
axis.spines['left'].set_color("w")
axis.spines['right'].set_color("w")
axis.tick_params(colors='w')  # Окрашивание рисок

for k in range(0, n):  # Цикл пробегающий все заряды

    x_k = x_list[k]
    y_k = y_list[k]
    q_k = q_list[k]
    z = sign_list[k]
    # (в зависимости от условий будет менятся)

    axis.scatter(x_list, y_list, s=s_list, c=c_list, edgecolors="w", zorder=1)  # Отрисовка зарядов (точечный график)
    axis.plot(ax, ay, linewidth=0.5, c="#00ffff7f", zorder=-1)  # Отрисовка просчитанных линий зарядов
    plt.draw()
    plt.gcf().canvas.flush_events()  # Обрабатывает анимацию

    ax = []  # Обновляем списки координат линий, чтобы не возникло переполнение списка
    ay = []

    for l in range(0, 12):  # Цикл, который рисует для одного заряда несколько линий,
        # отступая от предыдущей линии на некоторый угол

        x_k1 = x_k + R * np.cos(2 * np.pi * l / 12)  # Отступ от заряда на отрезок R в определённом направлении
        y_k1 = y_k + R * np.sin(2 * np.pi * l / 12)

        dx = 0  # Приращение координаты х и у
        dy = 0

        ax = ax + list(reversed(ax))  # Добавление к списку координат линии перевёрнутого списка, чтобы вернутся к заряду
        ay = ay + list(reversed(ay))

        ax.append(x_k)  # Добавление к списку координат линии начальных точек
        ax.append(x_k1)
        ay.append(y_k)
        ay.append(y_k1)

        distance = list([10])
        d_dot_mid = ((x_k1 - sum(x_list) / n) ** 2 + (y_k1 - sum(y_list) / n) ** 2) ** (1 / 2)
        for m in range(0, n):  # Цикл, определяющий дистанции от данной точки линии до других зарядов, чтобы
            # ограничить просчёт если он слишком близко к другому заряду, или если слишком далеко
            # от всех зарядов

            if (m != l) and (n != 1):
                d = ((x_k1 - x_list[m]) ** 2 + (y_k1 - y_list[m]) ** 2) ** (1 / 2)
                distance.append(d)
                if k == 0:
                    max_d = 3 * max(distance)  # Задаём ограничение по дальности прорисовки линии.

        i = 0  # Счётчик следующего цикла, для ограничения итераций вычислений

        while (round(min(distance), 3) >= 0.01) and \
                (max_d > d_dot_mid) and (i <= 1000):  # Цикл просчитывающий одну за другой линии
            E_x = 0  # Проекции на оси напряжённости электростатического поля
            E_y = 0

            for o in range(0, n):  # Вычисление проекций суперпозиции полей всех зарядов
                E_x = (E_x +
                       z * q_list[o] * (x_k1 - x_list[o]) / (
                               ((x_k1 - x_list[o]) ** 2 + (y_k1 - y_list[o]) ** 2) ** (3 / 2))
                       )

                E_y = (E_y +
                       z * q_list[o] * (y_k1 - y_list[o]) / (
                               ((x_k1 - x_list[o]) ** 2 + (y_k1 - y_list[o]) ** 2) ** (3 / 2))
                       )

            sin = (E_y / (E_y ** 2 + E_x ** 2) ** (1 / 2))  # Необходимо для следующих условий
            cos = (E_x / (E_y ** 2 + E_x ** 2) ** (1 / 2))
            tg = E_y / E_x

            # Следующие условия определяют в какую сторону направлена напряжённость поля для корректного простраивания
            # линии.Это нужно для:
            # 1. Например, если мы будем отступать только по оси х на некое dx, а потом считать dу через dx,
            #    то при углах близких, например, к 90 градусах относительно оси Ох, то dy будет стремится к бесконечности
            #    что явно плохо скажется на отображении графика.
            # 2. Например, если угол относительно оси Ох тупой, то dx должно быть отрицательным, однако если не учесть
            #    это условие и оставить dx отрицательным, то мы будем пытаться двигаться в положительном направлении
            #    что опять же приведёт к некорректному отображению линии
            # Чтобы описанного выше не происходило мы разделяем плоскость  на 4 части:
            # от -45 градусов до 45, от 45 до 90 и так далее...
            # P.S. Я давольно таки долго тупил и делал эти выводы, смотря на то, как у меня вместо силовой линий
            #      напряжённости рисуется кардиограмма курильщика :)

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

            ax.append(x_k1)  # Добавляем просчитанную следующую точку к спискам координат линии
            ay.append(y_k1)

            d_dot_mid = ((x_k1 - sum(x_list) / n) ** 2 + (y_k1 - sum(y_list) / n) ** 2) ** (1 / 2)
            for s in range(0, n):  # Обновляем список дистанций от просчитанной точки до зарядов

                if s != l:
                    d = ((x_k1 - x_list[s]) ** 2 + (y_k1 - y_list[s]) ** 2) ** (1 / 2)
                    distance.append(d)

axis.plot(ax, ay, linewidth=0.5, c="#00ffff7f", zorder=-1)  # Отрисовываем итоговые линии
plt.ioff()  # Выключаем интерактивный режим отрисовки графиков

end = time.time()  # Конец отсчёта времени выполнения вычислений
print(f"На вычисления было затрачено {round(end - start, 4)} с.")

plt.show()  # указываем программе чтобы не закрывала окно с графиком после окончания программы

# P.S. У зарядов не указываются единицы измерения, так как для отрисовки линий напряжённости важно не их значение,
#      а отношение значений указанных зарядов. Так же условно координаты отображаются в метрах, однако тут так же
#      важно отношение расстояний, а не их конкретное значение.