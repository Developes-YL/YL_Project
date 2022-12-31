import random

import pygame.sprite

from files.Objects.Player import Bullet
from files.Support.Consts import DOWN, UP, LEFT, RIGHT
from files.Support.ui import TANK_AI_1


class AI(pygame.sprite.Sprite):
    def __init__(self, size, pos, group):
        super().__init__(group)
        self.group = group
        self.size = size
        self.pos = pos[2:]

        self.image = pygame.transform.scale(TANK_AI_1, (size, size))
        self.default_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[:2]

        self.stage = 0  # стадия игры

        self.direction = DOWN

        self.default_speed = size // 32
        self.speed = self.default_speed

        # движение в сторону
        self.direction_time = 0
        self.keep_direction_time = random.randint(0, 1600) % 800 + 50

        self.fire_time = 0
        self.reload_time = 100

        self.change_direction()

    def update(self, *events):
        self.direction_time += 1
        self.fire_time += 1

        if self.direction_time > self.keep_direction_time:
            self.direction_time = 0
            self.keep_direction_time = random.randint(0, 1600) % 800 + 50
            self.speed = self.default_speed
            self.change_direction()
        else:
            self.move()

        if self.fire_time > self.reload_time:
            self.fire_time = 0
            self.make_shot()

    def move(self):
        pos_1 = self.rect.x, self.rect.y
        pos_2 = self.pos
        if self.direction == UP:
            self.rect.y -= self.speed
            self.pos[1] -= 1
        elif self.direction == DOWN:
            self.rect.y += self.speed
            self.pos[1] += 1
        elif self.direction == LEFT:
            self.rect.x -= self.speed
            self.pos[0] -= 1
        elif self.direction == RIGHT:
            self.rect.x += self.speed
            self.pos[0] += 1

        flag = False
        sprites = pygame.sprite.spritecollide(self, self.group, False)
        for sprt in sprites:
            if sprt.__class__.__name__ not in ["AI", "Bullet"]:
                self.speed = 0
                self.rect.x, self.rect.y = pos_1
                self.pos = pos_2
                flag = True
                break

        if flag:
            self.speed = self.default_speed
            if "Border" in sprites:
                if random.randint(0, 50) % 5 == 0:
                    self.invert_direction()
                else:
                    self.change_direction()
            elif random.randint(0, 50) % 8 == 0:
                self.invert_direction()
            else:
                self.change_direction()

    def rotate(self):
        self.image = pygame.transform.rotate(self.default_image, 90 * self.direction)

    def change_direction(self):
        a = random.choice([LEFT, RIGHT, UP, DOWN])
        while a == self.direction:
            a = random.choice([LEFT, RIGHT, UP, DOWN])
        self.direction = a
        self.rotate()

    def invert_direction(self):
        if self.direction == UP:
            self.direction = DOWN
        elif self.direction == DOWN:
            self.direction = UP
        elif self.direction == LEFT:
            self.direction = RIGHT
        elif self.direction == RIGHT:
            self.direction = LEFT
        self.rotate()

    def make_shot(self):
        self.bullet_speed = self.speed * 2
        Bullet(self.bullet_speed, self.direction, self.rect, self.group, False)

    def __del__(self):
        pass
