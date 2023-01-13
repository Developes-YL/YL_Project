import pygame.sprite

from files.Support.Consts import *
from files.Support.events import PAUSE
from files.Support.ui import TANK, BULLET_IMAGE, EXPLOSION_1, EXPLOSION_2, EXPLOSION_3, TANK_PLAYER_1

class Player(pygame.sprite.Sprite):
    def __init__(self, group, number=1, cell_size=30, pos=(0, 0)):
        super().__init__(group)
        self.group = group
        self.number = number
        self.start = pos
        self.lives = 3
        self.rect = pygame.Rect(*pos, cell_size * 90 // 100, cell_size * 90 // 100)
        self.normal_image = pygame.transform.scale(TANK, (cell_size * 90 // 100, cell_size * 90 // 100))
        self.speed = cell_size // 32
        self.d = 'up'
        self.bullet_speed = int(cell_size * BULLET_SPEED)
        self.direction = UP
        self.pos = pos[0], pos[1]
        self.is_move = False
        self.image = pygame.transform.rotate(self.normal_image, 90).copy()
        self.fire_time = 0
        self.pause = False
        if number == 1:
            self.buttons = [pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_SPACE]
        if number == 2:
            self.buttons = [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_RSHIFT]
        self.images = list(map(lambda x: pygame.transform.scale(x, (cell_size * 90 // 100, cell_size * 90 // 100)), TANK_PLAYER_1)).copy()
        self.animation_time = 0
        self.frame_rate = 3

    def boom(self, flag):
        if not flag:
            self.lives -= 1
            exp = BigExplosion(self.group, self.rect[3], self.rect[0], self.rect[1])
            self.group.change_layer(exp, 2)
            if self.lives > 0:
                Player(self.group, self.number, self.rect[3], self.start)
                self.kill()
        return True

    def update(self, events):
        self.frame_rate -= 1
        if PAUSE in [event.type for event in events]:
            self.pause = not self.pause
        if self.pause:
            return
        self.fire_time += 1
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == self.buttons[0]:
                self.d = 'up'
                self.direction = UP
                self.is_move = True
                self.rotate()
            if event.type == pygame.KEYDOWN and event.key == self.buttons[1]:
                self.d = 'left'
                self.direction = LEFT
                self.is_move = True
                self.rotate()
            if event.type == pygame.KEYDOWN and event.key == self.buttons[2]:
                self.d = 'right'
                self.direction = RIGHT
                self.is_move = True
                self.rotate()
            if event.type == pygame.KEYDOWN and event.key == self.buttons[3]:
                self.d = 'down'
                self.direction = DOWN
                self.is_move = True
                self.rotate()
            if event.type == pygame.KEYUP and event.key == self.buttons[0]:
                self.is_move = False
            if event.type == pygame.KEYUP and event.key == self.buttons[1]:
                self.is_move = False
            if event.type == pygame.KEYUP and event.key == self.buttons[2]:
                self.is_move = False
            if event.type == pygame.KEYUP and event.key == self.buttons[3]:
                self.is_move = False
            if event.type == pygame.KEYDOWN and event.key == self.buttons[4]:
                if self.fire_time > RELOAD_TIME:
                    self.fire_time = 0
                    if self.direction == UP:
                        self.make_shot(UP)
                    if self.direction == DOWN:
                        self.make_shot(DOWN)
                    if self.direction == LEFT:
                        self.make_shot(LEFT)
                    if self.direction == RIGHT:
                        self.make_shot(RIGHT)
        if self.is_move:
            self.move()
            if self.animation_time > MOVE_ANIMATION:
                self.animation_time = 0
                self.image = self.images[0]
                self.images[:2] = self.images[:2][::-1]

        if self.frame_rate == 0:
            self.animation_time += 1
            self.frame_rate = MOVE_ANIMATION



    def move(self):
        coord = self.rect.x, self.rect.y
        speed = self.speed
        if ICE in [a.__class__.__name__ for a in pygame.sprite.spritecollide(self, self.group, False)]:
            speed = int(speed * SPEED_ON_ICE)

        if self.d == 'up':
            self.rect.y -= speed
        if self.d == 'down':
            self.rect.y += speed
        if self.d == 'left':
            self.rect.x -= speed
        if self.d == 'right':
            self.rect.x += speed

        sprites = pygame.sprite.spritecollide(self, self.group, False)
        for sprite in sprites:
            if sprite.__class__.__name__ not in NON_CONFLICT_OBJECTS:
                if sprite == self:
                    continue
                self.is_move = False
                print(sprite.__class__.__name__)

                self.rect.x, self.rect.y = coord
                break

    def make_shot(self, dir):
        Bullet(self.bullet_speed, dir, self.rect, self.group, True)

    def rotate(self):
        self.image = pygame.transform.rotate(self.normal_image, 90 * self.direction)
        self.images = [pygame.transform.rotate(pygame.transform.scale(TANK_PLAYER_1[0], (75, 75)), 90 * self.direction),
                       pygame.transform.rotate(pygame.transform.scale(TANK_PLAYER_1[1], (75, 75)), 90 * self.direction)]

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
