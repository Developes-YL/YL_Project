import pygame

from files.Objects.AI import AI
from files.Objects.Player import Player
from files.Objects.fields import Field1
from files.Support.Consts import FPS


class Game:
    def __init__(self, screen, player_count=1, level=0):
        self.level = level
        self.window_size = map(int, screen.get_size())
        self.screen = screen
        self.player_count = player_count

        self.cell_size = 30 # потом поправлю и добавлю настройку
        self.field = Field1(screen, level, self.cell_size)

        # рассчет времени появления ботов
        self.ai_time_max = (190 - level * 4 - (player_count - 1) * 20) * 60  # в секундах
        # self.ai = ... все боты
        self.ai_time = 0
        self.game_over = False

    def start(self):
        self.player_1 = Player(1, self.cell_size)
        if self.player_count == 2:
            self.player_2 = Player(2, self.cell_size)

    def render(self):
        self.field.render()
        self.player_1.render()
        if self.player_count == 2:
            self.player_2.render()
        # for bot in self.ai:
        #     bot.render()

    def process_events(self, events):
        # all_sprites.update()
        self.ai_time += 1 / FPS
        if self.ai_time >= self.ai_time_max:
            self.ai_time = 0
            # self.ai.append(AI())
        # if pygame.KEYDOWN in [event.type for event in events]:
        #    self.level += 1
        #    self.field = Field1(self.screen, self.level)
        #    if self.level >= 34:
        #        self.level = 0

    def reset(self):
        self.field.reset()
