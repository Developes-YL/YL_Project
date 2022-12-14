import pygame.sprite

from files.Support.Consts import *
from files.Support.events import PAUSE
from files.Support.ui import TANK, BULLET_IMAGE, EXPLOSION_1, EXPLOSION_2, EXPLOSION_3


class Player(pygame.sprite.Sprite):
    def __init__(self, group, number=1, cell_size=30, pos=(0, 0)):
        super().__init__(group)
        self.group = group
        self.number = number
        self.start = pos
        self.lives = 3
        self.rect = pygame.Rect(*pos, cell_size, cell_size)
        self.image = pygame.transform.scale(TANK, (cell_size, cell_size))

    def boom(self, flag):
        if not flag:
            self.lives -= 1
            exp = BigExplosion(self.group, self.rect[3], self.rect[0], self.rect[1])
            self.group.change_layer(exp, 2)
            if self.lives > 0:
                Player(self.group, self.number, self.rect[3], self.start)
                self.kill()
        return True


class PlayerDemo:
    def __init__(self, pos1, pos2):
        self.pu = pygame.image.load('ggu.png')
        self.ggd = pygame.transform.rotate(self.pu, 180)
        self.ggl = pygame.transform.rotate(self.pu, 90)
        self.ggr = pygame.transform.rotate(self.pu, 270)
        self.px = pos1 * 10
        self.py = pos2 * 10
        self.orient = 1
        self.hp = 100
        self.lives = 3
        self.move = 0
        self.wall = 0
        self.rect = pygame.Rect(self.px * 2, self.py * 2, 20, 20)
        self.power = 2

    def moveP(self, key):
        if self.orient == 1 and self.wall != 1:
            if key == 1:
                self.py -= 1
                self.wall = 0
            elif key != 0:
                self.orient = key
                self.move = 0
            if (self.py % 10) == 0:
                key = 0
                self.move = 0

            elif key == 0:
                self.py -= 1
                self.move = 1

        elif self.orient == 2 and self.wall != 2:
            if key == 2:
                self.py += 1
                self.wall = 0
            elif key != 0:
                self.orient = key
                self.move = 0
            if (self.py % 10) == 0:
                key = 0
                self.move = 0

            elif key == 0:
                self.py += 1
                self.move = 1

        elif self.orient == 3 and self.wall != 3:
            if key == 3:
                self.px -= 1
                self.wall = 0
            elif key != 0:
                self.orient = key
                self.move = 0
            if (self.px % 10) == 0:
                key = 0
                self.move = 0

            elif key == 0:
                self.px -= 1
                self.move = 1

        elif self.orient == 4 and self.wall != 4:
            if key == 4:
                self.px += 1
                self.wall = 0
            elif key != 0:
                self.orient = key
                self.move = 0
            if (self.px % 10) == 0:
                key = 0
                self.move = 0

            elif key == 0:
                self.px += 1
                self.move = 1

        else:
            self.move = 0
        self.rect = pygame.Rect(self.px * 2, self.py * 2, 20, 20)

    def walls(self, matrix):
        if (self.py % 10) == 0 and (self.px % 10) == 0:
            Y_axisd = matrix[self.py // 10 + 1][self.px // 10]
            Y_axisu = matrix[self.py // 10 - 1][self.px // 10]
            X_axisr = matrix[self.py // 10][self.px // 10 + 1]
            X_axisl = matrix[self.py // 10][self.px // 10 - 1]
            if (Y_axisd == 1 or Y_axisd == 2 or Y_axisd == 4 or Y_axisd == 6) and self.orient == 2:
                self.wall = 2
            elif (Y_axisu == 1 or Y_axisu == 2 or Y_axisu == 4 or Y_axisu == 6) and self.orient == 1:
                self.wall = 1
            elif (X_axisr == 1 or X_axisr == 2 or X_axisr == 4 or X_axisr == 6) and self.orient == 4:
                self.wall = 4
            elif (X_axisl == 1 or X_axisl == 2 or X_axisl == 4 or X_axisl == 6) and self.orient == 3:
                self.wall = 3

    def render(self, screen):
        screen.blit(self.pu, (self.px * 2, self.py * 2))

    def touch(self, i):
        if self.orient == 1:
            if self.px == enemyes[i].x and self.py - 10 == enemyes[i].y:
                self.wall = 1
                return True
            return False
        elif self.orient == 2:
            if self.px == enemyes[i].x and self.py + 10 == enemyes[i].y:
                self.wall = 2
                return True
            return False
        elif self.orient == 3:
            if self.px - 10 == enemyes[i].x and self.py == enemyes[i].y:
                self.wall = 3
                return True
            return False
        elif self.orient == 4:
            if self.px + 10 == enemyes[i].x and self.py == enemyes[i].y:
                self.wall = 4
                return True
            return False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed, direction, rect, group, from_player=True):
        self._layer = 1
        super().__init__(group)
        self.from_player = from_player
        self.group = group
        pos, self.size = [rect.x, rect.y], rect.size[0]
        self.image = pygame.transform.scale(BULLET_IMAGE, (self.size // 8, self.size // 8))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.speed = speed
        self.direction = direction
        self.image = pygame.transform.rotate(self.image, 90 * self.direction)
        if direction == UP:
            self.speed = [0, -speed]
            self.rect.x += self.size // 2 - self.size // 16
            self.rect.y -= self.size // 8
        if direction == DOWN:
            self.speed = [0, speed]
            self.rect.x += self.size // 2 - self.size // 16
            self.rect.y += self.size
        if direction == RIGHT:
            self.speed = [speed, 0]
            self.rect.y += self.size // 2 - self.size // 16
            self.rect.x += self.size
        if direction == LEFT:
            self.speed = [-speed, 0]
            self.rect.y += self.size // 2 - self.size // 16
            self.rect.x -= self.size // 8
        self.pause = False

    def update(self, *events):
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

            else:
                try:
                    flag = sprite.boom(self.from_player)
                except:
                    pass

        if flag:
            self.kill()

    def boom(self, flag):
        self.kill()

    def kill(self, with_explosion=True):
        if with_explosion:
            exp = Explosion(self.group, self.size, self.rect.x, self.rect.y)
            self.group.change_layer(exp, 2)
        super().kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, group, size, x, y):
        super().__init__(group)
        self.size = size
        self.x, self.y = x, y
        self.image = pygame.transform.scale(EXPLOSION_1, (size // 2, size // 2))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x - size // 4, y - size // 4
        self.time = 0
        self.death_time_1 = 2
        self.death_time_2 = 5
        self.pause = False

    def update(self, *events):
        if PAUSE in [event.type for event in events]:
            self.pause = not self.pause
        if self.pause:
            return

        self.time += 1
        if self.time > self.death_time_2:
            self.kill()
        elif self.time > self.death_time_1:
            self.image = pygame.transform.scale(EXPLOSION_2, (self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.x - self.size // 2, self.y - self.size // 2


class BigExplosion(pygame.sprite.Sprite):
    def __init__(self, group, size, x, y):
        super().__init__(group)
        self.size = size
        self.x, self.y = x, y
        self.image = pygame.Surface([0, 0])
        self.rect = self.image.get_rect()
        self.time = 0
        self.start_time = 4
        self.death_time = 8
        self.pause = False

    def update(self, *events):
        if PAUSE in [event.type for event in events]:
            self.pause = not self.pause
        if self.pause:
            return

        self.time += 1
        if self.time > self.death_time:
            self.kill()
        elif self.time > self.start_time:
            self.image = pygame.transform.scale(EXPLOSION_3, (self.size * 5 // 4, self.size * 5 // 4))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.x - self.size // 8, self.y - self.size // 8
