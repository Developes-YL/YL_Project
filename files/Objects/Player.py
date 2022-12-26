import pygame.sprite

from files.Support.ui import TANK


class Player(pygame.sprite.Sprite):
    def __init__(self, group, number=1, cell_size=30, pos=(0, 0)):
        super().__init__(group)
        self.number = number
        self.rect = (*pos, cell_size, cell_size)
        self.image = pygame.transform.scale(TANK, (cell_size, cell_size))


class Bullet:
    pass
