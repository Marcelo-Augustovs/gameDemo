from code.Entity import Entity
import pygame
from code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH

class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        # ---- Spritesheets ----
        self.surf_idle = self.surf  # idle (parado)
        self.surf_walk = pygame.image.load("assets/images/player_walk.png").convert_alpha()
        self.surf_walk_atk = pygame.image.load("assets/images/player_walk_attack.png").convert_alpha()
        self.surf_hurt = pygame.image.load("assets/images/player_hurt.png").convert_alpha()
        self.surf_dash = pygame.image.load("assets/images/player_dash.png").convert_alpha()
        self.surf_death = pygame.image.load("assets/images/player_death.png")

        # Config idle
        self.directions = 4
        self.frames_per_row_idle = 12
        self.frames_idle_up = 4
        self.frame_width_idle = self.surf_idle.get_width() // self.frames_per_row_idle
        self.frame_height_idle = self.surf_idle.get_height() // self.directions

        # Config walk
        self.frames_per_row_walk = 6
        self.frame_width_walk = self.surf_walk.get_width() // self.frames_per_row_walk
        self.frame_height_walk = self.surf_walk.get_height() // self.directions

        # Config dash
        self.frames_per_row_dash = 8
        self.frame_width_dash = self.surf_dash.get_width() // self.frames_per_row_dash
        self.frame_height_dash = self.surf_dash.get_height() // self.directions

        # Config walk atk
        self.frames_per_row_walk_atk = 6
        self.frame_width_walk_atk = self.surf_walk_atk.get_width() // self.frames_per_row_walk_atk
        self.frame_height_walk_atk = self.surf_walk_atk.get_height() // self.directions
        
        #config hurt
        self.frames_per_row_hurt = 5
        self.frame_width_hurt = self.surf_hurt.get_width() // self.frames_per_row_hurt
        self.frame_height_hurt = self.surf_hurt.get_height() // self.directions
        
        #config death
        self.frames_per_row_death = 7
        self.frame_width_death = self.surf_death.get_width() // self.frames_per_row_death
        self.frame_height_death = self.surf_death.get_height() // self.directions

        # Estado inicial
        self.state = "idle"  # idle, walk, attack
        self.current_direction = 0
        self.current_frame = 0
        self.row = self.current_direction
        self.moving = False
        self.idle_counter = 0
        self.idle_speed = 10
        self.hit_enemy = False
        self.hurt_duration = self.frames_per_row_hurt  # dura a animação completa
        self.hurt_counter = 0

        # Controle de animação
        self.animation_counter = 0
        self.animation_speed = 5

    def move(self):
        if self.state == "death":
            return
        
        pressed_key = pygame.key.get_pressed()
        self.moving = False

        # Se está atacando, ignora movimento
        if self.state == "attack":
            return  

        # Direção
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

        # Movimento
        if (pressed_key[pygame.K_d] or pressed_key[pygame.K_RIGHT]) and self.rect.right < WIN_WIDTH:
            self.rect.centerx += ENTITY_SPEED[self.name]
        if (pressed_key[pygame.K_a] or pressed_key[pygame.K_LEFT]) and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
        if (pressed_key[pygame.K_w] or pressed_key[pygame.K_UP]) and self.rect.top > 200:
            self.rect.centery -= ENTITY_SPEED[self.name]
        if (pressed_key[pygame.K_s] or pressed_key[pygame.K_DOWN]) and self.rect.bottom < WIN_HEIGHT - 100:
            self.rect.centery += ENTITY_SPEED[self.name]

        self.row = self.current_direction

        # ---- Atualiza estado ----
        if self.state not in ["hurt", "attack"]:
            if self.moving:
                self.state = "walk"
            else:
                self.state = "idle"


    def attack(self):
        if self.state == "death":
            return
        
        pressed_key = pygame.key.get_pressed()
        if self.state != "attack":  # só começa se não estiver atacando
            if pressed_key[pygame.K_j] or pressed_key[pygame.K_z]:
                self.state = "attack"
                self.current_frame = 0
                self.animation_counter = 0
    
    def take_damage(self, damage):
        """Aplica dano e inicia animação de 'hurt' ou 'death'"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.state = "death"
            self.current_frame = 0
            self.animation_counter = 0
            self.death_time = pygame.time.get_ticks()  # marca tempo da morte
        else:
            self.state = "hurt"
            self.current_frame = 0
            self.animation_counter = 0
            self.hurt_counter = 0
 

    def get_frame(self):
        
        if self.state == "death":
            frame_width = self.frame_width_death
            frame_height = self.frame_height_death
            surf = self.surf_death
            max_frames = self.frames_per_row_death   
            speed = self.animation_speed

            if self.current_frame < max_frames - 1:  # avança até o último frame
                self.animation_counter += 1
                if self.animation_counter >= speed:
                    self.current_frame += 1
                    self.animation_counter = 0
            else:
                self.current_frame = max_frames - 1  # trava no último

            
            return surf.subsurface(
                (self.current_frame * frame_width,
                self.row * frame_height,
                frame_width, frame_height)
            )

        

        elif self.state == "hurt":
            frame_width = self.frame_width_hurt
            frame_height = self.frame_height_hurt
            surf = self.surf_hurt
            max_frames  = self.frames_per_row_hurt
            speed = self.animation_speed 
            
            self.animation_counter += 1
            if self.animation_counter >= speed:
                self.current_frame += 1
                self.animation_counter = 0
                self.hurt_counter += 1

            # Se terminou a animação de hurt → volta para idle
            if self.hurt_counter >= max_frames:
                self.state = "idle"
                self.current_frame = 0
                self.hurt_counter = 0
            
        elif self.state == "walk":
            frame_width = self.frame_width_walk
            frame_height = self.frame_height_walk
            surf = self.surf_walk
            max_frames = self.frames_per_row_walk
            
        elif self.state == "attack":
            frame_width = self.frame_width_walk_atk
            frame_height = self.frame_height_walk_atk
            surf = self.surf_walk_atk
            max_frames = self.frames_per_row_walk_atk
            
        else:  # idle
            frame_width = self.frame_width_idle
            frame_height = self.frame_height_idle
            surf = self.surf_idle
            if self.current_direction == 3:
                max_frames = self.frames_idle_up
            else:
                max_frames = self.frames_per_row_idle
        
        
        

        # Atualização de frames
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.current_frame += 1
            self.animation_counter = 0

            # Se ataque terminou → volta para idle
            if self.state == "attack" and self.current_frame >= max_frames:
                self.state = "idle"
                self.current_frame = 0
                self.hit_enemy = False

        # Proteção
        if self.current_frame >= max_frames:
            self.current_frame = 0

        x = self.current_frame * frame_width
        y = self.row * frame_height

        frame_surf = surf.subsurface((x, y, frame_width, frame_height))
        self.rect.width = frame_width
        self.rect.height = frame_height
        return frame_surf
