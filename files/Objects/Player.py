import pygame.sprite

from files.Objects.Bullet import Bullet
from files.Objects.explosions import BigExplosion
from files.Support.consts import *
from files.Support.events import PAUSE, PLAYER_KILLED, SHOT_EFFECT_EVENT, PLAYER_KILL
from files.Support.ui import TANK_PLAYER


class Player(pygame.sprite.Sprite):
    def __init__(self, group, lst: list, size: int = 30, pos: tuple = (0, 0),
                 number: int = 1, lives: int = PLAYER_LIVES):

        # сохранение начальных значений
        self.lst = lst
        self.group = group
        self.size = size * TANK_SIZE_KOEF
        self.cell_size = size
        self.pos = pos
        self.start = pos
        self.number = number

        # настройка спрайтов и анимаций
        self.images = list(map(lambda x: pygame.transform.scale(x, (self.size, self.size)),
                               TANK_PLAYER[0])).copy()
        self.default_images = self.images.copy()

        self.animation_time = 0

        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(0, 0, 0, 0)

        # стартовые значения
        self.lives = lives
        self.pause = False
        self.direction = UP
        self.freeze = 0
        self.upgrade_status = 0

        self.speed = int(size * TANK_SPEED)
        self.move_buttons = [False] * 4  # ulrd

        # стрельба
        self.fire_time = 0
        self.reload_time = RELOAD_TIME
        self.bullet_speed = int(self.size * BULLET_SPEED)

        self.spawned = False

        # назаначение кнопок упрваления up, left, right, down, shot
        if number == 1:
            self.buttons = [pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_SPACE]
        if number == 2:
            self.buttons = [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_KP_0]
        if number == 3:
            self.buttons = [pygame.K_i, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_h]

        super().__init__(group)
        self._rotate()

    def boom(self, from_player: bool = False):
        """реакция на столкновение с пулей"""
        if not from_player:
            self.lives -= 1

            exp = BigExplosion(self.group, self.cell_size, (self.rect.x, self.rect.y))
            self.group.change_layer(exp, 2)

            if self.lives > 0:
                self.lst[self.number - 1] = Player(self.group, self.lst, self.cell_size,
                                                   self.start, self.number, self.lives)
            else:
                pygame.time.set_timer(pygame.event.Event(PLAYER_KILLED), 1, 1)

            self.kill()
        return True

    def update(self, events):
        if not self.spawned:
            self._spawn()
        if not self.spawned:
            return

        if PAUSE in [event.type for event in events]:
            self.pause = not self.pause
        if self.pause:
            return

        if PLAYER_KILL in [event.type for event in events]:
            self.boom()
            return

        if self.freeze != 0:
            self.freeze -= 1
        else:
            self.animation_time += 1
            self.fire_time += 1

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == self.buttons[0]:
                self.direction = UP
                self.move_buttons = [False] * 4
                self.move_buttons[0] = True
                self._rotate()
            if event.type == pygame.KEYDOWN and event.key == self.buttons[1]:
                self.direction = LEFT
                self.move_buttons = [False] * 4
                self.move_buttons[1] = True
                self._rotate()
            if event.type == pygame.KEYDOWN and event.key == self.buttons[2]:
                self.direction = RIGHT
                self.move_buttons = [False] * 4
                self.move_buttons[2] = True
                self._rotate()
            if event.type == pygame.KEYDOWN and event.key == self.buttons[3]:
                self.direction = DOWN
                self.move_buttons = [False] * 4
                self.move_buttons[3] = True
                self._rotate()

            if event.type == pygame.KEYUP and event.key in self.buttons[:4]:
                self.move_buttons[self.buttons.index(event.key)] = False

            if event.type == pygame.KEYDOWN and event.key == self.buttons[4]:
                if self.fire_time > self.reload_time:
                    self._make_shot(self.direction)

        if True in self.move_buttons:
            self._move()

    def get_lives(self):
        return self.lives

    def _move(self):
        if self.animation_time > MOVE_ANIMATION:
            self.animation_time = 0
            self.image = self.images[0]
            self.images = self.images[::-1]

        coord = self.rect.x, self.rect.y
        speed = self.speed

        if ICE in [a.__class__.__name__ for a in pygame.sprite.spritecollide(self, self.group, False)]:
            speed = int(speed * SPEED_ON_ICE)

        if self.direction == UP:
            self.rect.y -= speed
        if self.direction == DOWN:
            self.rect.y += speed
        if self.direction == LEFT:
            self.rect.x -= speed
        if self.direction == RIGHT:
            self.rect.x += speed

        sprites = pygame.sprite.spritecollide(self, self.group, False)
        for sprite in sprites:
            if sprite.__class__.__name__ not in NON_CONFLICT_OBJECTS:
                if sprite == self:
                    continue
                self.is_move = False
                self.rect.x, self.rect.y = coord
                break

    def _make_shot(self, direction):
        self.fire_time = 0
        pygame.time.set_timer(pygame.event.Event(SHOT_EFFECT_EVENT), 1, 1)
        Bullet(self.group, self.rect, self.bullet_speed, direction, True, self.upgrade_status >= 3)

    def _rotate(self):
        self.images[0] = pygame.transform.rotate(self.default_images[0], -90 * self.direction)
        self.images[1] = pygame.transform.rotate(self.default_images[1], -90 * self.direction)

    def _spawn(self):
        # анимация появление запускается только если рядом нет танков
        sprite = pygame.sprite.Sprite()
        sprite.rect = self.images[0].get_rect()
        sprite.rect.x, sprite.rect.y = self.pos
        if len(pygame.sprite.spritecollide(sprite, self.group, False)) == 0:
            self.image = self.images[0]
            self.rect = self.images[0].get_rect()
            self.rect.x, self.rect.y = self.pos
            self.spawned = True
        del sprite

    def upgrade(self):
        self.upgrade_status += 1
        if self.upgrade_status == 1:
            self.reload_time = int(self.reload_time * 0.8)
        elif self.upgrade_status == 2:
            self.speed = int(self.speed * 1.5)
        elif self.upgrade_status == 3:
            self.images = list(map(lambda x: pygame.transform.scale(x, (self.size, self.size)),
                                   TANK_PLAYER[1])).copy()
            self.default_images = self.images.copy()
            self._rotate()
            self.lives += 1
        else:
            self.lives += 1
