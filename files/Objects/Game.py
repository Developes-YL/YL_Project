import random

import pygame

from files.Objects.AI import AI
from files.Objects.Player import Player
from files.Objects.cells import StarBonus
from files.Objects.fields import Field1
from files.Support.consts import FPS, GAME_END_FREEZE, LEVELS_COUNT, UPGRADE_CELLS_TIME, BONUS_TIME
from files.Support.events import PAUSE, START_EFFECT_EVENT, AI_DESTROYED, WIN_WINDOW, STOP_GAME, GAME_OVER_WINDOW, \
    PLAYER_KILLED, PLAYER_GET_BONUS, BASE_UPGRADE, BASE_DEGRADE


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
        self.bonus_time = 0
        self.number_bot = 0
        self.players_killed = 0

        # рассчет времени появления ботов в секундах
        self.ai_time_max = (190 - level * 4 - (player_count - 1) * 20) // 16
        self.ai_time = self.ai_time_max

        pygame.event.post(pygame.event.Event(START_EFFECT_EVENT))
        self.new_game()

    def load_queue(self):
        # загрузка очередности появления ботов
        with open("./Support/ai_queue.txt", 'r') as f:
            queue = list(map(int, f.readlines()[self.level + 1].split(";")[:-1]))
            self.queue = [*[0] * queue[0], *[1] * queue[1], *[2] * queue[2], *[3] * queue[3]]
            random.shuffle(self.queue)
        self.count_ai = len(self.queue)

    def get_score(self):
        return self.score

    def new_game(self):
        self.pause = False
        self.score = 0
        self.freeze = 0
        self.bonus_time = 0
        self.kills = 0
        self.players_killed = 0
        self.number_bot = 0
        self.all_sprites.empty()
        self.field.reset()

        self.ai_time = self.ai_time_max
        self.players = [0] * 2
        self.players[0] = Player(self.players, self.all_sprites, 1, self.cell_size * 2, self.positions["player"][0])
        if self.player_count == 2:
            self.players[1] = Player(self.players, self.all_sprites, 2, self.cell_size * 2, self.positions["player"][1])

        self.queue = 0
        self.load_queue()

    def render(self):
        self.all_sprites.draw(self.screen)

    def process_events(self, events):
        if [event for event in events if event.type == pygame.KEYDOWN if event.key == pygame.K_k]:
            pygame.time.set_timer(pygame.event.Event(STOP_GAME, game_over=True), 1, 1)
        if BASE_UPGRADE in [event.type for event in events]:
            self.field.upgrade_base_cells()
            pygame.time.set_timer(pygame.event.Event(BASE_DEGRADE), UPGRADE_CELLS_TIME, 1)
        if BASE_DEGRADE in [event.type for event in events]:
            self.field.degrade_base_cells()
        for event in events:
            if event.type == STOP_GAME:
                if not event.game_over:
                    max_level = 0
                    with open("./Support/company.txt", 'r') as f:
                        level = int(f.readlines()[0].split(';')[0])
                        max_level += min(LEVELS_COUNT - 1, max(level, self.level + 1))
                    with open("./Support/company.txt", 'w') as f:
                        f.write(str(max_level) + ";")
                    settings = self.score, self.player_count, min(self.level, max_level)
                    pygame.time.set_timer(pygame.event.Event(WIN_WINDOW, settings=settings), 1, 1)
                else:
                    settings = self.score, self.player_count, self.level
                    pygame.time.set_timer(pygame.event.Event(GAME_OVER_WINDOW, settings=settings), 1, 1)
        self.all_sprites.update(events)
        if PAUSE in [event.type for event in events]:
            self.pause = not self.pause
        if self.pause:
            return
        if PLAYER_GET_BONUS in [event.type for event in events]:
            self.score += [event.score for event in events if event.type == PLAYER_GET_BONUS][0]
        if PLAYER_KILLED in [event.type for event in events]:
            self.score -= 200
            self.players_killed += 1
            if self.players_killed == self.player_count:
                pygame.time.set_timer(pygame.event.Event(PAUSE), 1, 1)
                pygame.time.set_timer(pygame.event.Event(STOP_GAME, game_over=True), GAME_END_FREEZE, 1)
        if AI_DESTROYED in [event.type for event in events]:
            self.score += [event.score for event in events if event.type == AI_DESTROYED][0]
            self.kills += 1
            if self.kills == self.count_ai:
                pygame.time.set_timer(pygame.event.Event(PAUSE), 1, 1)
                pygame.time.set_timer(pygame.event.Event(STOP_GAME, game_over=False), GAME_END_FREEZE, 1)
        self.ai_time += 1 / FPS
        if self.ai_time > self.ai_time_max and len(self.queue) > 0:
            self.ai_time = 0
            n = random.choice(range(len(self.positions["ai"])))
            ai = AI(self.all_sprites, self.cell_size * 2, self.positions["ai"][n],
                    self.queue[0], self.number_bot % 5 == 4)
            self.queue.pop(0)
            self.all_sprites.change_layer(ai, 1)
            self.number_bot += 1
        self.bonus_time += 1
        if self.bonus_time > BONUS_TIME:
            self.bonus_time = 0
            n = len(self.positions["bonuses"])
            pos = self.positions["bonuses"][random.choice(range(n))]
            StarBonus(self.cell_size * 2, pos, self.all_sprites)

    def get_size(self):
        return self.field.get_size()

    def get_lives(self):
        if self.player_count == 2:
            return [self.players[0].get_lives(), self.players[1].get_lives()]
        return [self.players[0].get_lives()]
