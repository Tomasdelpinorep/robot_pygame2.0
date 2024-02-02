import pygame
from config import *
from heart import *


class LifeBar(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, player):
        self.game = game
        self._layer = LIFEBAR_LAYER
        self.groups = self.game.lifebar_group
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((width, height))
        self.image.fill(pygame.Color(255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.draw_hearts(player.hp)

    def draw_hearts(self, hp):
        # Remove only the hearts from the lifebar_group
        for sprite in self.game.lifebar_group.sprites():
            if isinstance(sprite, Heart):
                sprite.kill()

        for i in range(hp):
            heart = Heart(self.game, i * (LIFEBAR_ITEM_SPRITE_WIDTH + 5),
                          WIN_HEIGHT - (LIFEBAR_HEIGHT - 5))
            self.game.lifebar_group.add(heart)
