import pygame
from config import *


class Spike(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = SPIKE_LAYER

        # Añade a los grupos de los sprites y de los spikes
        self.groups = self.game.all_sprites, self.game.spikes, self.game.deals_damage_group

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