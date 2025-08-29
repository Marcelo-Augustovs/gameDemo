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
                if getattr(ent, "hit_enemy", False):  # se já acertou, ignora
                    continue

                attack_rect = ent.rect.copy()

                # Ajusta área do ataque dependendo da direção
                if ent.current_direction == 2:  # direita
                    attack_rect.left += ent.rect.width
                    attack_rect.width = 1
                elif ent.current_direction == 1:  # esquerda
                    attack_rect.left -= 1
                    attack_rect.width = 1
                elif ent.current_direction == 0:  # baixo
                    attack_rect.top += ent.rect.height
                    attack_rect.height = 1
                elif ent.current_direction == 3:  # cima
                    attack_rect.top -= 1
                    attack_rect.height = 1

                for target in entity_list:
                    if isinstance(target, Enemy) and target.health > 0:
                        if attack_rect.colliderect(target.rect):
                            target.take_damage(ENTITY_DAMAGE.get(ent.name, 0))

                            # marca que o ataque já acertou
                            ent.hit_enemy = True
                           
              
              #Enemy            
            if isinstance(ent, Enemy) and ent.state == "attack":
                if getattr(ent, "hit_player", False):  # se já acertou, ignora
                    continue
                
                attack_rect = ent.rect.copy()

                # Ajusta área do ataque dependendo da direção
                if ent.row == 3:  # direita
                    attack_rect.left += ent.rect.width
                    attack_rect.width = 1
                elif ent.row == 2:  # esquerda
                    attack_rect.left -= 1
                    attack_rect.width = 1
                elif ent.row == 0:  # baixo
                    attack_rect.top += ent.rect.height
                    attack_rect.height = 1
                elif ent.row == 1:  # cima
                    attack_rect.top -= 1
                    attack_rect.height = 1

                for target in entity_list:
                    if isinstance(target, Player) and target.health > 0:
                        if attack_rect.colliderect(target.rect):
                            target.take_damage(ENTITY_DAMAGE.get(ent.name, 0))

                            # marca que o ataque já acertou
                            ent.hit_player = True
                            break  # remove o break se quiser atingir múltiplos inimigos por ataque


    @staticmethod
    def verify_health(entity_list: list[Entity]):
        now = pygame.time.get_ticks()
        for ent in entity_list[:]:
            if isinstance(ent, (Player, Enemy)) and ent.state == "death":
                if ent.death_time and now - ent.death_time >= 7000:  # 7.0 segundos
                    entity_list.remove(ent)


