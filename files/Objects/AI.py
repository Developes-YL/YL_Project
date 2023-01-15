
import random

import pygame.sprite

from files.Objects.Player import Bullet, BigExplosion
from files.Support.consts import *
from files.Support.events import PAUSE, AI_DESTROYED
from files.Support.ui import TANK_AI


class AI(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.LayeredUpdates, size: int = 30, rect: tuple = (0, 0, 0, 0),
                 sort: int = 0, is_boss: bool = False):

        # сохранение начальных значений
        self.group = group
        self.size = size * TANK_SIZE_KOEF
        self.coord, self.pos = rect[:2], rect[2:]  # pos - позиция на поле, coord - на экране
        self.sort = sort
        self.is_boss = is_boss

        # стартовые значения
        with open("./Support/ai_settings.txt", "r") as f:
            self.settings = f.readlines()[1 + self.sort].split(";")
        self.lives = int(self.settings[3])
        if is_boss:
            self.settings[2] = 0.9 * float(self.settings[2])
        self.ram = self.settings[4] == "t"

        self.pause = False
        self.stage = 0  # стадия игры
        self.direction = DOWN
        self.freeze = 0

        self.default_speed = size * TANK_SPEED * float(self.settings[1])
        self.speed = self.default_speed

        # настройка спрайтов и анимаций
        self.images = []
        self.default_images = []
        self.change_image()

        self.animation_time = 0

        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(0, 0, 0, 0)

        # движение в сторону
        self.direction_time = 0
        self.keep_direction_time = 0

        # стрельба
        self.fire_time = 0
        self.reload_time = RELOAD_TIME * float(self.settings[2])
        self.bullet_speed = int(self.size * BULLET_SPEED)

        super().__init__(group)
        self.spawned = False

    def spawn(self):
        # анимация появление запускается только если рядом нет танков
        sprite = pygame.sprite.Sprite()
        sprite.rect = self.images[0].get_rect()
        sprite.rect.x, sprite.rect.y = self.coord
        if len(pygame.sprite.spritecollide(sprite, self.group, False)) == 0:
            self.image = self.images[0]
            self.rect = self.images[0].get_rect()
            self.rect.x, self.rect.y = self.coord
            self.spawned = True
        del sprite

    def update(self, events):
        if not self.spawned:
            self.spawn()
        if not self.spawned:
            return
        if PAUSE in [event.type for event in events]:
            self.pause = not self.pause
        if self.pause:
            return

        if self.freeze != 0:
            self.freeze -= 1
        else:
            self.animation_time += 1
            self.direction_time += 1
            self.fire_time += 1

        if self.stage == 0:
            if self.direction_time > self.keep_direction_time:
                self.new_move()
            elif self.freeze == 0:
                self.move()

            if self.fire_time > RELOAD_TIME:
                self.fire_time = 0
                self.make_shot()

            if self.animation_time > MOVE_ANIMATION:
                self.animation_time = 0
                self.image = self.images[0]
                self.images[:2] = self.images[:2][::-1]

    def new_move(self):
        self.direction_time = 0
        self.speed = self.default_speed
        self.keep_direction_time = random.randint(0, 100) % 10 * 16 + 80
        self.change_direction()

    def move(self):
        coord = self.rect.x, self.rect.y
        speed = self.speed
        if ICE in [a.__class__.__name__ for a in pygame.sprite.spritecollide(self, self.group, False)]:
            speed = int(speed * SPEED_ON_ICE)
        pos = self.pos

        if self.direction == UP:
            self.rect.y -= speed
            self.pos[1] -= 1
        elif self.direction == DOWN:
            self.rect.y += speed
            self.pos[1] += 1
        elif self.direction == LEFT:
            self.rect.x -= speed
            self.pos[0] -= 1
        elif self.direction == RIGHT:
            self.rect.x += speed
            self.pos[0] += 1

        sprites = pygame.sprite.spritecollide(self, self.group, False)
        for sprite in sprites:
            if sprite.__class__.__name__ not in NON_CONFLICT_OBJECTS:
                if sprite == self:
                    continue
                if sprite.__class__.__name__ == PLAYER and self.ram:
                    sprite.kill()
                    continue

                self.speed = 0
                self.keep_direction_time = 0
                self.direction_time = 0

                self.rect.x, self.rect.y = coord
                self.pos = pos
                break

    def rotate_image(self):
        self.images[0] = pygame.transform.rotate(self.default_images[0], -90 * self.direction)
        self.images[1] = pygame.transform.rotate(self.default_images[1], -90 * self.direction)

    def change_direction(self):
        self.freeze = 4
        amounts = [0, FIELD_SIZE[0] // 2 - 1]
        if self.pos[0] in amounts and self.pos[1] in amounts:
            # в углу
            if random.randint(0, 3) != 0:
                self.invert_direction()
            else:
                self.near_direction()
        elif self.pos[0] in amounts or self.pos[1] in amounts:
            # у границы
            if random.randint(0, 16) == 0:
                self.invert_direction()
            else:
                self.near_direction()
        else:
            self.random_direction()
        self.rotate_image()

    def random_direction(self):
        a = self.direction
        while a == self.direction:
            a = random.choice([LEFT, RIGHT, UP, DOWN])
        self.direction = a

    def near_direction(self):
        a = random.choice([1, -1])
        self.direction = (self.direction + a) % 4

    def invert_direction(self):
        if self.direction == UP:
            self.direction = DOWN
        elif self.direction == DOWN:
            self.direction = UP
        elif self.direction == LEFT:
            self.direction = RIGHT
        elif self.direction == RIGHT:
            self.direction = LEFT

    def make_shot(self):
        Bullet(self.bullet_speed, self.direction, self.rect, self.group, False)

    def boom(self, flag: bool = True) -> bool:
        if flag:
            self.lives -= 1
            if self.lives == 0:
                self.kill()
            else:
                self.change_image()
        return True

    def change_image(self):
        self.images = list(map(lambda x: pygame.transform.scale(x, (self.size, self.size)),
                               TANK_AI[self.sort][self.lives - 1]))
        self.default_images = self.images.copy()
        self.rotate_image()

    def kill(self):
        pygame.time.set_timer(pygame.event.Event(AI_DESTROYED, score=int(self.settings[0])), 1, 1)
        BigExplosion(self.group, self.rect.size[0], self.rect.x, self.rect.y)
        super().kill()
