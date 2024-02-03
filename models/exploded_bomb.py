import pygame
from config import *


class ExplodedBomb(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = LIFEBAR_LAYER
        self.groups = self.game.lifebar_group

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = 20
        self.height = 20

        self.image = pygame.transform.scale(self.game.exploded_bomb_sprite, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
