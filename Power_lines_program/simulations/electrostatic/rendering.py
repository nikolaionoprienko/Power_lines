import pygame as pg
import numpy as np
from engine.vector import vec
from core.colors import TURQUOISE, WHITE, DARK_GRAY

def draw_scene(scene):
    """Отрисовка линий поля, зарядов и вектора скорости (если тянем) на поле scene.field."""
    field = scene.field

    # Силовые линии
    if scene.power_lines_simulation:
        for segment in scene.segments:
            pg.draw.aalines(field, TURQUOISE, False, segment)

    # Заряды
    for i in range(len(scene.q_list)):
        pg.draw.circle(field, scene.c_list[i], [scene.x_list[i], scene.y_list[i]], scene.s_list[i])
        pg.draw.circle(field, WHITE, [scene.x_list[i], scene.y_list[i]], scene.s_list[i], 2)

    # Вектор скорости при добавлении заряда
    if (scene.LKM or scene.PKM) and scene.field_rect.collidepoint(scene.mouse):
        try:
            vec(field,
                np.array(scene.mouse_start) - np.array([25 * scene.scal_x, 25 * scene.scal_y]),
                scene.mouse - np.array([25 * scene.scal_x, 25 * scene.scal_y]),
                WHITE, vec_size=10)
        except:
            pass
    # Если движение включено – выводим время
    elif scene.movement_simulation:
        time_text = scene.f1.render(str(round(scene.t, 1)) + ' c', True, DARK_GRAY, WHITE)
        field.blit(time_text, (5, 5))