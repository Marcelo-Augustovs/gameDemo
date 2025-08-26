import pygame

from code.Level import Level
from code.Const import MENU_OPTION, WIN_HEIGHT, WIN_WIDTH
from code.Menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH,WIN_HEIGHT))

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()
            
            if menu_return == MENU_OPTION[0]:
                level = Level(self.window, 'Level1Bg', menu_return)
                level_return = level.run()
            elif menu_return == MENU_OPTION[4]:
                pygame.quit()
                quit()
            else:
                pass    
                 