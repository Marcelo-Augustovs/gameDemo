import random
import sys
import pygame
from pygame.font import Font
from pygame import Rect, Surface
from code.Const import COLOR_YELLOW, EVENT_ENEMY, WIN_HEIGHT
from code.EntityFactory import EntityFactory
from code.Entity import Entity
from code.EntityMediator import EntityMediator
from code.Player import Player



class Level:
    
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = [] 
        self.entity_list.extend(EntityFactory.get_entity(self.name))
        if self.name is not 'menu_inicial':
            self.entity_list.append(EntityFactory.get_entity('Player'))
        self.timeout = 20000 # 20 segundos
        pygame.time.set_timer(EVENT_ENEMY, 2000)
        
    def update(self):
        for ent in self.entity_list:
            ent.move()
            
        if isinstance(ent, (Player)):
            ent.attack()

    def draw(self):
        for ent in self.entity_list:
            self.window.blit(ent.get_frame(), ent.rect)

    def run(self):
        pygame.mixer_music.load(f'./assets/music/{self.name}.wav')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        
        while True:
            clock.tick(60)
            self.update()
            self.draw()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1','Enemy2','Enemy3'))
                    self.entity_list.append(EntityFactory.get_entity(choice))
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_j) or (event.key == pygame.K_z): 
                        for ent in self.entity_list:
                            if isinstance(ent, Player):  
                                ent.attack()    
                                
            self.level_text(18,f'{self.name} - Timeout: {self.timeout / 1000 :.1f}s', COLOR_YELLOW,(10,5))
            self.level_text(18,f'fps: {clock.get_fps() :.0f}', COLOR_YELLOW,(10, WIN_HEIGHT - 35))
            self.level_text(18,f'entidades: {len(self.entity_list)}', COLOR_YELLOW, (10, WIN_HEIGHT - 20))
            pygame.display.flip()
            
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)
        pass
    
    def level_text(self,text_size: int, text:str, text_color: tuple, text_pos: tuple):
        
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter",size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0],top=text_pos[1])
        
        self.window.blit(source=text_surf, dest=text_rect)   