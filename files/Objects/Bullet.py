import pygame

from files.Objects.explosions import Explosion
from files.Support.consts import UP, RIGHT, DOWN, LEFT, CONCRETE
from files.Support.events import PAUSE
from files.Support.ui import BULLET_IMAGE


class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, rect: pygame.rect.Rect, speed: int = 30, direction: int = DOWN,
                 from_player: bool = True, mega: bool = False):
        super().__init__(group)
        # сохранение начальных значений
        self.group = group
        pos, self.size = [rect.x, rect.y], rect.size[0]
        self.speed = speed
        self.direction = direction
        self.from_player = from_player
        self.mega = mega

        # настройка спрайта
        size = self.size // 3, self.size // 3
        self.image = pygame.transform.scale(BULLET_IMAGE, size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.image = pygame.transform.rotate(self.image, -90 * self.direction)

        # выставление начальной позиции относительно направления
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
        self.rect.y += self.speed[1]  # speed всегда содержит 1 ноль, потому перемещение всегда по одной оси

        destroy = False
        for sprite in pygame.sprite.spritecollide(self, self.group, False):
            if sprite == self:
                continue
                
            if sprite.__class__.__name__ == CONCRETE:
                # уничтожение пули происходит только при достижении игроком 3 уровня апгрейда
                destroy = True
                sprite.boom(self.mega)
            else:
                try:
                    destroy = sprite.boom(self.from_player)  # попытка уничтожения препятствия
                except AttributeError:
                    pass

        if destroy:
            self.kill()

    def boom(self, flag: bool = True):
        if flag != self.from_player:
            self.kill()
            return True
        return False

    def kill(self, with_explosion: bool = True):
        if with_explosion:
            explosion = Explosion(self.group, self.size, (self.rect.x, self.rect.y))
            self.group.change_layer(explosion, 2)
        super().kill()
