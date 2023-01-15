import pygame.sprite

from files.Support.consts import AI, PLAYER, GAME_END_FREEZE, BONUS_ANIMATION
from files.Support.events import PAUSE, STOP_GAME
from files.Support.ui import *


class Cell(pygame.sprite.Sprite):
    def __init__(self, size, pos, group):
        self._layer = 0
        self.size = size
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.set_up()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.group = group
        super().__init__(group)
        group.change_layer(self, self._layer)

    def set_up(self):
        self.image = pygame.Surface([0, 0])

    def boom(self, flag) -> bool:
        return False


class Brick(Cell):
    def set_up(self):
        self.image = BRICK_IMAGE
        self.time = 0

    def boom(self, flag) -> bool:
        self.image = pygame.transform.scale(self.image, (0, 0))
        pos = self.rect.x, self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        return True

    def upgrade(self, group):
        group[group.index(self)] = Concrete(self.size, (self.rect.x, self.rect.y), self.group)
        self.kill()


class Water(Cell):
    def set_up(self):
        self.image = WATER_IMAGE


class Concrete(Cell):
    def set_up(self):
        self.image = CONCRETE_IMAGE

    def boom(self, flag) -> bool:
        if flag:
            self.kill()
        return True

    def degrade(self, group):
        group[group.index(self)] = Brick(self.size, (self.rect.x, self.rect.y), self.group)
        self.kill()

    def upgrade(self, group):
        pass


class Bush(Cell):
    def set_up(self):
        self.image = BUSH_IMAGE
        self._layer = 3


class Ice(Cell):
    def set_up(self):
        self.image = ICE_IMAGE


class Base1(Cell):
    def set_up(self):
        self.image = BASE_1_IMAGE
        self.flag = True

    def boom(self, flag) -> bool:
        if self.flag:
            self.lose()
            self.flag = False
        return True

    def lose(self):
        # функция на пройгрыш
        pygame.time.set_timer(pygame.event.Event(PAUSE), 1, 1)
        pygame.time.set_timer(pygame.event.Event(STOP_GAME, game_over=True), GAME_END_FREEZE, 1)
        Base2(self.rect.size[0], (self.rect.x, self.rect.y), self.group)
        self.kill()


class Base2(Cell):
    def set_up(self):
        self.image = BASE_2_IMAGE

    def boom(self, flag):
        return True


class Bonus(Cell):
    def set_up(self):
        self.set_up_2()
        self.image = pygame.transform.scale(self.image, (self.size, self.size)).copy()
        self._layer = 3
        self.time = 0
        self.__class__.__name__ = "Bonus"
        self.images = [self.image, pygame.transform.scale(self.image, (self.size * 15 // 16, self.size * 15 // 16)).copy()]
        self.poses = [(self.rect.x, self.rect.y), (self.rect.x + self.size // 32, self.rect.y + self.size // 32)]

    def set_up_2(self):
        self.image = pygame.Surface([0, 0])

    def update(self, events):
        self.play_animation()
        for sprite in pygame.sprite.spritecollide(self, self.group, False):
            if sprite == self:
                continue
            if sprite.__class__.__name__ == AI:
                self.ai_get(sprite)
                self.kill()
            if sprite.__class__.__name__ == PLAYER:
                self.player_get(sprite)
                self.kill()

    def play_animation(self):
        self.time += 1
        if self.time == BONUS_ANIMATION:
            self.time = 0
            self.rect.x, self.rect.y = self.poses[-1]
            self.image = self.images[0]
            self.images = self.images[::-1]
            self.poses = self.poses[::-1]

    def ai_get(self, sprite):
        pass

    def player_get(self, sprite):
        pass


class StarBonus(Bonus):
    def set_up_2(self):
        self.image = STAR_BONUS

    def ai_get(self, sprite):
        pass

    def player_get(self, sprite):
        sprite.upgrade()
