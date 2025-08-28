from abc import ABC, abstractmethod
import pygame

from code.Const import ENTITY_DAMAGE, ENTITY_HEALTH


class Entity(ABC):
    
    def __init__(self, name: str, position: tuple, frame_size: tuple = None, frames_per_row: int = 1):
        self.name = name
        self.surf = pygame.image.load('./assets/images/' + name + '.png').convert_alpha()
        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.speed = 0
        self.health = ENTITY_HEALTH.get(self.name, 1)
        self.damage = ENTITY_DAMAGE.get(self.name, 0)
        
        # Controle de animação
        self.frame_size = frame_size      
        self.frames_per_row = frames_per_row
        self.current_frame = 0
        self.row = 0
        self.animation_counter = 0
    
    def get_frame(self):
        """Retorna o frame atual ou a imagem inteira"""
        if self.frame_size:  # caso seja sprite sheet
            w, h = self.frame_size
            x = self.current_frame * w
            y = self.row * h
            return self.surf.subsurface((x, y, w, h))
        return self.surf  # entidades normais (background etc.)

    @abstractmethod
    def move(self):
        pass
