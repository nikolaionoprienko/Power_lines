import numpy as np

def movement(n, x_list, y_list, m_list, vx_list, vy_list, t, dt=1/60):

    G = 1000 # 6.67 * 10**(-11) m^3/(kg * c**2)

    acceleration_x_list = np.zeros(n)
    acceleration_y_list = np.zeros(n)

    for k in range(n):

        mask = np.arange(n) != k
        dist32 = ((x_list[mask] - x_list[k])**2 +
                  (y_list[mask] - y_list[k])**2 + 10**(-9))**(3/2)

        acceleration_x = G * sum( (m_list[mask] * (x_list[mask] - x_list[k])) /
                                  dist32)
        acceleration_y = G * sum((m_list[mask] * (y_list[mask] - y_list[k])) /
                                 dist32)
        acceleration_x_list[k] = acceleration_x
        acceleration_y_list[k] = acceleration_y

    x_list = x_list + (vx_list * dt + acceleration_x_list * dt**2 / 2)
    y_list = y_list + (vy_list * dt + acceleration_y_list * dt**2 / 2)

    vx_list = vx_list + acceleration_x_list * dt
    vy_list = vy_list + acceleration_y_list * dt

    t = t + dt

    return x_list, y_list, vx_list, vy_list, t