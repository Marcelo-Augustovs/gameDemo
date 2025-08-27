import pygame
import random
from code.Const import ENTITY_SPEED, WIN_WIDTH, WIN_HEIGHT
from code.Entity import Entity

class Enemy(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)
        
        # Sprites
        self.surf_idle = self.surf
        self.surf_walk = pygame.image.load(f"assets/images/{self.name}_walk.png").convert_alpha()

        # Config spritesheet
        self.frames_per_row_idle = 4    # idle: 4 frames por linha
        self.frames_per_row_walk = 6    # walk: 6 frames por linha
        self.directions = 4             # linhas: 0=baixo,1=esq,2=dir,3=cima

        # Tamanho de frame idle
        self.frame_width_idle = self.surf_idle.get_width() // self.frames_per_row_idle
        self.frame_height_idle = self.surf_idle.get_height() // self.directions

        # Tamanho de frame walk
        self.frame_width_walk = self.surf_walk.get_width() // self.frames_per_row_walk
        self.frame_height_walk = self.surf_walk.get_height() // self.directions

        # Controle de animação
        self.current_frame = 0
        self.row = 1              # direção inicial esquerda
        self.animation_counter = 0
        self.animation_speed = 10

        # Movimento
        self.vx = -2              # velocidade inicial
        self.vy = 0
        self.move_timer = 0
        self.move_interval = random.randint(60, 180)

    def move(self):
        # Atualiza posição
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

        # Muda direção aleatória a cada move_interval frames
        self.move_timer += 1
        if self.move_timer >= self.move_interval:
            self.choose_direction()
            self.move_timer = 0
            self.move_interval = random.randint(60, 180)

        # Mantém dentro das bordas do level
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx = 0
        elif self.rect.right > WIN_WIDTH:
            self.rect.right = WIN_WIDTH
            self.vx = 0

        if self.rect.top < 200:
            self.rect.top = 200
            self.vy = 0
        elif self.rect.bottom > WIN_HEIGHT - 100:
            self.rect.bottom = WIN_HEIGHT - 100
            self.vy = 0

        # Atualiza animação
        if self.vx != 0 or self.vy != 0:  # andando
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % self.frames_per_row_walk
                self.animation_counter = 0
        else:  # parado
            self.current_frame += 1
            if self.current_frame >= self.frames_per_row_idle:
                self.current_frame = 0

    def choose_direction(self):
        direction = random.randint(0, 3)
        speed = 2
        if direction == 0:    # baixo
            self.vx = 0
            self.vy = speed
        elif direction == 2:  # esquerda
            self.vx = -speed
            self.vy = 0
        elif direction == 3:  # direita
            self.vx = speed
            self.vy = 0
        elif direction == 1:  # cima
            self.vx = 0
            self.vy = -speed
        self.row = direction

    def get_frame(self):
        if self.vx != 0 or self.vy != 0:  # andando
            frame_width = self.frame_width_walk
            frame_height = self.frame_height_walk
            surf = self.surf_walk
            frames_per_row = self.frames_per_row_walk
        else:  # parado
            frame_width = self.frame_width_idle
            frame_height = self.frame_height_idle
            surf = self.surf_idle
            frames_per_row = self.frames_per_row_idle

        # Segurança: nunca sair do tamanho da sprite
        if self.current_frame >= frames_per_row:
            self.current_frame = 0

        x = self.current_frame * frame_width
        y = self.row * frame_height
        frame_surf = surf.subsurface((x, y, frame_width, frame_height))

        self.rect.width = frame_width
        self.rect.height = frame_height
        return frame_surf
