import pygame
from config import *


class Bomb(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = SPIKE_LAYER
        self.groups = self.game.all_sprites, self.game.items_group

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = 28
        self.height = 28

        self.image = pygame.transform.scale(self.game.bomb_sprite, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
