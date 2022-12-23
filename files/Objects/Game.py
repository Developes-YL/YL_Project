from files.Objects.AI import AI
from files.Objects.Player import Player
from files.Objects.fields import Field_1
from files.Support.Consts import FPS


class Game:
    def __init__(self, screen, player_count=1, level=0):
        self.window_size = map(int, screen.get_size())
        self.screen = screen
        self.player_count = player_count
        self.field = Field_1()

        # рассчет времени появления ботов
        self.ai_time_max = (190 - level * 4 - (player_count - 1) * 20) * 60  # в секундах
        # self.ai = ... все боты
        self.ai_time = 0
        self.game_over = False

    def start(self):
        self.player_1 = Player(1)
        if self.player_count == 2:
            self.player_2 = Player(2)

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

    def reset(self):
        self.field.reset()
