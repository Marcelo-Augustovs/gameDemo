import random
import sys
import pygame
from pygame.font import Font
from pygame import Rect, Surface
from code.Hud import Hud
from code.Const import COLOR_WHITE, COLOR_YELLOW, EVENT_ENEMY, EVENT_TIMEOUT, SPAWN_TIME, TIMEOUT_LEVEL, TIMEOUT_STEP, WIN_HEIGHT, COLOR_BLUE, WIN_WIDTH
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
        self.score = 0
        
        self.hud = None
        if self.name != 'menu_inicial':
            self.entity_list.append(EntityFactory.get_entity('Player'))
            
            self.lose_image = pygame.image.load("./assets/hud/lose.png").convert_alpha()
            self.player_dead = False 
            self.win_image = pygame.image.load("./assets/hud/win.png").convert_alpha()
             
            self.hud = Hud(self.entity_list)
            
            
        self.timeout = TIMEOUT_LEVEL 
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)
        
    def update(self):
        for ent in self.entity_list:
            ent.move()
            
            if isinstance(ent, (Player)):
                ent.attack()
            
        EntityMediator.verify_collision(self.entity_list)
        EntityMediator.verify_health(self.entity_list)
        
        self.score_gain = EntityMediator.verify_health(self.entity_list)
        self.score += self.score_gain
        
        self.player_dead = any(isinstance(ent, Player) and ent.state == "death" for ent in self.entity_list)

    def draw(self):
        for ent in self.entity_list:
            self.window.blit(ent.get_frame(), ent.rect)
            
        if self.hud:
            self.hud.draw(self.window)
                

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
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP  
                    if self.timeout == 0:
                        rect = self.win_image.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
                        self.window.blit(self.win_image, rect)
                        pygame.display.flip()
                        
                        pygame.time.delay(3000)
                        return True  
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_j) or (event.key == pygame.K_z): 
                        for ent in self.entity_list:
                            if isinstance(ent, Player):  
                                ent.attack()    
                                
            if self.player_dead:
                rect = self.lose_image.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
                self.window.blit(self.lose_image, rect)
                pygame.display.flip()
                
                pygame.time.delay(3000)
                return False  
                                
            self.level_text(18,f'{self.name[:6]} - Timeout: {self.timeout / 1000 :.1f}s', COLOR_WHITE,(10,5))
            #FPS
            self.level_text(18,f'FPS: {clock.get_fps() :.0f}', COLOR_YELLOW,(10, WIN_HEIGHT - 20))
            #score
            self.level_text(18,f'Score: {self.score}', COLOR_BLUE,(WIN_WIDTH - 110,5))
            pygame.display.flip()
        pass
    
    def level_text(self,text_size: int, text:str, text_color: tuple, text_pos: tuple):
        
        text_font: Font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)

        # sombra preta
        shadow_surf = text_font.render(text, True, (0, 0, 0)).convert_alpha()
        shadow_rect: Rect = shadow_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(shadow_surf, shadow_rect)

        # texto principal
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(text_surf, text_rect)  