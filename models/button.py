import pygame
from config import *


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font("../assets/PressStart2P-Regular.ttf", fontsize)
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
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            # pressed[0] significa que se ha hecho left click
            if pressed[0]:
                return True
            return False
        return False
