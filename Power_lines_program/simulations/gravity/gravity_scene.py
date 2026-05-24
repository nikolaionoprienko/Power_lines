import pygame as pg
from pygame import RESIZABLE, FULLSCREEN, Surface
import numpy as np
from core.colors import GRAY, DARK_GRAY, WHITE, TURQUOISE
from core.settings import (FPS, WINDOW_WIDTH, WINDOW_HEIGHT, FIELD_HEIGHT, FIELD_WIDTH,
                           DEFAULT_NUMBER_OF_LINES, DEFAULT_NUMBER_OF_ITERATIONS,
                           DEFAULT_Q, DEFAULT_M)
from engine.button import button
from engine.slider import slider
from engine.vector import vec
from simulations.gravity.physics import movement, collision
from simulations.gravity.rendering import draw_scene

class GravityScene:
    def __init__(self, display):
        self.display = display
        self.clock = pg.time.Clock()
        self.play = True

        self.x_list = np.array([])
        self.y_list = np.array([])
        self.m_list = np.array([])
        self.vx_list = np.array([])
        self.vy_list = np.array([])
        self.s_list = []
        self.c_list = []
        self.movement_simulation = True
        self.collision_simulation = True
        self.LKM_ONE = False

        self.m = DEFAULT_M
        self.t = 0.0

        self.LKM = False
        self.mouse = pg.mouse.get_pos()
        self.mouse_start = None

        self.is_fullscreen = False
        self.last_size = (WINDOW_WIDTH, WINDOW_HEIGHT)

        self.f1 = pg.font.Font(size=22)
        self.f2 = pg.font.Font(size=30)
        self.f3 = pg.font.Font(size=28)

        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.height_field = FIELD_HEIGHT
        self.width_field = FIELD_WIDTH

        self.virtual_display = Surface((self.width, self.height))
        self.field = Surface((self.width_field, self.height_field))
        self.field_rect = self.field.get_rect(topleft=(25, 25))

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.play = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    self.is_fullscreen = not self.is_fullscreen
                    if self.is_fullscreen:
                        self.last_size = self.display.get_size()
                        info = pg.display.Info()
                        full_size = (info.current_w, info.current_h)
                        self.display = pg.display.set_mode(full_size, FULLSCREEN)
                    else:
                        self.display = pg.display.set_mode(self.last_size, RESIZABLE)

                elif event.key == pg.K_ESCAPE:
                    self.clear_mass()


            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.LKM = True
                    self.LKM_ONE = True
                if self.field_rect.collidepoint(self.mouse):
                    if event.button == 1:
                        self.add_mass()
                        self.mouse_start = np.array(self.mouse)

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.LKM = False
                    if self.field_rect.collidepoint(self.mouse):
                        self.add_velocity_vector(np.array(self.mouse))



    def add_mass(self):
        x = self.mouse[0] - self.scal_x * 25
        y = self.mouse[1] - self.scal_y * 25
        self.x_list = np.append(self.x_list, x)
        self.y_list = np.append(self.y_list, y)
        self.m_list = np.append(self.m_list, self.m)
        self.s_list.append((3 * self.m)/(4 * np.pi * 5) + 4)
        self.c_list.append((155, 48, 68))

    def add_velocity_vector(self, mouse_pos):
        if self.mouse_start is not None:
            dx = (mouse_pos[0] - self.mouse_start[0])
            dy = (mouse_pos[1] - self.mouse_start[1])
            self.vx_list = np.append(self.vx_list, dx)
            self.vy_list = np.append(self.vy_list, dy)

    def clear_mass(self):
        self.x_list = np.array([])
        self.y_list = np.array([])
        self.m_list = np.array([])
        self.vx_list = np.array([])
        self.vy_list = np.array([])
        self.s_list = []
        self.c_list = []

    def update_and_draw(self):
        """Основное тело цикла: обновление данных, слайдеров, кнопок и рисование."""
        self.mouse = pg.mouse.get_pos()
        self.current_size = self.display.get_size()
        self.scal_x = self.current_size[0] / self.width
        self.scal_y = self.current_size[1] / self.height

        # Очистка экрана
        self.display.fill(GRAY)

        # --- Виртуальный дисплей и статический текст ---
        self.virtual_display.fill(GRAY)

        string_0 = self.f1.render('Управление: ', True, WHITE)
        string_1 = self.f1.render('Добавить массу: ЛКМ', True, WHITE)
        string_2 = self.f1.render('Очистить экран от зарядов: ESC', True, WHITE)
        string_3 = self.f1.render('Развернуть на полный экран: F', True, WHITE)
        string_4 = self.f1.render('Масса', True, WHITE)

        self.virtual_display.blit(string_0, (905, 40))
        self.virtual_display.blit(string_1, (905, 65))
        self.virtual_display.blit(string_2, (905, 90))
        self.virtual_display.blit(string_3, (905, 115))
        self.virtual_display.blit(string_4, (910, 210))

        string_8_8 = self.f1.render(str(self.m) + ' г', True, TURQUOISE)
        self.virtual_display.blit(string_8_8, (1200, 220))

        pg.draw.rect(self.virtual_display, WHITE, (20, 20, 870, 680), 7)

        scaled_virtual = pg.transform.scale(self.virtual_display, self.current_size)
        self.display.blit(scaled_virtual, (0, 0))


        self.field.fill(DARK_GRAY)

        self.m = round(slider(self.display, [self.scal_x * 925, self.scal_y * 235], self.scal_x * 255, 251,
                              self.m / 4, self.mouse, self.LKM, self.m / 4, 20) * 4, 1)

        self.collision_simulation = button(self.display, (self.scal_x * 925, self.scal_y * 450),
                                          self.scal_x * 255, self.scal_y * 25,
                                          self.collision_simulation, self.LKM_ONE,
                                          'Симуляция столкновения')

        self.movement_simulation = button(self.display, (self.scal_x * 925, self.scal_y * 510),
                                          self.scal_x * 255, self.scal_y * 25,
                                          self.movement_simulation, self.LKM_ONE,
                                          'Симуляция движения')

        n = len(self.m_list)
        draw_scene(self)

        scaled_field = pg.transform.scale(
            self.field,
            (self.width_field * self.scal_x, self.height_field * self.scal_y)
        )
        self.display.blit(scaled_field, (25 * self.scal_x, 25 * self.scal_y))
        self.field_rect = scaled_field.get_rect(topleft=(25 * self.scal_x, 25 * self.scal_y))

        if self.movement_simulation and not (self.LKM and self.field_rect.collidepoint(self.mouse)):
            self.x_list, self.y_list, self.vx_list, self.vy_list, self.t = movement(n, self.x_list, self.y_list, self.m_list, self.vx_list, self.vy_list, self.t)

        if self.collision_simulation and not (self.LKM and self.field_rect.collidepoint(self.mouse)):
            self.x_list, self.y_list, self.m_list, self.vx_list, self.vy_list, self.s_list, self.c_list = collision(self.x_list,
                                                                                                                    self.y_list,
                                                                                                                    self.m_list,
                                                                                                                    self.vx_list,
                                                                                                                    self.vy_list,
                                                                                                                    self.s_list,
                                                                                                                    self.c_list )

    def run(self):
        while self.play:
            self.handle_events()
            self.update_and_draw()
            self.LKM_ONE = False
            self.clock.tick(FPS)
            pg.display.update()
