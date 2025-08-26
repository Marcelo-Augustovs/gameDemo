import pygame.image
from pygame import Rect, Surface
from pygame.font import Font
from code.Level import Level

from code.Const import COLOR_ORANGE, COLOR_WHITE, COLOR_YELLOW, MENU_OPTION, WIN_WIDTH 

class Menu:
    
    def __init__(self,window):
        self.window = window
        self.background = Level(self.window, 'menu_inicial', self)
        
        
    def run(self):
        menu_option = 0
        clock = pygame.time.Clock()
    
        #music
        pygame.mixer_music.load('./assets/music/menu-inicial-160bpm-retro-game-square-wave-song-mysterious-exploration.wav')
        pygame.mixer_music.play(-1)
        
        #Menu
        while True:
            clock.tick(60)
            self.background.update()
            self.background.draw() 
            
                       
            self.menu_text(80,"Simple Adventure",COLOR_ORANGE,((WIN_WIDTH / 2), 120)) 
            
            for i in range(len(MENU_OPTION)):
                
              if i == menu_option:   
                self.menu_text(50,MENU_OPTION[i],COLOR_YELLOW,((WIN_WIDTH / 2), 280 + 35 * i)) 
              else:   
                self.menu_text(50,MENU_OPTION[i],COLOR_WHITE,((WIN_WIDTH / 2), 280 + 35 * i)) 
            pygame.display.flip()
        
        # events
            for event in pygame.event.get():
              if event.type == pygame.QUIT: 
                pygame.quit()
                quit()
              if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                  if menu_option < len(MENU_OPTION) -1:
                    menu_option += 1  
                  else:
                    menu_option = 0
                if event.key == pygame.K_w:
                  if menu_option > 0:
                    menu_option -= 1
                  else:
                    menu_option = len(MENU_OPTION) -1  
                if event.key == pygame.K_RETURN: 
                    return MENU_OPTION[menu_option]
        
    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
       
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
       
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        
        self.window.blit(source=text_surf,dest=text_rect)
         