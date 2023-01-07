import pygame.sprite

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
