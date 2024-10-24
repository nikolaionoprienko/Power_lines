import numpy_learn as np
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation, ArtistAnimation

plt.plot([1, 2, -6, 0, 4])
plt.show()

x = np.array([1, 2, 3, 4])
y = np.array([1, 1/2, 1/3, 1/4])
plt.plot(x, y)
plt.show()

x = np.arange(0, 10, 0.5)
y = np.array([a * a for a in x])  # создаёт массив

x2 = np.arange(-2, 5, 0.5)
y2 = np.array([np.sin(a) for a in x2])

plt.grid  # добавляет сетку
plt.plot(x, y, "-.co", x2, y2, ":k*", markerfacecolor="w")  # стиль и цвет и маркер
plt.show()

line = plt.plot(x, y, x2, y2)
# plt.setp(line, linestyle="-.", color=(0.4, 0.1, 0.3, 0.5))  # Для управление стилем/свойствам всех графиков в line
plt.setp(line, linestyle="-.", color="#391dabe2", marker="o", markerfacecolor="c", linewidth=2)
plt.show()

line = plt.plot(x, y, x2, y2)
# plt.setp(line, linestyle="-.", color=(0.4, 0.1, 0.3, 0.5))  # Для управление стилем/свойствам всех графиков в line
plt.setp(line[0], linestyle="-.", color="#391dabe2", marker="o", markerfacecolor="c", linewidth=2)  # Отдельно для каждого графика
plt.setp(line[1], linestyle="-.", color="#d315d6e2", marker="^", markerfacecolor="b", linewidth=1)
plt.show()

x = np.arange(-2*np.pi, 2*np.pi, 0.01)
y = np.cos(5*x) + np.cos(4*x)
plt.plot(x, y)
plt.fill_between(x, y, color="#29cf92e2")  # Закрашивание криволинейной трапеции
plt.fill_between(x, y, 1, color="#29cf92e2")  # Закрашивание криволинейной трапеции относительно y = 1
plt.fill_between(x, y, where=(y < 0), color=(1, 0.5, 0), alpha=0.5)
plt.fill_between(x, y, where=(y > 0), color=(0, 0.5, 1), alpha=0.5)

plt.grid()
plt.show()

# Первый способ анимации (Цикл):

x = np.arange(-2*np.pi, 2*np.pi, 0.01)

plt.ion()  # Интерактивный режим отображения графика
for f in np.arange(-2*np.pi, 2*np.pi, 0.2):
    y = np.cos(5*x-f) + np.cos(4*x-f)

    plt.clf()  # Очистка окна
    plt.fill_between(x, y, where=(y < 0), color=(1, 0.5, 0), alpha=0.5)
    plt.fill_between(x, y, where=(y > 0), color=(0, 0.5, 1), alpha=0.5)
    plt.plot(x, y)  # Перерисовка графика

    plt.draw()  # Обновление окна
    plt.gcf().canvas.flush_events()  # Обработка событий

    time.sleep(0.01)

plt.ioff()  # Выключение интерактивного режима
plt.show()

# Второй способ: ООП подход

plt.ion()  # Интерактивный режим отображения графика
fig, ax = plt.subplots()  # Создание фигуры и осей

x = np.arange(-4*np.pi, 4*np.pi, 0.01)
y = np.cos(5*x-2*np.pi) + np.cos(4*x-2*np.pi)

line, = ax.plot(x, y)

for f in np.arange(-2*np.pi, 10*np.pi, 0.2):
    y = np.cos(5*x-f) + np.cos(4*x-f)

    line.set_ydata(y)  # Обновление данных

    plt.draw()  # Обновление окна
    plt.gcf().canvas.flush_events()  # Обработка событий

    time.sleep(0.01)

plt.ioff()  # Выключение интерактивного режима
plt.show()

# Третий способ: специальные функции. FuncAnimation


def update(frame, line, x):
    # frame - параметр, который меняется от кадра к кадру
    # в данном случае - фаза
    # line - ссылка на объект Line2D
    line.set_ydata(np.cos(5*x-frame) + np.cos(4*x-frame))
    return [line]


fig, ax = plt.subplots()

x = np.arange(-4*np.pi, 4*np.pi, 0.01)
y = np.cos(5*x-2*np.pi) + np.cos(4*x-2*np.pi)
f = np.arange(-2*np.pi, 10*np.pi, 0.2)

line, = ax.plot(x, y)

animation = FuncAnimation(
    fig,                        # фигура, где отображается анимация
    func=update,                # функция обновления текущего кадра
    frames=f,                   # параметр, меняющийся от кадра к кадру
    fargs=(line, x),            # Дополнительные пормаетры для функции update
    interval=30,                # задержка между кадрами в мс
    blit=True,                  # использовать лт двойную буферизацию
    repeat=True                 # зациклить ли анимацию
)

plt.show()

# Четвёртый способ: для более сложных анимаций (требует больше памяти) ArtistAnimation:

fig = plt.figure(figsize=(10, 6))
ax_3d = fig.add_subplot(projection="3d")

x = np.arange(-2*np.pi, 2*np.pi, 0.1)
y = np.arange(-2*np.pi, 2*np.pi, 0.1)
xgrid, ygrid = np.meshgrid(x, y)

f = np.arange(0, 2*np.pi, 0.1)
frames = []  # Список кадров (пустой пока что)

for i in f:
    zgrid = (np.sin(xgrid**2 + ygrid**2-i))/(xgrid**2 + ygrid**2+1)

    line = ax_3d.plot_surface(xgrid, ygrid, zgrid, color=(0, 1, 1))
    frames.append([line])

animation = ArtistAnimation(
    fig,
    frames,
    interval=10,
    blit=True,
    repeat=True
 )

plt.show()



