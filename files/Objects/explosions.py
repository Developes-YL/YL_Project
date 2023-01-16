import pygame

from files.Support.events import PAUSE
from files.Support.ui import EXPLOSION_2, EXPLOSION_3, EXPLOSION_1


class Explosion(pygame.sprite.Sprite):
    def __init__(self, group, size: int = 30, pos: tuple = (0, 0)):
        super().__init__(group)
        self.size = size
        self.x, self.y = pos

        self.image = pygame.transform.scale(EXPLOSION_1, (size // 2, size // 2))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0] - size // 4, pos[1] - size // 4

        self.time = 0
        self.death_time_1 = 2
        self.death_time_2 = 5

        self.pause = False

    def update(self, events):
        if PAUSE in [event.type for event in events]:
            self.pause = not self.pause
        if self.pause:
            return

        self.time += 1
        if self.death_time_2 > self.time > self.death_time_1:
            # смена спрайта
            self.image = pygame.transform.scale(EXPLOSION_2, (self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.x - self.size // 2, self.y - self.size // 2
        elif self.time > self.death_time_2:
            # завершение анимации
            self.kill()


class BigExplosion(pygame.sprite.Sprite):
    def __init__(self, group, size, pos):
        super().__init__(group)
        self.size = size
        self.x, self.y = pos
        self.image = pygame.Surface([0, 0])
        self.rect = self.image.get_rect()

        self.time = 0
        self.start_time = 4
        self.death_time = 8
        self.pause = False

    def update(self, events):
        if PAUSE in [event.type for event in events]:
            self.pause = not self.pause
        if self.pause:
            return

        self.time += 1
        if self.death_time > self.time > self.start_time:
            # спрайт появядяется спустя какое то время
            self.image = pygame.transform.scale(EXPLOSION_3, (self.size * 5 // 4, self.size * 5 // 4))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.x - self.size // 8, self.y - self.size // 8
        elif self.time > self.death_time:
            self.kill()
