import pygame.sprite

<<<<<<< Updated upstream
<<<<<<< Updated upstream
from files.Support.consts import AI, PLAYER, GAME_END_FREEZE
from files.Support.events import PAUSE, STOP_GAME
=======
from files.Support.consts import AI, PLAYER, GAME_END_FREEZE, BONUS_ANIMATION, BONUS_LIFE
from files.Support.events import PAUSE, STOP_GAME, BASE_DEGRADE, BASE_UPGRADE
>>>>>>> Stashed changes
=======
from files.Support.consts import AI, PLAYER, GAME_END_FREEZE, BONUS_ANIMATION, BONUS_LIFE
from files.Support.events import PAUSE, STOP_GAME, BASE_DEGRADE, BASE_UPGRADE
>>>>>>> Stashed changes
from files.Support.ui import *


class Cell(pygame.sprite.Sprite):
    def __init__(self, size, pos, group):
        self._layer = 0
        self.set_up()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.group = group
        super().__init__(group)
        group.change_layer(self, self._layer)

    def set_up(self):
        self.image = pygame.Surface([0, 0])

    def boom(self, flag) -> bool:
        return False


class Brick(Cell):
    def set_up(self):
        self.image = BRICK_IMAGE

    def boom(self, flag) -> bool:
        self.kill()
        return True

    def degrage(self, group):
        self.boom(False)

class Water(Cell):
    def set_up(self):
        self.image = WATER_IMAGE


class Concrete(Cell):
    def set_up(self):
        self.image = CONCRETE_IMAGE

    def boom(self, flag) -> bool:
        return True


class Bush(Cell):
    def set_up(self):
        self.image = BUSH_IMAGE
        self._layer = 3


class Ice(Cell):
    def set_up(self):
        self.image = ICE_IMAGE


class Base1(Cell):
    def set_up(self):
        self.image = BASE_1
        self.flag = True

    def boom(self, flag) -> bool:
        if self.flag:
            self.lose()
            self.flag = False
        return True

    def lose(self):
        # функция на пройгрыш
        pygame.time.set_timer(pygame.event.Event(PAUSE), 1, 1)
        pygame.time.set_timer(pygame.event.Event(STOP_GAME, game_over=True), GAME_END_FREEZE, 1)
        Base2(self.rect.size[0], (self.rect.x, self.rect.y), self.group)
        self.kill()


class Base2(Cell):
    def set_up(self):
        self.image = BASE_2

    def boom(self, flag):
        return True


class Bonus(Cell):
    def set_up(self):
        self.image = pygame.Surface([0, 0])
        self._layer = 3

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
        pass

    def ai_get(self, sprite):
        pass

    def player_get(self, sprite):
        pass
<<<<<<< Updated upstream
=======

    def _player_get(self, sprite):
        sprite.upgrade()


class Grenade(Bonus):
    def _set_up(self):
        self.image = GRENADE_BONUS


class Shovel(Bonus):
    def _set_up(self):
        self.image = SHOVEL_BONUS

    def _ai_get(self, sprite):
        pygame.time.set_timer(pygame.event.Event(BASE_DEGRADE), 1, 1)

    def _player_get(self, sprite):
        pygame.time.set_timer(pygame.event.Event(BASE_UPGRADE), 1, 1)

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
