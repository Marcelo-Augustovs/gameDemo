import pygame
from code.Const import ENTITY_DAMAGE
from code.Enemy import Enemy
from code.Entity import Entity
from code.Player import Player

class EntityMediator:

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        
        for ent in entity_list:
            #Player
            if isinstance(ent, Player) and ent.state == "attack":
                if getattr(ent, "hit_enemy", False):
                    continue

                attack_size = 2

                if ent.current_direction == 2:  # direita
                    attack_rect = pygame.Rect(ent.rect.right, ent.rect.centery - attack_size // 2, attack_size, attack_size)
                elif ent.current_direction == 1:  # esquerda
                    attack_rect = pygame.Rect(ent.rect.left - attack_size, ent.rect.centery - attack_size // 2, attack_size, attack_size)
                elif ent.current_direction == 0:  # baixo
                    attack_rect = pygame.Rect(ent.rect.centerx - attack_size // 2, ent.rect.bottom, attack_size, attack_size)
                elif ent.current_direction == 3:  # cima
                    attack_rect = pygame.Rect(ent.rect.centerx - attack_size // 2, ent.rect.top - attack_size, attack_size, attack_size)

                
                for target in entity_list:
                    if isinstance(target, Enemy) and target.health > 0:
                        if attack_rect.colliderect(target.rect):
                            target.take_damage(ENTITY_DAMAGE.get(ent.name, 0))

                            
                            ent.hit_enemy = True
                           
              
              #Enemy            
            if isinstance(ent, Enemy) and ent.state == "attack":
                if getattr(ent, "hit_player", False):  
                    continue
                
                attack_size = 2

                # Ajusta área do ataque dependendo da direção
                if ent.row == 3:  # direita
                    attack_rect = pygame.Rect(ent.rect.right, ent.rect.centery - attack_size // 2, attack_size, attack_size)
                elif ent.row == 2:  # esquerda
                    attack_rect = pygame.Rect(ent.rect.left - attack_size, ent.rect.centery - attack_size // 2, attack_size, attack_size)
                elif ent.row == 0:  # baixo
                    attack_rect = pygame.Rect(ent.rect.centerx - attack_size // 2, ent.rect.bottom, attack_size, attack_size)
                elif ent.row == 1:  # cima
                    attack_rect = pygame.Rect(ent.rect.centerx - attack_size // 2, ent.rect.top - attack_size, attack_size, attack_size)

                for target in entity_list:
                    if isinstance(target, Player) and target.health > 0:
                        if attack_rect.colliderect(target.rect):
                            target.take_damage(ENTITY_DAMAGE.get(ent.name, 0))

                            
                            ent.hit_player = True
                            break  


    @staticmethod
    def verify_health(entity_list: list[Entity]):
        now = pygame.time.get_ticks()
        score_gain = 0
        
        for ent in entity_list[:]:
            if isinstance(ent, (Player, Enemy)) and ent.state == "death":
                if isinstance(ent,Enemy):
                    score_gain = 5  
                if ent.death_time and now - ent.death_time >= 7000:  
                    entity_list.remove(ent)
                                        
        return score_gain
