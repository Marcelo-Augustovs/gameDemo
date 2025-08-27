from code.Entity import Entity
import pygame
from code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH

class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        # ---- Spritesheets ----
        self.surf_idle = self.surf  # imagem idle (parado)
        self.surf_walk = pygame.image.load("assets/images/player_walk.png").convert_alpha()

        # Config idle
        self.directions = 4
        self.frames_per_row_idle = 12
        self.frames_idle_up = 4  # cima possui apenas 4 frames
        self.frame_width_idle = self.surf_idle.get_width() // self.frames_per_row_idle
        self.frame_height_idle = self.surf_idle.get_height() // self.directions

        # Config walk
        self.frames_per_row_walk = 6
        self.frame_width_walk = self.surf_walk.get_width() // self.frames_per_row_walk
        self.frame_height_walk = self.surf_walk.get_height() // self.directions

        # Estado inicial
        self.current_direction = 0
        self.current_frame = 0
        self.row = self.current_direction
        self.moving = False
        self.idle_counter = 0
        self.idle_speed = 18

        # Controle de animação
        self.animation_counter = 0
        self.animation_speed = 5

    def move(self):
        pressed_key = pygame.key.get_pressed()
        self.moving = False

        # Detecta direção e movimento
        if pressed_key[pygame.K_w] or pressed_key[pygame.K_UP]:
            self.current_direction = 3
            self.moving = True
        elif pressed_key[pygame.K_s] or pressed_key[pygame.K_DOWN]:
            self.current_direction = 0
            self.moving = True
        elif pressed_key[pygame.K_a] or pressed_key[pygame.K_LEFT]:
            self.current_direction = 1
            self.moving = True
        elif pressed_key[pygame.K_d] or pressed_key[pygame.K_RIGHT]:
            self.current_direction = 2
            self.moving = True

        # Atualiza posição
        if (pressed_key[pygame.K_d] or pressed_key[pygame.K_RIGHT]) and self.rect.right < WIN_WIDTH:
            self.rect.centerx += ENTITY_SPEED[self.name]
        if (pressed_key[pygame.K_a] or pressed_key[pygame.K_LEFT]) and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
        if (pressed_key[pygame.K_w] or pressed_key[pygame.K_UP]) and self.rect.top > 200:
            self.rect.centery -= ENTITY_SPEED[self.name]
        if (pressed_key[pygame.K_s] or pressed_key[pygame.K_DOWN]) and self.rect.bottom < WIN_HEIGHT - 100:
            self.rect.centery += ENTITY_SPEED[self.name]

        self.row = self.current_direction

        # ---- Atualiza animação ----
        if self.moving:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % self.frames_per_row_walk
                self.animation_counter = 0
        else:
            self.idle_counter += 1
            if self.idle_counter >= self.idle_speed:
                # Proteção: garante que current_frame nunca extrapole a largura da imagem
                if self.current_direction == 3:  # olhando para cima
                    self.current_frame = (self.current_frame + 1) % self.frames_idle_up
                else:
                    self.current_frame = (self.current_frame + 1) % self.frames_per_row_idle
                self.idle_counter = 0

    def get_frame(self):
        """Retorna o frame atual do Player e ajusta o rect"""
        if self.moving:
            frame_width = self.frame_width_walk
            frame_height = self.frame_height_walk
            surf = self.surf_walk
            max_frames = self.frames_per_row_walk
        else:
            frame_width = self.frame_width_idle
            frame_height = self.frame_height_idle
            surf = self.surf_idle
            # Protege o idle up com 4 frames
            if self.current_direction == 3:
                max_frames = self.frames_idle_up
            else:
                max_frames = self.frames_per_row_idle

        # Garante que current_frame nunca ultrapasse o limite
        if self.current_frame >= max_frames:
            self.current_frame = 0

        x = self.current_frame * frame_width
        y = self.row * frame_height

        # Proteção extra caso algum cálculo ultrapasse a largura/altura da imagem
        if x + frame_width > surf.get_width():
            x = surf.get_width() - frame_width
        if y + frame_height > surf.get_height():
            y = surf.get_height() - frame_height

        frame_surf = surf.subsurface((x, y, frame_width, frame_height))

        # Atualiza o rect para o tamanho do frame atual
        self.rect.width = frame_width
        self.rect.height = frame_height

        return frame_surf
