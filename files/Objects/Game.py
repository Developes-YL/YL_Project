import random

import pygame

from files.Objects.AI import AI
from files.Objects.Player import Player
from files.Objects.fields import Field1
from files.Support.Consts import FPS


class Game:
    def __init__(self, screen, player_count=1, level=0):
        self.level = level
        self.screen = screen
        self.player_count = player_count
        self.game_over = False
        self.window_size = list(map(int, screen.get_size()))

        self.new_game()

        # рассчет времени появления ботов в секундах
        self.ai_time_max = (190 - level * 4 - (player_count - 1) * 20) // 10
        self.ai_time = self.ai_time_max

    def new_game(self):
        self.game_over = False

        self.all_sprites = pygame.sprite.Group()
        self.field = Field1(self.screen, self.all_sprites, self.level, self.window_size)
        self.cell_size = self.field.get_cell_size()

        self.positions = self.field.get_positions()

        self.ai_time = 0
        self.player_1 = Player(self.all_sprites, 1, self.cell_size * 2, self.positions["player"][0])
        if self.player_count == 2:
            self.player_2 = Player(self.all_sprites, 2, self.cell_size * 2, self.positions["player"][1])

    def render(self):
        self.all_sprites.draw(self.screen)

    def process_events(self, events):
        self.all_sprites.update()
        self.ai_time += 1 / FPS
        print(self.ai_time)
        if self.ai_time >= self.ai_time_max:
            self.ai_time = 0
            print("-" * 100)
            n = random.randrange(0, 3)
            AI(self.cell_size * 2, self.positions["ai"][n], self.all_sprites)
