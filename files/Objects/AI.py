import random

import pygame.sprite

from files.Objects.Player import Bullet, BigExplosion
from files.Support.consts import *
from files.Support.events import PAUSE
from files.Support.ui import TANK_AI


class AI(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.LayeredUpdates, size: int = 30, rect: tuple = (0, 0, 0, 0),
                 sort: int = 0, func=None, is_boss: bool = False):

        # сохранение начальных значений
        self.group = group
        self.size = size * TANK_SIZE_KOEF
        self.coord, self.pos = rect[:2], rect[2:]  # pos - позиция на поле, coord - на экране
        self.sort = sort  # тип танка
        self.func = func  # функция для увелечения счета при уничтожении
        self.is_boss = is_boss

        # стартовые значения
        try:
            with open("./Support/ai_settings.txt", "r") as f:
                self.settings = f.readlines()[self.sort + 1].split(";")
        except FileNotFoundError or IndexError:
            self.settings = ["0"] * 5
            print("Ошибка при чтении ./Support/ai_settings.txt")
        self.lives = int(self.settings[3])
        if is_boss:
            self.settings[2] = 0.8 * float(self.settings[2])  # перезарядка
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
        self._change_image()  # загрузка начальных изображений

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

    def _spawn(self):
        # бот спавнится только, если место свободное
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
            self._spawn()
        if not self.spawned:
            return

        if PAUSE in [event.type for event in events]:
            self.pause = not self.pause
        if self.pause:
            return

        if self.freeze != 0:
            self.freeze -= 1
            return
        else:
            self.animation_time += 1
            self.direction_time += 1
            self.fire_time += 1

        if self.stage == 0:  # в первый период игры боты действуют случайно
            if self.direction_time > self.keep_direction_time:
                self._new_move()

            self._move()

            if self.fire_time > self.reload_time:
                self.fire_time = 0
                self._make_shot()

            if self.animation_time > MOVE_ANIMATION:
                self.animation_time = 0
                self.image = self.images[0]
                self.images = self.images[::-1]

    def _new_move(self):
        self.direction_time = 0
        self.speed = self.default_speed
        self.keep_direction_time = random.randint(0, 200) % 20 * 16 + 80
        self._change_direction()

    def _move(self):
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
                    sprite.boom(False)  # некоторые боты могут уничтожить игрока тараном
                    continue

                # танк упертся во что то
                self.speed = 0
                self.keep_direction_time = 0
                self.direction_time = 0
                # возвращаемся на старое место
                self.rect.x, self.rect.y = coord
                self.pos = pos
                break

    def _rotate_image(self):
        # получаем новые сроайты для анимации движения после поворота танка
        self.images[0] = pygame.transform.rotate(self.default_images[0], -90 * self.direction)
        self.images[1] = pygame.transform.rotate(self.default_images[1], -90 * self.direction)

    def _change_direction(self):
        # после смены танк замораживается ненадолго, чтобы не вращался быстро
        self.freeze = 5
        amounts = [0, FIELD_SIZE[0] // 2 - 1]
        if self.pos[0] in amounts and self.pos[1] in amounts:
            # в углу
            if random.randint(0, 3) != 0:
                self._invert_direction()
            else:
                self._near_direction()
        elif self.pos[0] in amounts or self.pos[1] in amounts:
            # у границы
            if random.randint(0, 16) == 0:
                self._invert_direction()
            else:
                self._near_direction()
        else:
            self._random_direction()
        self._rotate_image()

    def _random_direction(self):
        a = self.direction
        while a == self.direction:
            a = random.choice([LEFT, RIGHT, UP, DOWN])
        self.direction = a

    def _near_direction(self):
        a = random.choice([1, -1])
        self.direction = (self.direction + a) % 4

    def _invert_direction(self):
        if self.direction == UP:
            self.direction = DOWN
        elif self.direction == DOWN:
            self.direction = UP
        elif self.direction == LEFT:
            self.direction = RIGHT
        elif self.direction == RIGHT:
            self.direction = LEFT

    def _make_shot(self):
        Bullet(self.group, self.rect, self.bullet_speed, self.direction, False)

    def boom(self, from_player: bool = True) -> bool:
        """попадание пули в танк"""
        if from_player:
            self.lives -= 1
            if self.lives <= 0:
                self.kill()
            else:
                self._change_image()
        return True

    def _change_image(self):
        self.images = list(map(lambda x: pygame.transform.scale(x, (self.size, self.size)),
                               TANK_AI[self.sort][self.lives - 1]))
        self.default_images = self.images.copy()
        self._rotate_image()

    def kill(self):
        """уничтожение танка"""
        self.func(int(self.settings[0]))  # увелечение счета игроков
        BigExplosion(self.group, self.rect.size[0], (self.rect.x, self.rect.y))
        super().kill()
