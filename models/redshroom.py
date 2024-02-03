import pygame
from config import *


class RedShroom(pygame.sprite.Sprite):
    heals = 5

    def __init__(self, game, x, y):
        self.game = game
        self._layer = SPIKE_LAYER
        self.groups = self.game.all_sprites, self.game.items_group

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE + 15
        self.height = TILE_SIZE

        self.image = pygame.transform.scale(game.red_shroom_sprite, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.heals = 5
