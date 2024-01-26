import pygame
from config import *
import math
import random


class spriteSheet():
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        # Esto hace que el hitbox negro del personaje sea transparente
        sprite.set_colorkey(pygame.Color(0, 0, 0))
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        # Establezco el hitbox al mismo tamaño que la imagen
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def move_camera_right(self):
        # Mando todos los sprites a la izquierda, esto da la ilusión de que hay una cámara siguiendo al personaje
        for sprite in self.game.all_sprites:
            sprite.rect.x -= PLAYER_SPEED

    def move_camera_left(self):
        for sprite in self.game.all_sprites:
            sprite.rect.x += PLAYER_SPEED

    def move_camera_up(self):
        for sprite in self.game.all_sprites:
            sprite.rect.y += PLAYER_SPEED

    def move_camera_down(self):
        for sprite in self.game.all_sprites:
            sprite.rect.y -= PLAYER_SPEED

    def collide_blocks(self, direction):
        if direction == "x":
            # Ese último parámetro "dokill" es por si quieres borrar el sprite al colisionar
            hits = pygame.sprite.spritecollide(self, self.game.spikes, False)
            if hits:
                # Compruebo si se está moviendo a la derecha o a la izquierda
                if self.x_change > 0:
                    # Coloca el hitbox del personaje (self.rect.x) justo al lado del spike al hacer contacto
                    # Esto es para que se haga contacto 1 vez nada mas e inmediatamente el juego separe los hitboxes
                    # Igualarlo a hits[0] lo coloca justo encima del spike y luego al restarle el ancho del jugador
                    # lo coloca al lado pero sin tocar
                    self.rect.x = hits[0].rect.left - self.rect.width

                # Si estoy yendo a la izquierda
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

            # Si no choca y se mueve a la derecha o izquierda, muevo la "cámara"
            else:
                if self.x_change > 0:
                    self.move_camera_right()
                if self.x_change < 0:
                    self.move_camera_left()

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.spikes, False)
            if hits:
                # Si estoy yendo hacia abajo
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height

                # Si estoy yendo hacia arriba
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

            # Si no choca y se mueve hacia arriba o abajo, muevo la "cámara"
            else:
                if self.y_change > 0:
                    self.move_camera_down()
                if self.y_change < 0:
                    self.move_camera_up()

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]

        if self.facing == "down":
            # Si el personaje está quieto
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

            # Si el personaje se está moviendo hacia abajo
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                # 0.1 porque así suma 1 cada 10 frames (6 veces al segundo)
                # es decir, cambia la animación 6 veces al segundo
                self.animation_loop += 0.1
                # El valor es 3 porque solo hay 3 sprites de animación hacia abajo
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Spike(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = SPIKE_LAYER
        self.groups = self.game.all_sprites, self.game.spikes  # Añade a los grupos de los sprites y de los spikes

        # Llama al inicializador de sprite.Sprite y se añade la clase Spike a los grupos de sprite pasados por parámetro
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_sprite_sheet.get_sprite(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_sprite_sheet.get_sprite(64, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", fontsize)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg = bg
        self.fg = fg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        # Coloca el texto en la mitad del botón
        self.text_rect = self.text.get_rect(center = (self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            # pressed[0] significa que se ha hecho left click
            if pressed[0]:
                return True
            return False
        return False


