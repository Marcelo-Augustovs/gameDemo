import pygame.image
from pygame import Rect, Surface
from pygame.font import Font

from code.Const import COLOR_ORANGE, COLOR_WHITE, MENU_OPTION, WIN_WIDTH 

class Menu:
    
    def __init__(self,window):
        self.window = window
        self.surface = pygame.image.load('./assets/menu-inicial/imagens/orig800x620.png')
        self.rect = self.surface.get_rect(left=0,top=0)
        
        
    def run(self):
        pygame.mixer_music.load('./assets/menu-inicial/music/160bpm-retro-game-square-wave-song-mysterious-exploration.wav')
        pygame.mixer_music.play(-1)
        
        while True:
            self.window.blit(source=self.surface,dest=self.rect)
            
            self.menu_text(80,"Simple Adventure",COLOR_ORANGE,((WIN_WIDTH / 2), 120)) 
            
            for i in range(len(MENU_OPTION)):
                 self.menu_text(50,MENU_OPTION[i],COLOR_WHITE,((WIN_WIDTH / 2), 280 + 35 * i)) 
           
            pygame.display.flip()

           
            for event in pygame.event.get():
             if event.type == pygame.QUIT: 
                pygame.quit()
                quit()
        
    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
       
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
       
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        
        self.window.blit(source=text_surf,dest=text_rect)
         