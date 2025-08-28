# C
import pygame


COLOR_ORANGE = (255,128,0)
COLOR_WHITE = (128, 128, 128)
COLOR_YELLOW = (255, 215, 0)

#E
EVENT_ENEMY = pygame.USEREVENT + 1
ENTITY_SPEED = {
    'menu_inicial0': 0,
    'menu_inicial1': 1.9,
    'menu_inicial2': 1,
    'menu_inicial3': 1.9,
    'menu_inicial4': 2.5,
    'Player': 1,
    'Enemy1': 1,
    'Enemy2': 1
}
ENTITY_HEALTH = {
    'Player': 250,
    'Enemy1': 150,
    'Enemy2': 200
}
# M 
MENU_OPTION = ('NEW GAME',
               'CONTINUE',
               'SCORE',
               'Credits',
                'EXIT'
)

# W
WIN_WIDTH = 800
WIN_HEIGHT = 620