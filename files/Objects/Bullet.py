import pygame

from files.Objects.explosions import Explosion
from files.Support.consts import UP, RIGHT, DOWN, LEFT, CONCRETE
from files.Support.events import PAUSE
from files.Support.ui import BULLET_IMAGE


class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed, direction, rect, group, from_player=True, mega=False):
        self._layer = 1
        super().__init__(group)
        self.from_player = from_player
        self.group = group
        pos, self.size = [rect.x, rect.y], rect.size[0]
        size = self.size // 3, self.size // 3
        self.image = pygame.transform.scale(BULLET_IMAGE, size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.speed = speed
        self.mega = mega
        self.direction = direction
        self.image = pygame.transform.rotate(self.image, -90 * self.direction)
        if direction == UP:
            self.speed = [0, -speed]
            self.rect.x += self.size // 2 - self.size // 6
            self.rect.y -= self.size // 3
        if direction == DOWN:
            self.speed = [0, speed]
            self.rect.x += self.size // 2 - self.size // 6
            self.rect.y += self.size
        if direction == RIGHT:
            self.speed = [speed, 0]
            self.rect.y += self.size // 2 - self.size // 6
            self.rect.x += self.size
        if direction == LEFT:
            self.speed = [-speed, 0]
            self.rect.y += self.size // 2 - self.size // 6
            self.rect.x -= self.size // 3
        self.pause = False

    def update(self, events):
        if PAUSE in [event.type for event in events]:
            self.pause = not self.pause
        if self.pause:
            return

        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        flag = False
        for sprite in pygame.sprite.spritecollide(self, self.group, False):
            if sprite == self:
                continue
            if sprite.__class__.__name__ == CONCRETE:
                flag = True
                sprite.boom(self.mega)
            else:
                try:
                    flag = sprite.boom(self.from_player)
                except AttributeError:
                    pass

        if flag:
            self.kill()

    def boom(self, flag):
        self.kill()
        return True

    def kill(self, with_explosion=True):
        if with_explosion:
            exp = Explosion(self.group, self.size, self.rect.x, self.rect.y)
            self.group.change_layer(exp, 2)
        super().kill()
