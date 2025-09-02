import pygame

from code.Level import Level
from code.Const import MENU_OPTION, WIN_HEIGHT, WIN_WIDTH
from code.Menu import Menu
from code.Score import Score

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH,WIN_HEIGHT))
        self.score = 0
        self.game_score = Score(self.window)

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()
            
            if menu_return == MENU_OPTION[0]:
                level = Level(self.window, 'Level1Bg', menu_return,score=self.score)
                level_return, self.score = level.run()
                if level_return:
                    level = Level(self.window, 'Level2Bg', menu_return, score=self.score)
                    level_return, self.score = level.run()
                    if level_return:
                        self.game_score.save(menu_return,self.score)   
            
            elif menu_return == MENU_OPTION[1]:
               self.game_score.show()
               pass          
                    
            elif menu_return == MENU_OPTION[2]:
                pygame.quit()
                quit()
            else:
                pass    
                 