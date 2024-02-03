import random

import pygame

from Player import Player
from models.blueshroom import BlueShroom
from config import *
from models.button import Button
from models.diamond import Diamond
from models.goggles import Goggles
from models.ground import Ground
from lifebar import LifeBar
from models.redshroom import RedShroom
from models.spike import Spike
from spriteSheet import spriteSheet
from models.water import Water


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('assets/PressStart2P-Regular.ttf', 32)

        self.character_spritesheet = spriteSheet("assets/character.png")
        self.character_waterproof_spriteshet = spriteSheet("assets/animated_waterproof.png")
        self.terrain_sprite_sheet = spriteSheet("assets/terrain.png")
        self.intro_background = pygame.image.load("assets/introbackground.png")
        self.game_over_background = pygame.image.load("assets/gameover.png")
        self.heart_image = pygame.image.load("assets/heartpng.png")
        self.goggles_image = pygame.image.load("assets/goggles.png")
        self.red_shroom_sprite = pygame.image.load("assets/5_life.png")
        self.blue_shroom_sprite = pygame.image.load("assets/3_life.png")
        self.diamond_Sprite = pygame.image.load("assets/diamond.png")

        self.max_spikes = NUM_SPIKES
        self.max_water = NUM_WATER
        self.max_diamonds = NUM_DIAMONDS
        self.max_blue_shrooms = NUM_BLUE_SHROOMS
        self.max_red_shrooms = NUM_RED_SHROOMS

    def createLifeBar(self):
        self.lifeBar = LifeBar(self, 0, WIN_HEIGHT - LIFEBAR_HEIGHT, WIN_WIDTH, LIFEBAR_HEIGHT, self.player)
        self.lifeBar.draw_hearts(self.player.hp)

    def createTilemap(self):

        possible_spawns = ['W', 'S', 'D', 'B', 'Red', 'Blue']

        # Aquí la i actúa como la coordenada "Y" y j actúa como la coordenada "X"
        for i, row in enumerate(TILEMAP):
            for j, column in enumerate(row):
                if column == "S":
                    Spike(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == ".":
                    chance = random.random()
                    # 10% de probabilidad de que spawnee algo en cada bloque
                    if chance < 0.15:
                        hasnt_spawned = True
                        while hasnt_spawned:
                            random_spawn = random.choice(possible_spawns)

                            if random_spawn == 'W' and self.max_water > 0:
                                Water(self, j, i)
                                hasnt_spawned = False
                                self.max_water -= 1

                            if random_spawn == 'S' and self.max_spikes > 0:
                                Spike(self, j, i)
                                hasnt_spawned = False
                                self.max_spikes -= 1

                            if random_spawn == "Blue" and self.max_blue_shrooms > 0:
                                BlueShroom(self, j, i)
                                hasnt_spawned = False
                                self.max_blue_shrooms -= 1

                            if random_spawn == "Red" and self.max_red_shrooms > 0:
                                RedShroom(self, j, i)
                                hasnt_spawned = False
                                self.max_red_shrooms -= 1

                            if random_spawn == "D" and self.max_diamonds > 0:
                                Diamond(self, j, i)
                                hasnt_spawned = False
                                self.max_diamonds -= 1

                            # Por si se da el caso que spawneen todos los bloques posibles antes de que
                            # cargue el mapa al completo
                            item_counters = [self.max_water, self.max_spikes, self.max_blue_shrooms,
                                             self.max_red_shrooms, self.max_diamonds]

                            if all(counter == 0 for counter in item_counters):
                                hasnt_spawned = False

                Ground(self, j, i)

        random_x = random.randint(0, len(TILEMAP[0]) - 1)
        random_y = random.randint(0, len(TILEMAP) - 1)

        existing_element = self.get_element_at_coordinate(random_x, random_y)
        if existing_element:
            existing_element.kill()

        Goggles(self, random_x, random_y)

    def get_element_at_coordinate(self, x, y):
        for sprite in self.all_sprites:
            if isinstance(sprite, (Spike, Water, Goggles)):  # Add more classes if needed
                if sprite.rect.collidepoint(x * TILE_SIZE, y * TILE_SIZE):
                    return sprite
        return None

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.spikes = pygame.sprite.LayeredUpdates()
        self.water = pygame.sprite.LayeredUpdates()
        self.lifebar_group = pygame.sprite.LayeredUpdates()
        self.deals_damage_group = pygame.sprite.Group()
        self.goggles = pygame.sprite.LayeredUpdates()
        self.items_group = pygame.sprite.Group()

        self.createTilemap()
        self.createLifeBar()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        self.lifebar_group.update()
        self.quit_game()

    def draw(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        self.all_sprites.draw(self.screen)
        self.lifebar_group.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        self.playing = False

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

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def quit_game(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
            self.close_game_message()

    def close_game_message(self):
        quit_game_message = True

        game_over_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 16)

        title = game_over_font.render('Are you sure you want to quit?', True, pygame.Color(255, 255, 255))
        title_rect = title.get_rect(x=10, y=10)
        yes_button = Button(10, 50, 150, 50, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0), 'Yes', 32)
        no_button = Button(200, 50, 150, 50, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0), 'No', 32)

        while quit_game_message:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game_message = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            # aquí mouse_pressed[0] es left click y mouse_pressed[1] es right click
            mouse_pressed = pygame.mouse.get_pressed()

            if no_button.is_pressed(mouse_pos, mouse_pressed):
                quit_game_message = False

            if yes_button.is_pressed(mouse_pos, mouse_pressed):
                self.game_over()
                quit_game_message = False

            self.screen.blit(self.game_over_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(yes_button.image, yes_button.rect)
            self.screen.blit(no_button.image, no_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
