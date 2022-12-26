import pygame.sprite

from files.Support.ui import TANK


class AI(pygame.sprite.Sprite):
    def __init__(self, size, pos, group):
        super().__init__(group)
        self.image = TANK
        self.rect = (*pos, size, size)
        self.image = pygame.transform.scale(TANK, (size, size))
