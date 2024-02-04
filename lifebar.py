import math

import pygame

from models.exploded_bomb import ExplodedBomb
from models.lifebar_bomb import LifeBarBomb
from models.lifebar_diamond import *
from models.heart import *


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

        self.num_used_bombs = 0

        self.draw_hearts(player.hp)

        # Puntuación
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 16)
        self.text_color = pygame.Color(0, 0, 0)
        self.points = 0

    def draw_hearts(self, hp):
        # Remove only the hearts from the lifebar_group
        for sprite in self.game.lifebar_group.sprites():
            if isinstance(sprite, Heart):
                sprite.kill()

        for i in range(hp):
            heart = Heart(self.game, i * (LIFEBAR_ITEM_SPRITE_WIDTH + 5),
                          WIN_HEIGHT - LIFEBAR_HEIGHT + 5)
            self.game.lifebar_group.add(heart)

    def draw_diamonds(self, num_diamonds):
        diamond = LifeBarDiamond(self.game, (num_diamonds - 1) * (LIFEBAR_ITEM_SPRITE_WIDTH + 5),
                                 WIN_HEIGHT - LIFEBAR_ITEM_SPRITE_HEIGHT - 5)
        self.game.lifebar_group.add(diamond)

    def draw_bombs(self, num_bombs):
        if num_bombs > 0:
            bomb = LifeBarBomb(self.game, (WIN_WIDTH / 2) + (self.num_used_bombs + num_bombs - 1) * (
                    LIFEBAR_ITEM_SPRITE_WIDTH + 5), WIN_HEIGHT - LIFEBAR_ITEM_SPRITE_HEIGHT - 5)
            self.game.lifebar_group.add(bomb)

    # Dibuja los sprites de bombas usadas
    def update_bombs(self, num_bombs):
        for sprite in self.game.lifebar_group.sprites():
            if isinstance(sprite, LifeBarBomb):
                sprite.kill()
                break

        used_bomb = ExplodedBomb(self.game, (WIN_WIDTH / 2) + self.num_used_bombs * (LIFEBAR_ITEM_SPRITE_WIDTH + 5),
                                 WIN_HEIGHT - LIFEBAR_ITEM_SPRITE_HEIGHT - 5)
        self.game.lifebar_group.add(used_bomb)
        self.num_used_bombs += 1

    def draw_score(self):
        self.image.fill(pygame.Color(255, 255, 255))
        score_text_surface = self.font.render(f"Score: {self.points}", True, self.text_color)
        text_x = self.rect.width - score_text_surface.get_width()
        text_y = (LIFEBAR_HEIGHT / 2) - (score_text_surface.get_height() / 2)

        self.image.blit(score_text_surface, (text_x, text_y))

    def calculate_score(self, steps_taken, num_diamonds, hp):
        self.points += math.ceil((num_diamonds * hp) / (steps_taken + 1) ** 0.5)
        self.draw_score()
        return self.points
