
from datetime import datetime
import sys
import pygame
from pygame.font import Font
from pygame import K_BACKSPACE, K_ESCAPE, K_RETURN, KEYDOWN, Rect, Surface


from code.Const import COLOR_BLUE, COLOR_WHITE, COLOR_YELLOW, MENU_OPTION, SCORE_POS
from code.DBProxy import DBProxy


class Score:
    
    def __init__(self,window):
        self.window = window
        self.surface = pygame.image.load('./assets/images/menu_score.png').convert_alpha()
        self.rect = self.surface.get_rect(left=0,top=0)
        pass
    
    def save(self,menu_return, player_score):
        pygame.mixer_music.load('./assets/music/score_sound.wav')
        pygame.mixer_music.play(-1)
        self.window.blit(source=self.surface, dest=self.rect)
        
        db_proxy = DBProxy('DBscore')
        name = ''
        
        while True:
            self.score_text(98,'YOU WIN!!',COLOR_YELLOW,SCORE_POS['Title'])
            if menu_return == MENU_OPTION[0]:
                score = player_score
                text = 'Player 1 enter your name (4 characters):'
                self.score_text(40,text, COLOR_WHITE, SCORE_POS['EnterName'])
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN and len(name) == 4:
                        db_proxy.save({'name':name,'score': score,'date': get_formatted_date()})
                        self.show()
                        return
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 4:
                            name += event.unicode
                            
            self.score_text(40,name, COLOR_WHITE, SCORE_POS['Name'])                            
            pygame.display.flip()
        
    
    def show(self):
        pygame.mixer_music.load('./assets/music/score_sound.wav')
        pygame.mixer_music.play(-1)
        self.window.blit(source=self.surface, dest=self.rect)
        
        self.score_text(98,'TOP 10 SCORE',COLOR_YELLOW,SCORE_POS['Title'])
        self.score_text(40,'       NAME        SCORE                     DATE',COLOR_BLUE,SCORE_POS['Label'])
        db_proxy = DBProxy('DBscore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()
        
        for player_score in list_score:
            id_, name, score, date = player_score
            self.score_text(40,f'                  {name}         {score:6d}           {date}   ',COLOR_WHITE,SCORE_POS[list_score.index(player_score)])
            
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return    
            pygame.display.flip()
            
        
    def score_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)

        # texto principal
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=(text_pos[0], text_pos[1]))
        self.window.blit(text_surf, text_rect)
   
def get_formatted_date():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M")
    current_date = current_datetime.strftime("%d/%m/%y")
    return f"{current_time} - {current_date}"
    