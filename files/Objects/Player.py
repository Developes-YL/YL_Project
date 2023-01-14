import pygame.sprite

from files.Support.Consts import *
from files.Support.events import PAUSE, PLAYER_KILLED
from files.Support.ui import TANK_PLAYER, BULLET_IMAGE, EXPLOSION_1, EXPLOSION_2, EXPLOSION_3


class Player(pygame.sprite.Sprite):
    def __init__(self, group, number=1, size=30, pos=(0, 0)):

        # сохранение начальных значений
        self.group = group
        self.size = size * TANK_SIZE_KOEF
        self.cell_size = size
        self.pos = pos
        self.start = pos
        self.number = number

        # настройка спрайтов и анимаций
        self.images = list(map(lambda x: pygame.transform.scale(x, (self.size, self.size)),
                               TANK_PLAYER[0])).copy()
        self.default_images = self.images.copy()

        self.animation_time = 0

        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(0, 0, 0, 0)

        # стартовые значения
        self.lives = 1

        self.pause = False
        self.direction = UP
        self.freeze = 0

        self.speed = size * TANK_SPEED // 1
        self.is_move = False

        # стрельба
        self.fire_time = 0
        self.reload_time = RELOAD_TIME
        self.bullet_speed = int(self.size * BULLET_SPEED)

        self.spawned = False

        if number == 1:
            self.buttons = [pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_SPACE]
        if number == 2:
            self.buttons = [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_KP_0]

        super().__init__(group)
        self.rotate()

    def boom(self, flag):
        if not flag:
            self.lives -= 1
            exp = BigExplosion(self.group, self.cell_size, self.rect[0], self.rect[1])
            self.group.change_layer(exp, 2)
            if self.lives > 0:
                Player(self.group, self.number, self.cell_size, self.start)
            else:
                pygame.time.set_timer(pygame.event.Event(PLAYER_KILLED), 1, 1)
            self.kill()
        return True

    def update(self, events):
        if not self.spawned:
            self.spawn()
        if not self.spawned:
            return
        if PAUSE in [event.type for event in events]:
            self.pause = not self.pause
        if self.pause:
            return

        if self.freeze != 0:
            self.freeze -= 1
        else:
            self.animation_time += 1
            self.fire_time += 1

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == self.buttons[0]:
                self.direction = UP
                self.is_move = True
                self.rotate()
            if event.type == pygame.KEYDOWN and event.key == self.buttons[1]:
                self.direction = LEFT
                self.is_move = True
                self.rotate()
            if event.type == pygame.KEYDOWN and event.key == self.buttons[2]:
                self.direction = RIGHT
                self.is_move = True
                self.rotate()
            if event.type == pygame.KEYDOWN and event.key == self.buttons[3]:
                self.direction = DOWN
                self.is_move = True
                self.rotate()
            if event.type == pygame.KEYUP and event.key in self.buttons[:4]:
                self.is_move = False
            if event.type == pygame.KEYDOWN and event.key == self.buttons[4]:
                if self.fire_time > RELOAD_TIME:
                    self.make_shot(self.direction)
        if self.is_move:
            self.move()
            if self.animation_time > MOVE_ANIMATION:
                self.animation_time = 0
                self.image = self.images[0]
                self.images[:2] = self.images[:2][::-1]

    def move(self):
        coord = self.rect.x, self.rect.y
        speed = self.speed

        if ICE in [a.__class__.__name__ for a in pygame.sprite.spritecollide(self, self.group, False)]:
            speed = int(speed * SPEED_ON_ICE)

        if self.direction == UP:
            self.rect.y -= speed
        if self.direction == DOWN:
            self.rect.y += speed
        if self.direction == LEFT:
            self.rect.x -= speed
        if self.direction == RIGHT:
            self.rect.x += speed

        sprites = pygame.sprite.spritecollide(self, self.group, False)
        for sprite in sprites:
            if sprite.__class__.__name__ not in NON_CONFLICT_OBJECTS:
                if sprite == self:
                    continue
                self.is_move = False
                self.rect.x, self.rect.y = coord
                break

    def make_shot(self, direction):
        self.fire_time = 0
        Bullet(self.bullet_speed, direction, self.rect, self.group, True)

    def rotate(self):
        self.images[0] = pygame.transform.rotate(self.default_images[0], -90 * self.direction)
        self.images[1] = pygame.transform.rotate(self.default_images[1], -90 * self.direction)

    def spawn(self):
        # анимация появление запускается только если рядом нет танков
        sprite = pygame.sprite.Sprite()
        sprite.rect = self.images[0].get_rect()
        sprite.rect.x, sprite.rect.y = self.pos
        if len(pygame.sprite.spritecollide(sprite, self.group, False)) == 0:
            self.image = self.images[0]
            self.rect = self.images[0].get_rect()
            self.rect.x, self.rect.y = self.pos
            self.spawned = True
        del sprite


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
        self.image = pygame.transform.rotate(self.image, -90 * self.direction)
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

    def update(self, events):
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

    def update(self, events):
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
