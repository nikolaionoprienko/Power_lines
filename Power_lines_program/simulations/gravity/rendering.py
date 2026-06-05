import pygame as pg
import numpy as np

from engine.vector import vec
from core.colors import WHITE, DARK_GRAY

def draw_scene(scene):

    field = scene.field

    # отрисовка масс
    for i in range(len(scene.m_list)):
        center = scene.phys_to_screen(scene.x_list[i], scene.y_list[i])
        radius = int(scene.s_list[i] * scene.camera_zoom)
        pg.draw.circle(field, scene.c_list[i], center, radius)
        pg.draw.circle(field, WHITE, center, radius, 2)

    # отрисовка вектора скорости при добавлении массы
    if scene.LKM and scene.field_rect.collidepoint(scene.mouse):
        try:
            vec(field,
                np.array(scene.mouse_start) - np.array([25 * scene.scal_x, 25 * scene.scal_y]),
                np.array(scene.mouse) - np.array([25 * scene.scal_x, 25 * scene.scal_y]), WHITE, vec_size=10)
        except:
            pass

    # Вывод времени если движение включено, а добавление массы закончено
    elif scene.movement_simulation:
         time_text = scene.f1.render(str(round(scene.t, 1)) + ' c', True, DARK_GRAY, WHITE)
         field.blit(time_text, (5, 5))

def draw_tracers(scene):
    if not scene.tracers_simulation:
        return
    field = scene.field
    for tracer in scene.tracers:
        if len(tracer) < 2:
            continue
        points = [scene.phys_to_screen(x, y) for x, y in tracer]
        for j in range(1, len(points)):
            brightness = int(255 * j / len(points))
            color = (brightness, 200, 200)
            pg.draw.line(field, color, points[j-1], points[j], 1)