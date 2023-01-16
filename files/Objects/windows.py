# все окна
import pygame.event

from files.Objects.Game import Game
from files.Support.consts import LEVELS_COUNT
from files.Support.events import *
from files.Support.ui import *
from files.Support.colors import *


class Window:
    """общий класс окон для данного проекта"""
    def __init__(self, screen):
        self.screen = screen
        self.size = self.width, self.height = map(int, self.screen.get_size())
        self.min_size = min(self.width, self.height)
        self._set_presets()

    def render(self):
        pass

    def create_events(self, events):
        """создание первостепенных событий,
        например, переключение окон"""
        pass

    def _set_presets(self):
        """настройка элементов окна"""
        pass

    def update(self, events):
        """отрисовка окна и дочерних элементов"""
        pass

    def _render_text(self, text_size=0, text='text', color=WHITE, rect=(0, 0, 0, 0), font='Comic Sans MS'):
        """отрисовка текста с данными параметрами с центром в данной точке"""
        # здесь rect = (<center_x>, <center_y>, <width>, <height>)
        my_font = pygame.font.SysFont(font, text_size)
        text_surface = my_font.render(text, False, color)
        center = (rect[0] + rect[2] // 2, rect[1] + rect[3] // 2)
        text_rect = text_surface.get_rect(center=center)
        self.screen.blit(text_surface, text_rect)


class StartWindow(Window):
    def _set_presets(self):
        # статус настроек
        # 0 - ничего
        # 1 - один игрок
        # 2 - два игрока
        # 3 - выйти
        # 4 - настройки
        self.button = 0

        # надпись 'Tank 1990'
        w, h = BG1.get_size()
        w_sc = self.width / w / 2
        h_sc = self.height / 2 / h / 2
        sc = min(w_sc, h_sc)
        self.bg = pygame.transform.scale(BG1, (w * sc, h * sc))

        self.colors = [RED, WHITE]  # цвета для кнопок
        size = [247, 75]

        # кнопки
        self.one_player = ((self.width - size[0]) // 2, self.height * 6 // 10, *size)
        self.two_player = ((self.width - size[0]) // 2, self.height * 7 // 10, *size)
        self.settings_main_window = ((self.width - size[0]) // 2, self.height * 5 // 10, *size)

        # кнопка exit
        size = [154, 45]
        self.exit = (self.width * 75 // 100, self.height * 9 // 10, *size)

    def render(self):
        """отрисовка фона и кнопок"""
        self.screen.blit(self.bg, ((self.width - self.bg.get_size()[0]) // 2, 0))
        self._render_text(64, '1 Player', self.colors[self.button == 1], self.one_player)
        self._render_text(64, '2 Players', self.colors[self.button == 2], self.two_player)
        self._render_text(64, 'Exit', self.colors[self.button == 3], self.exit)
        self._render_text(64, 'Settings', self.colors[self.button == 4], self.settings_main_window)

    def create_events(self, events):
        """обработка нажатий на кнопки"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button == 1:
                    pygame.event.post(pygame.event.Event(LEVEL_SELECTION, count=1))
                elif self.button == 2:
                    pygame.event.post(pygame.event.Event(LEVEL_SELECTION, count=2))
                elif self.button == 3:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif self.button == 4:
                    pygame.event.post(pygame.event.Event(SETTINGS_WINDOW, count=0))

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                # подсветка текста у кнопок
                if pygame.Rect(self.one_player).collidepoint(event.pos):
                    self.button = 1
                elif pygame.Rect(self.two_player).collidepoint(event.pos):
                    self.button = 2
                elif pygame.Rect(self.exit).collidepoint(event.pos):
                    self.button = 3
                elif pygame.Rect(self.settings_main_window).collidepoint(event.pos):
                    self.button = 4
                else:
                    self.button = 0


class GameWindow(Window):
    def __init__(self, screen, count, level):
        self.count_players = count  # количество игроков
        self.level = level
        super().__init__(screen)

    def _set_presets(self):
        self.game = Game(self.screen, self.count_players, self.level)
        self.field_size = self.game.get_size()

        # фон вокруг игрового поля
        border_1 = [0, 0, self.width, self.field_size[1]]
        border_2 = [0, self.field_size[1], self.field_size[0], self.height - self.field_size[1]]
        border_3 = [self.field_size[0], self.field_size[1] + self.field_size[3],
                    self.width - self.field_size[0], self.height - self.field_size[1] - self.field_size[3]]
        border_4 = [self.field_size[0] + self.field_size[2], 0, self.width - self.field_size[0] - self.field_size[2],
                    self.height - self.field_size[1]]
        self.borders = [border_1, border_2, border_3, border_4]

        # кнопки
        self.back = [0, 0, self.width // 10, self.height // 20]
        self.pause_button = [self.width // 100 * 80, 0, *[self.min_size // 20] * 2]

        self.pause_images_normal = [PAUSE_RED, PAUSE_WHITE, PLAY_WHITE, PLAY_RED]
        self.pause_images_selected = [PAUSE_WHITE, PAUSE_RED, PLAY_RED, PLAY_WHITE]
        self.pause_images_normal = [pygame.transform.scale(img, (self.pause_button[2:]))
                                    for img in self.pause_images_normal]
        self.pause_images_selected = [pygame.transform.scale(img, (self.pause_button[2:]))
                                      for img in self.pause_images_selected]
        self.pause_images = self.pause_images_normal

        self.restart_button = [self.width // 100 * 92, 0, *[self.min_size // 20] * 2]
        self.restart_images_normal = [pygame.transform.scale(img, (self.pause_button[2:]))
                                      for img in [RESTART_RED, RESTART_WHITE]]
        self.restart_images = self.restart_images_normal

        self.score_label = [0, self.height // 3, self.field_size[0], self.height // 20]

        self.lives_1 = [0, self.height // 2, self.field_size[0], self.height // 20]
        self.lives_2 = [self.field_size[0] + self.field_size[2], self.height // 2,
                        self.field_size[0], self.height // 20]

        self.button = -1  # выбранная кнопка

        self.game_over = False
        self.score = 0

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.button = -1
                if pygame.Rect(self.back).collidepoint(event.pos):
                    self.button = 2
                if pygame.Rect(self.pause_button).collidepoint(event.pos):
                    self.button = 1
                    self.pause_images = self.pause_images_selected
                else:
                    self.pause_images = self.pause_images_normal
                if pygame.Rect(self.restart_button).collidepoint(event.pos):
                    self.button = 3
                    self.restart_images = self.restart_images_normal[::-1]
                else:
                    self.restart_images = self.restart_images_normal
            self.score = self.game.get_score()

        self.game.process_events(events)

    def render(self):
        self.game.render()
        for rect in self.borders:
            pygame.draw.rect(self.screen, GREY_2, rect)

        if self.button == 2:
            self._render_text(self.min_size // 20, "BACK", WHITE, self.back)
        else:
            self._render_text(self.min_size // 20, "BACK", RED, self.back)

        self.screen.blit(self.pause_images[0], self.pause_button[:2])
        self.screen.blit(self.restart_images[0], self.restart_button[:2])
        self._render_text(self.min_size // 30, str(self.score), WHITE, self.score_label)
        lives = self.game.get_lives()
        self._render_text(self.min_size // 30, f"PLayer1's lives: {lives[0]}", WHITE, self.lives_1)
        if len(lives) > 1:
            self._render_text(self.min_size // 30, f"PLayer2's lives: {lives[1]}", WHITE, self.lives_2)

    def create_events(self, events):
        if STOP_GAME in [event.type for event in events]:
            self.game_over = True
        if self.game_over:
            return

        if pygame.MOUSEBUTTONDOWN in [event.type for event in events]:
            if self.button == 1:
                pygame.event.post(pygame.event.Event(PAUSE))
                self.pause_images = self.pause_images[::-1]
                self.pause_images_normal = self.pause_images_normal[::-1]
                self.pause_images_selected = self.pause_images_selected[::-1]
            elif self.button == 2:
                pygame.event.post(pygame.event.Event(START_WINDOW))
            elif self.button == 3:
                self.game.new_game()


class LoadingWindow(Window):
    def _set_presets(self):
        self.max_loading = 600
        self.loading = 0
        self.label = "LOADING"
        self.number = 0
        self.font = pygame.font.SysFont('Comic Sans MS', self.min_size // 15)
        size = [self.width // 100 * 20, self.height // 100 * 20]
        self.label_size = ((self.width - size[0]) // 2, self.height * 8 // 10, *size)
        text_surface = self.font.render(self.label, False, RED)
        rect = text_surface.get_rect(center=(self.width // 2, self.height // 3))
        self.point = rect.midleft
        self.count = 0
        self.max_count = 50
        self.pause = True

    def create_events(self, events):
        if pygame.K_p in [event.key for event in events if event.type == pygame.KEYDOWN]:
            self.loading = self.max_loading
        if self.loading == self.max_loading:
            pygame.event.post(pygame.event.Event(START_WINDOW))

    def render(self):

        text_surface = self.font.render(self.label + "." * self.number, False, RED)
        rect = text_surface.get_rect(midleft=self.point)
        self.screen.blit(text_surface, rect)

        self._render_text(self.min_size // 15, 'POWERED BY DEADBEATS', RED, self.label_size)
        rect = pygame.Rect(self.width // 100, self.height // 2, self.width // 100 * 98, self.height // 50)
        pygame.draw.rect(self.screen, GREY, rect)
        rect = pygame.Rect(self.width // 100, self.height // 2,
                           self.width // 100 * 98 / self.max_loading * self.loading, self.height // 50)
        pygame.draw.rect(self.screen, RED, rect)

    def update(self, events):
        if self.count < self.max_count and self.loading % 100 == 20:
            self.count += 1

        # имитация загрузки как на приставках :)
        if self.count < self.max_count and self.loading % 100 == 20:
            pass
        elif self.loading < self.max_loading * 0.4:
            self.loading += 7
        elif self.loading < self.max_loading * 0.6:
            self.loading += 5
        elif self.loading < self.max_loading * 0.8:
            self.loading += 3
        else:
            self.loading += 1

        if self.count == self.max_count:
            self.count = 0

        if self.loading % 20 == 0 and not (self.count < self.max_count and self.loading % 100 == 20):
            self.number = (self.number + 1) % 4


class SelectionLevel(Window):
    def __init__(self, screen, count):
        self.count_players = count
        super().__init__(screen)

    def _set_presets(self):
        self.level_count = 0
        # загрузка количества уровней
        with open("./Support/company.txt", 'r') as f:
            self.level_count = int(f.readlines()[0].split(';')[0]) + 1

        # параметры отривки кнопок уровней
        self.labels = ["level " + str(number + 1) for number in range(self.level_count)]
        self.label_size = (self.width // 10, self.height // 15)
        self.left = self.width // 20 * 9
        self.label_space = self.label_size[1] // 3
        self.top = self.label_space

        # границы прокрутки
        self.min_top = self.top - (self.label_size[1] + self.label_space) * self.level_count + self.height
        self.max_top = self.top

        self.back = [0, 0, self.width // 10, self.height // 20]

        self.down_pressed = False
        self.up_pressed = False
        self.button = -1

    def create_events(self, events):
        if pygame.MOUSEWHEEL not in [event.type for event in events]:
            if pygame.MOUSEBUTTONDOWN in [event.type for event in events]:
                if self.button in range(self.level_count):
                    pygame.event.post(pygame.event.Event(GAME_WINDOW, count=self.count_players, level=self.button))
                elif self.button == -2:
                    pygame.event.post(pygame.event.Event(START_WINDOW))

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.up_pressed = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.down_pressed = True
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                self.up_pressed = False
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                self.down_pressed = False
            if event.type == pygame.MOUSEWHEEL:
                # прокрутка с помощью колесика мыши
                self.top += event.y * 50
            if event.type == pygame.MOUSEMOTION:
                # подсветка текста у кнопок
                self.button = -1

                for number in range(self.level_count):
                    rect = (self.left, self.top + (self.label_space + self.label_size[1]) * number, *self.label_size)
                    if pygame.Rect(rect).collidepoint(event.pos):
                        self.button = number
                        break

                if pygame.Rect(self.back).collidepoint(event.pos):
                    self.button = -2

        # прокрутка с помощью стрелок
        if self.up_pressed:
            self.top += 15
        if self.down_pressed:
            self.top -= 15

        if self.top < self.min_top:
            self.top = self.min_top
        if self.top > self.max_top:
            self.top = self.max_top

    def render(self):
        # отрисовываются только кнопки, которые отображаются на экране
        for number, label in enumerate(self.labels):
            rect = (self.left, self.top + (self.label_space + self.label_size[1]) * number, *self.label_size)
            if rect[1] in range(-self.label_size[1], self.height + self.label_space + self.label_size[1]):
                color = RED
                if self.button == number:
                    color = WHITE
                self._render_text(self.min_size // 20, label, color, rect)

        if self.button == -2:
            self._render_text(self.min_size // 15, "BACK", WHITE, self.back)
        else:
            self._render_text(self.min_size // 15, "BACK", RED, self.back)


class SettingsWindow(Window):
    def _set_presets(self):
        self.difficulty = 0
        self.button = 0

        w, h = SETTINGS1.get_size()
        w_sc = self.width / w / 2
        h_sc = self.height / 2 / h / 2
        sc = min(w_sc, h_sc)
        self.bg = pygame.transform.scale(SETTINGS1, (w * sc, h * sc))

        self.colors = [RED, WHITE]
        size = [self.width // 100 * 25, self.height // 100 * 20]
        self.change_music_volume = ((self.width - size[0]) // 2, self.height * 3 // 10, *size)
        self.change_effect_volume = ((self.width - size[0]) // 2, self.height * 5 // 10, *size)

        size = [self.min_size // 100 * 20] * 2
        self.music_volume_plus = ((self.width - size[0]) // 4 * 3, self.height * 3 // 10, *size)
        self.music_volume_minus = ((self.width - size[0]) // 4, self.height * 3 // 10, *size)
        self.effect_volume_plus = ((self.width - size[0]) // 4 * 3, self.height * 5 // 10, *size)
        self.effect_volume_minus = ((self.width - size[0]) // 4, self.height * 5 // 10, *size)

        # кнопка back
        self.back = [0, 0, self.width // 10, self.height // 20]

    def render(self):
        # отрисовка фона и кнопок
        self.screen.blit(self.bg, ((self.width - self.bg.get_size()[0]) // 2, 0))
        self._render_text(self.min_size // 30, 'Back', self.colors[self.button == 2], self.back)

        self._render_text(self.min_size // 15, 'Music volume',
                          self.colors[self.button == 1], self.change_music_volume)
        self._render_text(self.min_size // 10, '+', self.colors[self.button == 3], self.music_volume_plus)
        self._render_text(self.min_size // 10, '-', self.colors[self.button == 4], self.music_volume_minus)

        self._render_text(self.min_size // 15, 'Effect volume',
                          self.colors[self.button == 5], self.change_effect_volume)
        self._render_text(self.min_size // 10, '+', self.colors[self.button == 6], self.effect_volume_plus)
        self._render_text(self.min_size // 10, '-', self.colors[self.button == 7], self.effect_volume_minus)

    def create_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button == 2:
                    pygame.event.post(pygame.event.Event(START_WINDOW))

                elif self.button == 3:
                    pygame.event.post(pygame.event.Event(VOLUME_UP, music=True))
                elif self.button == 4:
                    pygame.event.post(pygame.event.Event(VOLUME_DOWN, music=True))
                elif self.button == 1:
                    pygame.event.post(pygame.event.Event(STANDART_VOLUME, music=True))

                elif self.button == 6:
                    pygame.event.post(pygame.event.Event(VOLUME_UP, music=False))
                    pygame.event.post(pygame.event.Event(SHOT_EFFECT_EVENT))
                elif self.button == 7:
                    pygame.event.post(pygame.event.Event(VOLUME_DOWN, music=False))
                    pygame.event.post(pygame.event.Event(SHOT_EFFECT_EVENT))
                elif self.button == 5:
                    pygame.event.post(pygame.event.Event(STANDART_VOLUME, music=False))
                    pygame.event.post(pygame.event.Event(SHOT_EFFECT_EVENT))

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                # подсветка текста у кнопок
                if pygame.Rect(self.change_music_volume).collidepoint(event.pos):
                    self.button = 1
                elif pygame.Rect(self.back).collidepoint(event.pos):
                    self.button = 2
                elif pygame.Rect(self.music_volume_plus).collidepoint(event.pos):
                    self.button = 3
                elif pygame.Rect(self.music_volume_minus).collidepoint(event.pos):
                    self.button = 4
                elif pygame.Rect(self.change_effect_volume).collidepoint(event.pos):
                    self.button = 5
                elif pygame.Rect(self.effect_volume_plus).collidepoint(event.pos):
                    self.button = 6
                elif pygame.Rect(self.effect_volume_minus).collidepoint(event.pos):
                    self.button = 7
                else:
                    self.button = 0


class EndWindow(Window):
    def __init__(self, screen, settings):
        super().__init__(screen)
        self.score, self.player_count, self.level = settings

    def _set_presets(self):
        self.difficulty = 0
        self.button = 0

        w, h = BG_LOSE.get_size()
        w_sc = self.width / w / 2
        h_sc = self.height / 2 / h / 2
        sc = min(w_sc, h_sc)
        self.bg = pygame.transform.scale(BG_LOSE, (w * sc, h * sc))

        self.colors = [RED, WHITE]
        size = [self.width // 100 * 20, self.height // 100 * 20]
        self.restart_level = ((self.width - size[0]) // 2, self.height * 7.5 // 10, *size)
        self.label_size = ((self.width - size[0]) // 2, self.height * 3 // 10, *size)

        # кнопка back
        self.back = [0, 0, self.width // 7, self.height // 20]

    def render(self):
        # отрисовка фона и кнопок)

        self.screen.blit(self.bg, ((self.width - self.bg.get_size()[0]) // 2, 0))
        self._render_text(self.min_size // 30, 'Back to levels', self.colors[self.button == 2], self.back)
        self._render_text(self.min_size // 15, 'Restart level', self.colors[self.button == 3], self.restart_level)
        self._render_text(self.min_size // 15, 'Your Score:' + str(self.score), RED, self.label_size)

    def create_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button == 2:
                    pygame.event.post(pygame.event.Event(LEVEL_SELECTION, count=self.player_count))
                elif self.button == 3:
                    pygame.event.post(pygame.event.Event(GAME_WINDOW, count=self.player_count, level=self.level))

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                # подсветка текста у кнопок
                if pygame.Rect(self.back).collidepoint(event.pos):
                    self.button = 2
                elif pygame.Rect(self.restart_level).collidepoint(event.pos):
                    self.button = 3
                else:
                    self.button = 0


class WinWindow(Window):
    def __init__(self, screen, settings):
        super().__init__(screen)
        self.score, self.player_count, self.level = settings

    def _set_presets(self):
        self.difficulty = 0
        self.button = 0
        w, h = BG_WIN.get_size()
        w_sc = self.width / w / 2
        h_sc = self.height / 2 / h / 2
        sc = min(w_sc, h_sc)
        self.bg = pygame.transform.scale(BG_WIN, (w * sc, h * sc))

        self.colors = [RED, WHITE]
        size = [self.width // 100 * 20, self.height // 100 * 20]
        self.next_level = ((self.width - size[0]) // 2, self.height * 5 // 10, *size)
        self.restart_level = ((self.width - size[0]) // 2, self.height * 6 // 10, *size)
        self.label_size = ((self.width - size[0]) // 2, self.height * 3 // 10, *size)

        # кнопка back
        self.back = [0, 0, self.width // 7, self.height // 20]

    def render(self):
        # отрисовка фона и кнопок)

        self.screen.blit(self.bg, ((self.width - self.bg.get_size()[0]) // 2, 0))
        self._render_text(self.min_size // 30, 'Back to levels', self.colors[self.button == 2], self.back)
        self._render_text(self.min_size // 15, 'Next level', self.colors[self.button == 1], self.next_level)
        self._render_text(self.min_size // 15, 'Restart level', self.colors[self.button == 3], self.restart_level)
        self._render_text(self.min_size // 15, 'Your Score:' + str(self.score), RED, self.label_size)

    def create_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button == 2:
                    pygame.event.post(pygame.event.Event(LEVEL_SELECTION, count=self.player_count))
                elif self.button == 3:
                    pygame.event.post(pygame.event.Event(GAME_WINDOW, count=self.player_count, level=self.level))
                elif self.button == 1:
                    level = min(LEVELS_COUNT - 1, self.level + 1)
                    pygame.event.post(pygame.event.Event(GAME_WINDOW, count=self.player_count, level=level))

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                # подсветка текста у кнопок
                if pygame.Rect(self.next_level).collidepoint(event.pos):
                    self.button = 1
                elif pygame.Rect(self.back).collidepoint(event.pos):
                    self.button = 2
                elif pygame.Rect(self.restart_level).collidepoint(event.pos):
                    self.button = 3
                else:
                    self.button = 0
