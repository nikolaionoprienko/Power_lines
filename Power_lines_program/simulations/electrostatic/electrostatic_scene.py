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
from simulations.electrostatic.physics import power_lines, movement
from simulations.electrostatic.rendering import draw_scene


class ElectrostaticScene:
    def __init__(self, display):
        self.display = display
        self.clock = pg.time.Clock()
        self.play = True

        # Состояние симуляции
        self.x_list = np.array([])
        self.y_list = np.array([])
        self.q_list = np.array([])
        self.m_list = np.array([])
        self.vx_list = np.array([])
        self.vy_list = np.array([])
        self.sign_list = np.array([])
        self.s_list = []
        self.c_list = []
        self.power_lines_simulation = True
        self.movement_simulation = True
        self.LKM_ONE = False

        self.q = DEFAULT_Q
        self.m = DEFAULT_M
        self.t = 0.0

        self.number_of_lines = DEFAULT_NUMBER_OF_LINES
        self.number_of_iterations = DEFAULT_NUMBER_OF_ITERATIONS

        self.LKM = False
        self.PKM = False
        self.mouse = pg.mouse.get_pos()
        self.mouse_start = None

        # Полноэкранный режим
        self.is_fullscreen = False
        self.last_size = (WINDOW_WIDTH, WINDOW_HEIGHT)

        # Шрифты
        self.f1 = pg.font.Font(size=22)
        self.f2 = pg.font.Font(size=30)
        self.f3 = pg.font.Font(size=28)

        # Базовые размеры (для масштабирования)
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.height_field = FIELD_HEIGHT
        self.width_field = FIELD_WIDTH

        # Поверхности
        self.virtual_display = Surface((self.width, self.height))
        self.field = Surface((self.width_field, self.height_field))
        self.field_rect = self.field.get_rect(topleft=(25, 25))

        # Предварительный расчёт
        self.segments = power_lines(self.number_of_lines, self.number_of_iterations, 1,
                                    np.array([457.]), np.array([366.]), np.array([10.]), np.array([1.]))

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
                    self.clear_charges()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.LKM = True
                    self.LKM_ONE = True
                if self.field_rect.collidepoint(self.mouse):
                    if event.button == 1:
                        self.add_positive_charge()
                        self.mouse_start = np.array(self.mouse)
                    elif event.button == 3:
                        self.add_negative_charge()
                        self.PKM = True
                        self.mouse_start = np.array(self.mouse)

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.LKM = False
                    if self.field_rect.collidepoint(self.mouse):
                        self.add_velocity_vector(np.array(self.mouse))
                elif event.button == 3:
                    self.PKM = False
                    if self.field_rect.collidepoint(self.mouse):
                        self.add_velocity_vector(np.array(self.mouse))

    def add_positive_charge(self):
        x = self.mouse[0] - self.scal_x * 25
        y = self.mouse[1] - self.scal_y * 25
        self.x_list = np.append(self.x_list, x)
        self.y_list = np.append(self.y_list, y)
        self.q_list = np.append(self.q_list, self.q)
        self.m_list = np.append(self.m_list, self.m)
        self.sign_list = np.append(self.sign_list, 1)
        if self.m != 10**9:
            self.s_list.append(self.m/100 + 6)
        else:
            self.s_list.append(20)
        self.c_list.append((self.q + 155, 48, 68))

    def add_negative_charge(self):
        x = self.mouse[0] - self.scal_x * 25
        y = self.mouse[1] - self.scal_y * 25
        self.x_list = np.append(self.x_list, x)
        self.y_list = np.append(self.y_list, y)
        self.q_list = np.append(self.q_list, -1 * self.q)
        self.m_list = np.append(self.m_list, self.m)
        self.sign_list = np.append(self.sign_list, -1)
        if self.m != 10**9:
            self.s_list.append(self.m/100 + 6)
        else:
            self.s_list.append(20)
        self.c_list.append((28, 48, self.q + 155))

    def add_velocity_vector(self, mouse_pos):
        if self.mouse_start is not None:
            dx = (mouse_pos[0] - self.mouse_start[0]) / 1000.0
            dy = (mouse_pos[1] - self.mouse_start[1]) / 1000.0
            self.vx_list = np.append(self.vx_list, dx)
            self.vy_list = np.append(self.vy_list, dy)

    def clear_charges(self):
        self.x_list = np.array([])
        self.y_list = np.array([])
        self.q_list = np.array([])
        self.m_list = np.array([])
        self.vx_list = np.array([])
        self.vy_list = np.array([])
        self.sign_list = np.array([])
        self.s_list.clear()
        self.c_list.clear()

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
        string_1 = self.f1.render('Добавить положительный заряд: ЛКМ', True, WHITE)
        string_2 = self.f1.render('Добавить отрицательный заряд: ПКМ', True, WHITE)
        string_3 = self.f1.render('Очистить экран от зарядов: ESC', True, WHITE)
        string_4 = self.f1.render('Развернуть на полный экран: F', True, WHITE)
        string_5 = self.f2.render('Модуль заряда', True, WHITE)
        string_5_5 = self.f2.render('Масса', True, WHITE)
        string_6 = self.f3.render('Количество линий на заряд', True, WHITE)
        string_7 = self.f3.render('Количество итераций', True, WHITE)

        self.virtual_display.blit(string_0, (905, 40))
        self.virtual_display.blit(string_1, (905, 65))
        self.virtual_display.blit(string_2, (905, 90))
        self.virtual_display.blit(string_3, (905, 115))
        self.virtual_display.blit(string_4, (905, 140))
        self.virtual_display.blit(string_5, (970, 195))
        self.virtual_display.blit(string_5_5, (1020, 263))
        self.virtual_display.blit(string_6, (918, 330))
        self.virtual_display.blit(string_7, (950, 397))

        string_8 = self.f1.render(str(self.q) + ' мкКл', True, TURQUOISE)
        if self.m != 10**10:
            string_8_8 = self.f1.render(str(self.m) + ' г', True, TURQUOISE)
        else:
            string_8_8 = self.f1.render("infinity", True, TURQUOISE)
        string_9 = self.f1.render(str(self.number_of_lines), True, TURQUOISE)
        string_10 = self.f1.render(str(self.number_of_iterations), True, TURQUOISE)
        self.virtual_display.blit(string_8, (1200, 220))
        self.virtual_display.blit(string_8_8, (1200, 285))
        self.virtual_display.blit(string_9, (1200, 351))
        self.virtual_display.blit(string_10, (1200, 417))

        pg.draw.rect(self.virtual_display, WHITE, (20, 20, 870, 680), 7)

        scaled_virtual = pg.transform.scale(self.virtual_display, self.current_size)
        self.display.blit(scaled_virtual, (0, 0))

        # --- Поле и его содержимое ---
        self.field.fill(DARK_GRAY)

        # Слайдеры и кнопки (рисуются прямо на self.display и обновляют переменные)
        self.q = slider(self.display, [self.scal_x * 925, self.scal_y * 235], self.scal_x * 255, 50,
                        self.q/2, self.mouse, self.LKM, self.q/2, 5) * 2

        if self.m == 10**10:
            self.m = 1004
        self.m = round(slider(self.display, [self.scal_x * 925, self.scal_y * 300], self.scal_x * 255, 251,
                             self.m/4, self.mouse, self.LKM, self.m/4, 20) * 4, 1)
        if self.m == 1004:
            self.m = 10**10

        self.number_of_lines = int(slider(self.display, [self.scal_x * 925, self.scal_y * 365],
                                         self.scal_x * 255, 20, self.number_of_lines,
                                         self.mouse, self.LKM, self.number_of_lines, 2))
        self.number_of_iterations = int(slider(self.display, [self.scal_x * 925, self.scal_y * 430],
                                              self.scal_x * 255, 20, self.number_of_iterations // 200,
                                              self.mouse, self.LKM, self.number_of_iterations / 200, 2) * 200)

        self.power_lines_simulation = button(self.display, (self.scal_x * 925, self.scal_y * 480),
                                            self.scal_x * 255, self.scal_y * 25,
                                            self.power_lines_simulation, self.LKM_ONE,
                                            'Симуляция электрического поля')
        self.movement_simulation = button(self.display, (self.scal_x * 925, self.scal_y * 510),
                                         self.scal_x * 255, self.scal_y * 25,
                                         self.movement_simulation, self.LKM_ONE,
                                         'Симуляция движения')

        n = len(self.q_list)
        # Если нужно, пересчитываем силовые линии
        if self.power_lines_simulation:
            self.segments = power_lines(self.number_of_lines, self.number_of_iterations,
                                        n, self.x_list, self.y_list, self.q_list, self.sign_list)

        # Рисуем линии и заряды на field
        draw_scene(self)

        # Масштабируем и выводим поле
        scaled_field = pg.transform.scale(self.field, (self.width_field * self.scal_x, self.height_field * self.scal_y))
        self.display.blit(scaled_field, (25 * self.scal_x, 25 * self.scal_y))
        self.field_rect = scaled_field.get_rect(topleft=(25 * self.scal_x, 25 * self.scal_y))

        # Движение зарядов (только когда не тянем вектор)
        if self.movement_simulation and not ((self.LKM or self.PKM) and self.field_rect.collidepoint(self.mouse)):
            self.x_list, self.y_list, self.vx_list, self.vy_list, self.t = movement(
                n, self.x_list, self.y_list, self.q_list, self.m_list,
                self.vx_list, self.vy_list, self.t)

        # Сброс флага однократного нажатия
        self.LKM_ONE = False

    def run(self):
        while self.play:
            self.handle_events()
            self.update_and_draw()
            self.clock.tick(FPS)
            pg.display.update()