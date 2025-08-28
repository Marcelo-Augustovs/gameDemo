from code.Enemy import Enemy
from code.Entity import Entity
from code.Player import Player

class EntityMediator:

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        """
        Verifica colisões de ataque do Player com inimigos.
        """
        for ent in entity_list:
            if isinstance(ent, Player) and ent.state == "attack":
                attack_rect = ent.rect.copy()

                # Ajusta área do ataque dependendo da direção
                if ent.current_direction == 2:  # direita
                    attack_rect.left += ent.rect.width
                    attack_rect.width = 20
                elif ent.current_direction == 1:  # esquerda
                    attack_rect.left -= 20
                    attack_rect.width = 20
                elif ent.current_direction == 0:  # baixo
                    attack_rect.top += ent.rect.height
                    attack_rect.height = 20
                elif ent.current_direction == 3:  # cima
                    attack_rect.top -= 20
                    attack_rect.height = 20

                for target in entity_list:
                    if isinstance(target, Enemy) and target.health > 0:
                        if attack_rect.colliderect(target.rect):
                            target.health -= 10  # aplica dano
                            if target.health <= 0:
                                target.health = 0  # evita negativos

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        """
        Remove entidades com vida <= 0 da lista.
        """
        for ent in entity_list[:]:  # itera sobre cópia para não quebrar a lista
            if isinstance(ent, (Player, Enemy)) and ent.health <= 0:
                entity_list.remove(ent)
