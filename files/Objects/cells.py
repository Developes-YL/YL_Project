import pygame.sprite

from files.Support.consts import AI, PLAYER, GAME_END_FREEZE, BONUS_ANIMATION, BONUS_LIFE
from files.Support.events import PAUSE, STOP_GAME
from files.Support.ui import *


class Cell(pygame.sprite.Sprite):
    def __init__(self, group, size, pos):
        self.group = group
        self.size = size
        self.rect = pygame.Rect(*pos, size, size)

        self._layer = 0
        self.rect = pygame.Rect(0, 0, 0, 0)
        self._set_up()

        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = pygame.Rect(*pos, size, size)
        super().__init__(group)
        group.change_layer(self, self._layer)

    def _set_up(self):
        self.image = pygame.Surface([0, 0])

    def boom(self, flag) -> bool:
        """реакция на столкновение пулей"""
        return False


class Brick(Cell):
    def _set_up(self):
        self.image = BRICK_IMAGE

    def boom(self, flag) -> bool:
        self.image = pygame.transform.scale(self.image, (0, 0))
        pos = self.rect.x, self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        return True

    def upgrade(self, group):
        """улучшение кирпича до бетона"""
        group[group.index(self)] = Concrete(self.group, self.size, (self.rect.x, self.rect.y))
        self.kill()


class Water(Cell):
    def _set_up(self):
        self.image = WATER_IMAGE


class Concrete(Cell):
    def _set_up(self):
        self.image = CONCRETE_IMAGE

    def boom(self, mega: bool = False) -> bool:
        if mega:
            self.kill()
        return True

    def degrade(self, group):
        """возврат к кирпичу"""
        group[group.index(self)] = Brick(self.group, self.size, (self.rect.x, self.rect.y))
        self.kill()

    def upgrade(self, group):
        pass


class Bush(Cell):
    def _set_up(self):
        self.image = BUSH_IMAGE
        self._layer = 3


class Ice(Cell):
    def _set_up(self):
        self.image = ICE_IMAGE


class Base1(Cell):
    def _set_up(self):
        self.image = BASE_1_IMAGE
        self.flag = True

    def boom(self, from_player: bool = False) -> bool:
        if self.flag:
            self.lose()
            self.flag = False
        return True

    def lose(self):
        """уничтожение базы"""
        pygame.time.set_timer(pygame.event.Event(PAUSE), 1, 1)
        pygame.time.set_timer(pygame.event.Event(STOP_GAME, game_over=True), GAME_END_FREEZE, 1)
        Base2(self.group, self.rect.size[0], (self.rect.x, self.rect.y))
        self.kill()


class Base2(Cell):
    def _set_up(self):
        self.image = BASE_2_IMAGE

    def boom(self, flag):
        return True


class Bonus(Cell):
    def _set_up(self):
        self.set_up_2()
        self._layer = 4
        self.time = 0
        self.__class__.__name__ = "Bonus"

        self.image = pygame.transform.scale(self.image, (self.size, self.size)).copy()
        self.images = [self.image, pygame.transform.scale(self.image,
                                                          (self.size * 15 // 16, self.size * 15 // 16)).copy()]
        self.poses = [(self.rect.x, self.rect.y), (self.rect.x + self.size // 32, self.rect.y + self.size // 32)][::-1]

    def set_up_2(self):
        self.image = pygame.Surface([0, 0])

    def update(self, events):
        self.play_animation()
        for sprite in pygame.sprite.spritecollide(self, self.group, False):
            if sprite == self:
                continue
            if sprite.__class__.__name__ == AI:
                self.ai_get(sprite)
                self.kill()
            if sprite.__class__.__name__ == PLAYER:
                self.player_get(sprite)
                self.kill()

    def play_animation(self):
        self.time += 1
        print(self.time, BONUS_LIFE)
        if self.time % BONUS_ANIMATION == 0:
            self.rect.x, self.rect.y = self.poses[-1]
            self.image = self.images[0]
            self.images = self.images[::-1]
            self.poses = self.poses[::-1]
        if self.time == BONUS_LIFE:
            self.kill()

    def ai_get(self, sprite):
        pass

    def player_get(self, sprite):
        pass


class Star(Bonus):
    def set_up_2(self):
        self.image = STAR_BONUS

    def ai_get(self, sprite):
        pass

    def player_get(self, sprite):
        sprite.upgrade()


class Grenade(Bonus):
    def set_up_2(self):
        self.image = GRENADE_BONUS


class Shovel(Bonus):
    def set_up_2(self):
        self.image = SHOVEL_BONUS
