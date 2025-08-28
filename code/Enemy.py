import pygame
import random
from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Entity import Entity

class Enemy(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)
        
        # Sprites
        self.surf_idle = self.surf
        self.surf_walk = pygame.image.load(f"assets/images/{self.name}_walk.png").convert_alpha()
        self.surf_atk = pygame.image.load(f"assets/images/{self.name}_atk.png").convert_alpha()
        self.surf_hurt = pygame.image.load(f'assets/images/{self.name}_hurt.png').convert_alpha()

        # Config spritesheet
        self.frames_per_row_idle = 4
        self.frames_per_row_walk = 6
        self.frames_per_row_atk = 6
        self.frames_per_row_hurt = 5
        self.directions = 4

        # Tamanho de frame
        self.frame_width_idle = self.surf_idle.get_width() // self.frames_per_row_idle
        self.frame_height_idle = self.surf_idle.get_height() // self.directions
        self.frame_width_walk = self.surf_walk.get_width() // self.frames_per_row_walk
        self.frame_height_walk = self.surf_walk.get_height() // self.directions
        self.frame_width_atk = self.surf_atk.get_width() // self.frames_per_row_atk
        self.frame_height_atk = self.surf_atk.get_height() // self.directions
        self.frame_width_hurt = self.surf_hurt.get_width() // self.frames_per_row_hurt
        self.frame_height_hurt = self.surf_hurt.get_height() // self.directions

        # Estado e animação
        self.state = "idle"        # idle, walk, attack
        self.current_frame = 0
        self.row = 1
        self.animation_counter = 0
        self.animation_speed = 10          # walk e attack
        self.animation_speed_idle = 30     # idle mais lento
        self.hurt_duration = self.frames_per_row_hurt  # dura a animação completa
        self.hurt_counter = 0
        self.hit_player = False

        # Movimento
        self.vx = -2
        self.vy = 0
        self.move_timer = 0
        self.move_interval = random.randint(60, 180)

        # Ataque automático
        self.attack_timer = 0
        self.attack_interval = random.randint(120, 300)

    def move(self):
    # Atualiza posição
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

        # Muda direção aleatória a cada move_interval frames
        self.move_timer += 1
        if self.move_timer >= self.move_interval and self.state != "hurt":
            self.choose_direction()
            self.move_timer = 0
            self.move_interval = random.randint(60, 180)

        # Mantém dentro das bordas
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

        # Ataque automático
        self.attack_timer += 1
        if self.attack_timer >= self.attack_interval:
            if self.state not in ["hurt", "attack"]:
                self.state = "attack"
                self.current_frame = 0
                self.animation_counter = 0
            self.attack_timer = 0
            self.attack_interval = random.randint(120, 300)

        # Atualiza estado walk/idle, bloqueia se estiver em hurt ou attack
        if self.state not in ["attack", "hurt"]:
            if self.vx != 0 or self.vy != 0:
                self.state = "walk"
            else:
                self.state = "idle"


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
        
    def take_damage(self, damage):
        """Aplica dano e inicia animação de 'hurt'"""
        self.health -= damage
        if self.health < 0:
            self.health = 0
        self.state = "hurt"
        self.current_frame = 0
        self.animation_counter = 0
        self.hurt_counter = 0    

    def get_frame(self):
        # Seleciona sprite baseado no estado
        if self.state == "hurt":
            frame_width = self.frame_width_hurt
            frame_height = self.frame_height_hurt
            surf = self.surf_hurt
            frames_per_row = self.frames_per_row_hurt
            speed = self.animation_speed  # pode ser o mesmo do walk/atk

            self.animation_counter += 1
            if self.animation_counter >= speed:
                self.current_frame += 1
                self.animation_counter = 0
                self.hurt_counter += 1

                if self.current_frame >= frames_per_row:
                    self.current_frame = frames_per_row - 1  # mantém no último frame

                # Finaliza animação de hurt
                if self.hurt_counter >= self.hurt_duration:
                    self.state = "idle"
                    self.current_frame = 0
                    self.hurt_counter = 0

        elif self.state == "attack":
            frame_width = self.frame_width_atk
            frame_height = self.frame_height_atk
            surf = self.surf_atk
            frames_per_row = self.frames_per_row_atk
            speed = self.animation_speed
            self.hit_enemy = False
        elif self.state == "walk":
            frame_width = self.frame_width_walk
            frame_height = self.frame_height_walk
            surf = self.surf_walk
            frames_per_row = self.frames_per_row_walk
            speed = self.animation_speed
        else:  # idle
            frame_width = self.frame_width_idle
            frame_height = self.frame_height_idle
            surf = self.surf_idle
            frames_per_row = self.frames_per_row_idle
            speed = self.animation_speed_idle

        # Atualiza frames apenas para estados diferentes de 'hurt'
        if self.state != "hurt":
            self.animation_counter += 1
            if self.animation_counter >= speed:
                self.current_frame += 1
                self.animation_counter = 0

                # Se ataque terminou → volta para idle
                if self.state == "attack" and self.current_frame >= frames_per_row:
                    self.state = "idle"
                    self.current_frame = 0

            if self.current_frame >= frames_per_row:
                self.current_frame = 0

        x = self.current_frame * frame_width
        y = self.row * frame_height
        frame_surf = surf.subsurface((x, y, frame_width, frame_height))
        self.rect.width = frame_width
        self.rect.height = frame_height
        return frame_surf

