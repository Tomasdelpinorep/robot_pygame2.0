import pygame

class spriteSheet():
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        # Esto hace que el hitbox negro del personaje sea transparente
        sprite.set_colorkey(pygame.Color(0, 0, 0))
        return sprite