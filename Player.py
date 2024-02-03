import math

import pygame
from config import *
from models import redshroom, goggles, spike, water, blueshroom
from models.blueshroom import BlueShroom
from models.diamond import Diamond
from models.goggles import Goggles
from models.redshroom import RedShroom


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        self.hp = 10
        self.bombs = 0
        self.diamonds = 0
        self.cooldown_ticks = 0
        self.cooldown_duration = 15
        self.isWaterproof = False
        self.has_goggles = False
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1
        self.total_steps_taken = 0

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        # Establezco el hitbox un poco más pequeño para que quepa entre rocas
        self.rect = pygame.Rect(self.x, self.y, self.width - 15, self.height - 15)
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
        self.set_watersuit()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.collide_items()

        self.x_change = 0
        self.y_change = 0

        if self.cooldown_ticks > 0:
            self.cooldown_ticks -= 1

    def movement(self):
        keys = pygame.key.get_pressed()

        movement_keys = {
            pygame.K_LEFT: ('left', -PLAYER_SPEED, 0),
            pygame.K_RIGHT: ('right', PLAYER_SPEED, 0),
            pygame.K_UP: ('up', 0, -PLAYER_SPEED),
            pygame.K_DOWN: ('down', 0, PLAYER_SPEED),
        }

        for key, (direction, x_change, y_change) in movement_keys.items():
            if keys[key]:
                self.facing = direction
                self.x_change += x_change
                self.y_change += y_change
                self.total_steps_taken += 1

    # def move_camera_right(self):
    #     # Mando todos los sprites a la izquierda, esto da la ilusión de que hay una cámara siguiendo al personaje
    #     for sprite in self.game.all_sprites:
    #         sprite.rect.x -= PLAYER_SPEED
    #
    # def move_camera_left(self):
    #     for sprite in self.game.all_sprites:
    #         sprite.rect.x += PLAYER_SPEED
    #
    # def move_camera_up(self):
    #     for sprite in self.game.all_sprites:
    #         sprite.rect.y += PLAYER_SPEED
    #
    # def move_camera_down(self):
    #     for sprite in self.game.all_sprites:
    #         sprite.rect.y -= PLAYER_SPEED

    def set_watersuit(self):
        keys = pygame.key.get_pressed()
        # Si se pulsa la T y no se ha pulsado antes y el jugador tiene las gafas:
        if keys[pygame.K_t] and not self.t_pressed and self.has_goggles:
            self.isWaterproof = not self.isWaterproof  # Si está true se vuelve false y viceversa
            self.t_pressed = True
        elif not keys[pygame.K_t]:
            self.t_pressed = False

    def set_player_sprite(self):
        if self.isWaterproof:
            self.image = self.game.character_waterproof_spriteshet.get_sprite(3, 2, self.width, self.height)
        else:
            self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

    def collide_blocks(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.deals_damage_group, False)

        # Actualiza corazones o acaba la partida
        if hits:
            self.game.lifeBar.draw_hearts(self.hp)

            for sprite in hits:

                # Esto permite entrar en un bloque de agua pero te repele de un pincho
                if isinstance(sprite, spike.Spike):
                    self.take_damage()

                    if direction == "x":
                        # Compruebo si se está moviendo a la derecha o a la izquierda
                        if self.x_change > 0:
                            # Coloca el hitbox del personaje (self.rect.x) justo al lado del spike al hacer contacto
                            # Esto es para que se haga contacto 1 vez nada mas e inmediatamente el juego separe los
                            # hitboxes Igualarlo a hits[0] lo coloca justo encima del spike y luego al restarle el
                            # ancho del jugador lo coloca al lado pero sin tocar
                            self.rect.x = hits[0].rect.left - self.rect.width - 10

                        # Si estoy yendo a la izquierda
                        if self.x_change < 0:
                            self.rect.x = hits[0].rect.right + 10

                    if direction == "y":
                        # Si estoy yendo hacia abajo
                        if self.y_change > 0:
                            self.rect.y = hits[0].rect.top - self.rect.height - 10

                        # Si estoy yendo hacia arriba
                        if self.y_change < 0:
                            self.rect.y = hits[0].rect.bottom + 10

                if isinstance(sprite, water.Water):
                    if not self.isWaterproof:
                        self.take_damage()

    def collide_items(self):
        hits = pygame.sprite.spritecollide(self, self.game.items_group, False)

        actions = {
            Goggles: lambda sprite: self.handle_goggles(sprite),
            RedShroom: lambda sprite: self.handle_red_shroom(sprite),
            BlueShroom: lambda sprite: self.handle_blue_shroom(sprite),
            Diamond: lambda sprite: self.handle_diamond(sprite),
        }

        for sprite in hits:
            if type(sprite) in actions:
                actions[type(sprite)](sprite)

    def handle_goggles(self, sprite):
        self.isWaterproof = True
        self.set_player_sprite()
        self.has_goggles = True
        sprite.kill()

    def handle_red_shroom(self, sprite):
        if self.hp + 5 <= 10:
            self.hp += redshroom.RedShroom.heals
            self.game.lifeBar.draw_hearts(self.hp)
            sprite.kill()

    def handle_blue_shroom(self, sprite):
        if self.hp + 3 <= 10:
            self.hp += blueshroom.BlueShroom.heals
            self.game.lifeBar.draw_hearts(self.hp)
            sprite.kill()

    def handle_diamond(self, sprite):
        self.diamonds += 1
        self.game.lifeBar.draw_diamonds(self.diamonds)
        sprite.kill()

    # Hace que solo pueda dañarse 4 veces al segundo
    def take_damage(self):
        if self.cooldown_ticks == 0:
            self.hp -= 1
            if self.hp <= 0:
                self.game.game_over()
            self.game.lifeBar.draw_hearts(self.hp)
            self.cooldown_ticks = self.cooldown_duration

    def animate(self):
        if self.isWaterproof:
            down_animations = [self.game.character_waterproof_spriteshet.get_sprite(3, 2, self.width, self.height),
                               self.game.character_waterproof_spriteshet.get_sprite(35, 2, self.width, self.height),
                               self.game.character_waterproof_spriteshet.get_sprite(68, 2, self.width, self.height)]

            up_animations = [self.game.character_waterproof_spriteshet.get_sprite(3, 34, self.width, self.height),
                             self.game.character_waterproof_spriteshet.get_sprite(35, 34, self.width, self.height),
                             self.game.character_waterproof_spriteshet.get_sprite(68, 34, self.width, self.height)]

            left_animations = [self.game.character_waterproof_spriteshet.get_sprite(3, 98, self.width, self.height),
                               self.game.character_waterproof_spriteshet.get_sprite(35, 98, self.width, self.height),
                               self.game.character_waterproof_spriteshet.get_sprite(68, 98, self.width, self.height)]

            right_animations = [self.game.character_waterproof_spriteshet.get_sprite(3, 66, self.width, self.height),
                                self.game.character_waterproof_spriteshet.get_sprite(35, 66, self.width, self.height),
                                self.game.character_waterproof_spriteshet.get_sprite(68, 66, self.width, self.height)]

            if self.facing == "down":
                # Si el personaje está quieto
                if self.y_change == 0:
                    self.image = self.game.character_waterproof_spriteshet.get_sprite(3, 2, self.width, self.height)

                # Si el personaje se está moviendo hacia abajo
                else:
                    self.image = down_animations[math.floor(self.animation_loop)]
                    # 0.1 porque así suma 1 cada 10 frames (6 veces al segundo)
                    # es decir, cambia la animación 6 veces al segundo
                    self.animation_loop += 0.1
                    # El valor es 3 porque solo hay 3 sprites de animación hacia abajo
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

            if self.facing == "up":
                if self.y_change == 0:
                    self.image = self.game.character_waterproof_spriteshet.get_sprite(3, 34, self.width, self.height)
                else:
                    self.image = up_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

            if self.facing == "right":
                if self.x_change == 0:
                    self.image = self.game.character_waterproof_spriteshet.get_sprite(3, 66, self.width, self.height)
                else:
                    self.image = right_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

            if self.facing == "left":
                if self.x_change == 0:
                    self.image = self.game.character_waterproof_spriteshet.get_sprite(3, 98, self.width, self.height)
                else:
                    self.image = left_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

        else:
            down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

            up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                             self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                             self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

            left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

            right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]

            if self.facing == "down":
                # Si el personaje está quieto
                if self.y_change == 0:
                    self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

                # Si el personaje se está moviendo hacia abajo
                else:
                    self.image = down_animations[math.floor(self.animation_loop)]
                    # 0.1 porque así suma 1 cada 10 frames (6 veces al segundo)
                    # es decir, cambia la animación 6 veces al segundo
                    self.animation_loop += 0.1
                    # El valor es 3 porque solo hay 3 sprites de animación hacia abajo
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

            if self.facing == "up":
                if self.y_change == 0:
                    self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
                else:
                    self.image = up_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

            if self.facing == "right":
                if self.x_change == 0:
                    self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
                else:
                    self.image = right_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                        self.animation_loop = 1

            if self.facing == "left":
                if self.x_change == 0:
                    self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
                else:
                    self.image = left_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                        self.animation_loop = 1
