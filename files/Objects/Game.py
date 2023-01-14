import random

import pygame

from files.Objects.AI import AI
from files.Objects.Player import Player
from files.Objects.fields import Field1
from files.Support.Consts import FPS, GAME_END_FREEZE, LEVELS_COUNT
from files.Support.events import PAUSE, START_EFFECT_EVENT, AI_DESTROYED, WIN_WINDOW, STOP_GAME, GAME_OVER_WINDOW, \
    PLAYER_KILLED


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

        self.queue = []
        self.count_ai = 0
        self.kills = 0
        self.load_queue()
        self.number_bot = 0
        self.players_killed = 0

        # рассчет времени появления ботов в секундах
        self.ai_time_max = (190 - level * 4 - (player_count - 1) * 20) // 16
        self.ai_time = self.ai_time_max

        pygame.event.post(pygame.event.Event(START_EFFECT_EVENT))
        self.new_game()

    def load_queue(self):
        # загрузка очередности появления ботов
        ...
        self.queue = [0] * 1  # временно
        self.count_ai = 1

    def new_game(self):
        self.pause = False
        self.score = 0
        self.freeze = 0
        self.kills = 0
        self.players_killed = 0
        self.number_bot = 0
        self.all_sprites.empty()
        self.field.reset()

        self.ai_time = self.ai_time_max
        self.player_1 = Player(self.all_sprites, 1, self.cell_size * 2, self.positions["player"][0])
        if self.player_count == 2:
            self.player_2 = Player(self.all_sprites, 2, self.cell_size * 2, self.positions["player"][1])

        self.queue = 0
        self.load_queue()

    def render(self):
        self.all_sprites.draw(self.screen)

    def process_events(self, events):
        for event in events:
            if event.type == STOP_GAME:
                settings = self.score, self.player_count, min(self.level + 1, LEVELS_COUNT - 1)
                if event.game_over:
                    pygame.time.set_timer(pygame.event.Event(WIN_WINDOW, settings=settings), 1, 1)
                else:
                    pygame.time.set_timer(pygame.event.Event(GAME_OVER_WINDOW, settings=settings), 1, 1)
        self.all_sprites.update(events)
        if PAUSE in [event.type for event in events]:
            self.pause = not self.pause
        if self.pause:
            return
        if PLAYER_KILLED in [event.type for event in events]:
            self.players_killed += 1
            if self.players_killed == self.player_count:
                pygame.time.set_timer(pygame.event.Event(PAUSE), 1, 1)
                pygame.time.set_timer(pygame.event.Event(STOP_GAME, game_over=True), GAME_END_FREEZE, 1)
        if AI_DESTROYED in [event.type for event in events]:
            self.kills += 1
            if self.kills == self.count_ai:
                pygame.time.set_timer(pygame.event.Event(PAUSE), 1, 1)
                pygame.time.set_timer(pygame.event.Event(STOP_GAME, game_over=False), GAME_END_FREEZE, 1)
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
