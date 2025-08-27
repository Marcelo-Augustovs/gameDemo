from code.Entity import Entity
import pygame
from code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH

class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        # Configuração da spritesheet original
        self.directions = 4           
        self.frames_per_row = 12      
        self.frame_width = self.surf.get_width() // self.frames_per_row
        self.frame_height = self.surf.get_height() // self.directions

        # Estado inicial
        self.current_direction = 0    # linha atual
        self.current_frame = 0        # frame atual na linha
        self.row = self.current_direction

        # Animation control
        self.animation_counter = 0
        self.animation_speed = 5      

    def move(self):
        pressed_key = pygame.key.get_pressed()
        moving = False

        # animation for key press
        if pressed_key[pygame.K_w] or pressed_key[pygame.K_UP]:
            self.current_direction = 3  # cima
            moving = True   
        elif pressed_key[pygame.K_s] or pressed_key[pygame.K_DOWN]:
            self.current_direction = 0  # baixo
            moving = True   
        elif pressed_key[pygame.K_a] or pressed_key[pygame.K_LEFT]:
            self.current_direction = 1  # esquerda
            moving = True   
        elif pressed_key[pygame.K_d] or pressed_key[pygame.K_RIGHT]:
            self.current_direction = 2  # direita
            moving = True

        # move right
        if (pressed_key[pygame.K_d] or pressed_key[pygame.K_RIGHT]) and self.rect.right < WIN_WIDTH:
            self.rect.centerx += ENTITY_SPEED[self.name]
        # move left    
        if (pressed_key[pygame.K_a] or pressed_key[pygame.K_LEFT]) and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
        # move up    
        if (pressed_key[pygame.K_w] or pressed_key[pygame.K_UP]) and self.rect.top > 0:
            self.rect.centery -= ENTITY_SPEED[self.name]
        # move down    
        if (pressed_key[pygame.K_s] or pressed_key[pygame.K_DOWN]) and self.rect.bottom < WIN_HEIGHT:
            self.rect.centery += ENTITY_SPEED[self.name]

        # Atualiza linha da direção
        self.row = self.current_direction

        if moving:
            self.animation_counter += 1
            
            if self.animation_counter >= self.animation_speed:
            # fix up animation
                if self.current_direction == 3:
                     self.current_frame = (self.current_frame + 1) % 4
                else:
                    self.current_frame = (self.current_frame + 1) % self.frames_per_row
                self.animation_counter = 0
        else:
            self.current_frame = 0  # parado → frame inicial

    def get_frame(self):
        """Retorna o frame atual do Player"""
        x = self.current_frame * self.frame_width
        y = self.row * self.frame_height
        return self.surf.subsurface((x, y, self.frame_width, self.frame_height))
