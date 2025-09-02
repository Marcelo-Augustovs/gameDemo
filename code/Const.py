# C
import pygame


COLOR_ORANGE = (255,128,0)
COLOR_WHITE = (128, 128, 128)
COLOR_YELLOW = (255, 215, 0)
COLOR_BLUE = (70, 130, 180)

#E
EVENT_ENEMY = pygame.USEREVENT + 1
EVENT_TIMEOUT = pygame.USEREVENT + 2
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
    'Player': 50,
    'Enemy1': 15,
    'Enemy2': 20,
    'Enemy3': 10
}
ENTITY_DAMAGE = {
    'Player': 5,
    'Enemy1': 10,
    'Enemy2': 15,
    'Enemy3': 5
}
# M 
MENU_OPTION = ('NEW GAME',
               'SCORE',
                'EXIT'
)

# S
SPAWN_TIME = 3000

# T
TIMEOUT_STEP = 100
TIMEOUT_LEVEL = 60000  # 1 min 

# W
WIN_WIDTH = 800
WIN_HEIGHT = 620

# S
SCORE_POS = {'Title': (WIN_WIDTH / 2, 50),
             'EnterName': (WIN_WIDTH / 2, 90),
             'Label': (WIN_WIDTH / 2, 100),
             'Name': (WIN_WIDTH / 2, 120),
             0: (WIN_WIDTH / 2, 140),
             1: (WIN_WIDTH / 2, 160),
             2: (WIN_WIDTH / 2, 180),
             3: (WIN_WIDTH / 2, 200),
             4: (WIN_WIDTH / 2, 220),
             5: (WIN_WIDTH / 2, 240),
             6: (WIN_WIDTH / 2, 260),
             7: (WIN_WIDTH / 2, 280),
             8: (WIN_WIDTH / 2, 300),
             9: (WIN_WIDTH / 2, 320),
             }