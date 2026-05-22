import pygame as pg
from pygame import RESIZABLE
from core.colors import GRAY, WHITE
from core.settings import WINDOW_WIDTH, WINDOW_HEIGHT
from engine.button import button
from simulations.electrostatic.electrostatic_scene import ElectrostaticScene

def main_menu(screen, clock):
    """Главное меню выбора симуляции."""
    font = pg.font.Font(size=50)
    title = font.render("Выберите симуляцию", True, WHITE)

    while True:
        screen.fill(GRAY)
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))

        mouse = pg.mouse.get_pos()
        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return None
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        # Кнопка запуска электростатики
        btn_width, btn_height = 400, 80
        btn_x = WINDOW_WIDTH//2 - btn_width//2
        btn_y = 300
        selected = button(screen, (btn_x, btn_y), btn_width, btn_height,
                          False, click, 'Электростатическое поле')
        if selected:
            return "electrostatic"

        btn2_y = btn_y + btn_height + 20
        selected2 = button(screen, (btn_x, btn2_y), btn_width, btn_height,
                          False, click, 'Гравитация')

        if selected2:
            return "gravity"

        pg.display.update()
        clock.tick(60)

def main():
    pg.init()
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), RESIZABLE)
    pg.display.set_caption('Физические симуляции')
    clock = pg.time.Clock()

    choice = main_menu(screen, clock)
    if choice == "electrostatic":
        scene = ElectrostaticScene(screen)
        scene.run()

    elif choice == "gravity":
        from simulations.gravity.gravity_scene import GravityScene
        scene = GravityScene(screen)
        scene.run()
    else:
        pg.quit()
        return
    scene.run()

    pg.quit()

if __name__ == "__main__":
    main()