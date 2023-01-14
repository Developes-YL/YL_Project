import random

import pygame

from files.Objects.AI import AI
from files.Objects.Player import Player
from files.Objects.fields import Field1
from files.Support.Consts import FPS
from files.Support.events import PAUSE, START_EFFECT_EVENT


class Game:
    def __init__(self, screen, player_count: int = 1, level: int = 0):
        self.level = level
        self.screen = screen
        self.player_count = player_count

        self.window_size = tuple(map(int, screen.get_size()))

        self.game_over = False
        self.pause = False

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.field = Field1(self.screen, self.all_sprites, self.level, self.window_size)
        self.cell_size = self.field.get_cell_size()
        self.positions = self.field.get_positions()

        self.player_1 = Player(self.all_sprites, 1, self.cell_size * 2, self.positions["player"][0])
        if self.player_count == 2:
            self.player_2 = Player(self.all_sprites, 2, self.cell_size * 2, self.positions["player"][1])

        self.queue = []
        self.load_queue()
        self.number_bot = 0

        # рассчет времени появления ботов в секундах
        self.ai_time_max = (190 - level * 4 - (player_count - 1) * 20) // 16
        self.ai_time = self.ai_time_max

        pygame.event.post(pygame.event.Event(START_EFFECT_EVENT))

        self.new_game()

    def load_queue(self):
        # загрузка очередности появления ботов
        ...
        self.queue = [0] * 20  # временно

    def new_game(self):
        self.all_sprites.empty()
        self.field.reset()

        self.ai_time = self.ai_time_max
        self.player_1 = Player(self.all_sprites, 1, self.cell_size * 2, self.positions["player"][0])
        if self.player_count == 2:
            self.player_2 = Player(self.all_sprites, 2, self.cell_size * 2, self.positions["player"][1])
        self.queue = [0] * 20  # временно


    def render(self):
        self.all_sprites.draw(self.screen)

    def process_events(self, events):
        self.all_sprites.update(events)
        if PAUSE in [event.type for event in events]:
            self.pause = not self.pause
        if self.pause:
            return
        self.ai_time += 1 / FPS
        if self.ai_time > self.ai_time_max and len(self.queue) > 0:
            self.ai_time = 0
            n = random.choice(range(3))
            ai = AI(self.all_sprites, self.cell_size * 2, self.positions["ai"][n],
                    self.queue[0], self.number_bot % 5 == 0)
            self.queue.pop(0)
            self.all_sprites.change_layer(ai, 1)
            self.number_bot += 1

    def get_size(self):
        return self.field.get_size()
