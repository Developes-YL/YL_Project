import pygame.sprite

from files.Support.events import GAME_OVER_EVENT, PAUSE
from files.Support.ui import *


class Cell(pygame.sprite.Sprite):
    def __init__(self, size, pos, group):
        self._layer = 0
        self.set_up()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
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

    def boom(self, flag) -> bool:
        self.kill()
        return True


class Water(Cell):
    def set_up(self):
        self.image = WATER_IMAGE


class Concrete(Cell):
    def set_up(self):
        self.image = CONCRETE_IMAGE

    def boom(self, flag) -> bool:
        return True


class Bush(Cell):
    def set_up(self):
        self.image = BUSH_IMAGE
        self._layer = 3


class Ice(Cell):
    def set_up(self):
        self.image = ICE_IMAGE


class Base1(Cell):
    def set_up(self):
        self.image = BASE_1
        self.flag = True

    def boom(self, flag) -> bool:
        if self.flag:
            self.lose()
            self.flag = False
        return True

    def lose(self):
        # функция на пройгрыш
        pygame.event.post(pygame.event.Event(GAME_OVER_EVENT))
        Base2(self.rect.size[0], (self.rect.x, self.rect.y), self.group)
        self.kill()


class Base2(Cell):
    def set_up(self):
        self.image = BASE_2

    def boom(self, flag):
        return True
