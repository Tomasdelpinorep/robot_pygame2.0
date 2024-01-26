import pygame
from sprites import *
from config import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('assets/PressStart2P-Regular.ttf', 32)

        self.character_spritesheet = spriteSheet("assets/character.png")
        self.terrain_sprite_sheet = spriteSheet("assets/terrain.png")
        self.intro_background = pygame.image.load("assets/introbackground.png")

    def createTilemap(self):
        # Aquí la i actúa como la coordenada "y" y j actúa como la coordenada "X"
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == "S":
                    Spike(self, j, i)
                if column == "P":
                    Player(self, j, i)
                Ground(self, j, i)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.spikes = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        intro = True

        title = self.font.render('GTA VI', True, pygame.Color(0, 0, 0))
        title_rect = title.get_rect(x=10, y=10)
        play_button = Button(10, 50, 150, 50, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0), 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            # aquí mouse_pressed[0] es left click y mouse_pressed[1] es right click
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
