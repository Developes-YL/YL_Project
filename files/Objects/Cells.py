import pygame.sprite

from files.Support.ui import *


class Cell(pygame.sprite.Sprite):
    image = pygame.Surface([0, 0])

    def __init__(self, size, pos, group):
        self.type = "None"
        super().__init__(group)
        self.image = pygame.transform.scale(Cell.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def get_type(self):
        return "None"


class Brick(pygame.sprite.Sprite):
    image = BRICK

    def __init__(self, size, pos, group):
        super().__init__(group)
        self.image = pygame.transform.scale(Brick.image, (size, size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Water(pygame.sprite.Sprite):
    image = WATER

    def __init__(self, size, pos, group):
        super().__init__(group)
        self.image = pygame.transform.scale(Water.image, (size, size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Concrete(pygame.sprite.Sprite):
    image = CONCRETE

    def __init__(self, size, pos, group):
        super().__init__(group)
        self.image = pygame.transform.scale(Concrete.image, (size, size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Forest(pygame.sprite.Sprite):
    image = FOREST

    def __init__(self, size, pos, group):
        super().__init__(group)
        self.image = pygame.transform.scale(Forest.image, (size, size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Ice(pygame.sprite.Sprite):
    image = ICE

    def __init__(self, size, pos, group):
        super().__init__(group)
        self.image = pygame.transform.scale(Ice.image, (size, size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
