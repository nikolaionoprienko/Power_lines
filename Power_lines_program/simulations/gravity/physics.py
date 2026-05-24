import numpy as np

def movement(n, x_list, y_list, m_list, vx_list, vy_list, t, dt=1/60):

    G = 1000 # 6.67 * 10**(-11) m^3/(kg * c**2)

    acceleration_x_list = np.zeros(n)
    acceleration_y_list = np.zeros(n)

    for k in range(n):
        if m_list[k] !=0:
            mask = np.arange(n) != k
            dist32 = ((x_list[mask] - x_list[k])**2 +
                      (y_list[mask] - y_list[k])**2 + 10**(-9))**(3/2)

            acceleration_x = G * sum( (m_list[mask] * (x_list[mask] - x_list[k])) /
                                      dist32)
            acceleration_y = G * sum((m_list[mask] * (y_list[mask] - y_list[k])) /
                                     dist32)
            acceleration_x_list[k] = acceleration_x
            acceleration_y_list[k] = acceleration_y
        else:
            acceleration_x_list[k] = 0
            acceleration_y_list[k] = 0

    x_list = x_list + (vx_list * dt + acceleration_x_list * dt**2 / 2)
    y_list = y_list + (vy_list * dt + acceleration_y_list * dt**2 / 2)

    vx_list = vx_list + acceleration_x_list * dt
    vy_list = vy_list + acceleration_y_list * dt

    t = t + dt

    return x_list, y_list, vx_list, vy_list, t

def collision(x_list, y_list, m_list, vx_list, vy_list, s_list, c_list):
    n = len(m_list)

    for i in range(n):
        mask = np.arange(n) != i
        dist = ((x_list[mask] - x_list[i])**2 + (y_list[mask] - y_list[i])**2)**(1/2)
        for j in range(n-1):
            if i>j:
                if (dist[j] <= (s_list[i] + s_list[j])) and (m_list[i] != 0) and (m_list[j] != 0):
                    x_list[i] = (m_list[i] * x_list[i] + m_list[j] * x_list[j]) / (m_list[i] + m_list[j])
                    y_list[i] = (m_list[i] * y_list[i] + m_list[j] * y_list[j]) / (m_list[i] + m_list[j])
                    vx_list[i] = (m_list[i] * vx_list[i] + m_list[j] * vx_list[j]) / (m_list[i] + m_list[j])
                    vy_list[i] = (m_list[i] * vy_list[i] + m_list[j] * vy_list[j]) / (m_list[i] + m_list[j])
                    m_list[i] = m_list[i] + m_list[j]
                    s_list[i] = (s_list[i]**3 + s_list[j]**3)**(1/3)

                    x_list[j] = 0
                    y_list[j] = 0
                    vx_list[j] = 0
                    vy_list[j] = 0
                    m_list[j] = 0
                    s_list[j] = 0

        # Очистка "мёртвых" тел
    alive_mask = m_list > 0
    x_list = x_list[alive_mask]
    y_list = y_list[alive_mask]
    m_list = m_list[alive_mask]
    vx_list = vx_list[alive_mask]
    vy_list = vy_list[alive_mask]
    s_list = [s for i, s in enumerate(s_list) if alive_mask[i]]
    c_list = [c for i, c in enumerate(c_list) if alive_mask[i]]

    return x_list, y_list, m_list, vx_list, vy_list, s_list, c_list