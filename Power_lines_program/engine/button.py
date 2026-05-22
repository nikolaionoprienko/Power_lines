import numpy as np
import pygame as pg

def button(display, pos, width, height, var, LKM, buttonText=' '):
    fillColors = {
        'normal': (240, 48, 61),
        'hover': var * np.array([100, 163, 102]) + (not var) * np.array([163, 100, 100]),
        'pressed': (63, 204, 68)
    }
    mousePos = pg.mouse.get_pos()
    buttonSurface = pg.Surface((width, height))
    buttonRect = pg.Rect(pos[0], pos[1], width, height)
    font = pg.font.Font(size=22)
    buttonSurf = font.render(buttonText, True, (255, 255, 255))

    if var:
        buttonSurface.fill(fillColors['pressed'])
    else:
        buttonSurface.fill(fillColors['normal'])

    if buttonRect.collidepoint(mousePos):
        buttonSurface.fill(fillColors['hover'])
        if LKM:
            if var:
                var = False
                buttonSurface.fill(fillColors['normal'])
            else:
                var = True
                buttonSurface.fill(fillColors['pressed'])

    buttonSurface.blit(buttonSurf, [
        buttonRect.width / 2 - buttonSurf.get_rect().width / 2,
        buttonRect.height / 2 - buttonSurf.get_rect().height / 2
    ])
    display.blit(buttonSurface, buttonRect)
    pg.draw.rect(display, (255, 255, 255), (pos[0], pos[1], width, height), 2)
    return var