import pygame
from code.Const import ENTITY_HEALTH, WIN_HEIGHT
from code.Player import Player


class Hud:
    def __init__(self, entities, pos=(10, WIN_HEIGHT - 50)):
        self.entities = entities
        self.pos = pos

        
        self.base = pygame.image.load("./assets/hud/base.png").convert_alpha()
        self.hp_bar = pygame.image.load("./assets/hud/hp_bar.png").convert_alpha()

        self.hp_width = self.hp_bar.get_width()
        self.hp_height = self.hp_bar.get_height()

        
        self.hp_offset_x = 7   
        self.hp_offset_y = 10   

        
        self.max_hp = ENTITY_HEALTH.get("Player")

    def draw(self, surface):
        x, y = self.pos

        
        surface.blit(self.base, (x, y))

        
        player = None
        for ent in self.entities:
            if isinstance(ent, Player):
                player = ent
                break

        if player:
            
            hp_ratio = max(0, player.health / self.max_hp)

            
            max_bar_width = self.base.get_width() - 2 * self.hp_offset_x
            current_width = int(max_bar_width * hp_ratio)
            current_width = max(0, current_width)

            
            hp_height = self.hp_height + 4  

            
            offset_x = self.hp_offset_x - 12  
            offset_y = self.hp_offset_y - 8     

            
            hp_rect = pygame.Rect(0, 0, current_width, self.hp_height)

         
            surface.blit(self.hp_bar, (x + offset_x, y + offset_y), hp_rect)

