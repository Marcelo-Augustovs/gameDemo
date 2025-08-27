from code.Const import ENTITY_SPEED, WIN_WIDTH
from code.Entity import Entity
import pygame

class Enemy(Entity):
    
    def __init__(self, name, position):
        # Supondo que todos os inimigos têm 4 frames e 1 linha
        super().__init__(name, position)
        self.frames_per_row = 4
        self.frame_width = self.surf.get_width() // self.frames_per_row
        self.frame_height = self.surf.get_height()
        
        # Controle de animação
        self.current_frame = 0
        self.animation_counter = 0
        self.animation_speed = 10  # ajuste conforme necessário

    def move(self):
        """Move o inimigo para esquerda e atualiza a animação"""
        speed = ENTITY_SPEED.get(self.name, 0)
        self.rect.centerx -= speed

        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH

        # Atualiza animação
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % self.frames_per_row
            self.animation_counter = 0

    def get_frame(self):
        """Retorna o frame atual e ajusta o rect"""
        x = self.current_frame * self.frame_width
        y = 0  # linha única
        frame_surf = self.surf.subsurface((x, y, self.frame_width, self.frame_height))
        
        # Atualiza o rect
        self.rect.width = self.frame_width
        self.rect.height = self.frame_height
        return frame_surf
