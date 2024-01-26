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

        self.image = self.game.character_sprite_sheet.get_sprite(3, 2, self.width, self.height)

        # Sets as the same size as the image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()

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

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.spikes, False)
            if hits:
                # Si estoy yendo hacia abajo
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height

                # Si estoy yendo hacia arriba
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom


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
