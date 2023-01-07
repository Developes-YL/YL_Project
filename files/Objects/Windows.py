# все окна
import pygame

from files.Objects.Game import Game
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
        self.game = 0

        # надпись 'Tank 1990'
        w, h = BG1.get_size()
        w_sc = self.width / w / 2
        h_sc = self.height / 2 / h / 2
        sc = min(w_sc, h_sc)
        self.bg = pygame.transform.scale(BG1, (w * sc, h * sc))

        self.colors = [RED, WHITE]  # цвета для кнопок
        size = [247, 75]
        # кнопки '1 player' и '2 players'
        self.one_player = [((self.width - size[0]) // 2, self.height * 6 // 10, *size), 0]
        self.two_player = [((self.width - size[0]) // 2, self.height * 7 // 10, *size), 0]

        # кнопка exit
        size = [154, 45]
        self.exit = [(self.width * 75 // 100, self.height * 9 // 10, *size), 0]

    def render(self):
        # отрисовка фона и кнопок
        self.screen.blit(self.bg, ((self.width - self.bg.get_size()[0]) // 2, 0))
        self._render_text(64, '1 Player', self.colors[self.one_player[1]], self.one_player[0])
        self._render_text(64, '2 Players', self.colors[self.two_player[1]], self.two_player[0])
        self._render_text(64, 'Exit', self.colors[self.exit[1]], self.exit[0])

    def create_events(self, events):
        """обработка нажатий на кнопки"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game == 1:
                    pygame.event.post(pygame.event.Event(LEVEL_SELECTION, count=1))
                elif self.game == 2:
                    pygame.event.post(pygame.event.Event(LEVEL_SELECTION, count=2))
                elif self.game == 3:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                # подсветка текста у кнопок
                if pygame.Rect(self.one_player[0]).collidepoint(event.pos):
                    self.one_player[1] = 1
                    self.two_player[1] = 0
                    self.exit[1] = 0
                    self.game = 1
                elif pygame.Rect(self.two_player[0]).collidepoint(event.pos):
                    self.one_player[1] = 0
                    self.two_player[1] = 1
                    self.exit[1] = 0
                    self.game = 2
                elif pygame.Rect(self.exit[0]).collidepoint(event.pos):
                    self.one_player[1] = 0
                    self.two_player[1] = 0
                    self.exit[1] = 1
                    self.game = 3
                else:
                    self.one_player[1] = 0
                    self.two_player[1] = 0
                    self.exit[1] = 0
                    self.game = 0


class GameWindow(Window):
    def __init__(self, screen, count, level):
        self.count_players = count  # количество игроков
        self.level = level
        super().__init__(screen)

    def _set_presets(self):
        self.game = Game(self.screen, self.count_players, self.level)

    def update(self, events):
        # надо добавить кнопки перезапуска уровня,
        # выхода из него и кнопки активации бонусов

        self.game.process_events(events)

    def render(self):
        # надо добавить кнопки перезапуска уровня,
        # выхода из него и кнопки активации бонусов
        self.game.render()


class LoadingWindow(Window):
    def _set_presets(self):
        self.max_loading = 600
        self.loading = 0
        self.label = "LOADING"
        self.number = 0

        self.font = pygame.font.SysFont('Comic Sans MS', self.min_size // 15)

        text_surface = self.font.render(self.label, False, RED)
        rect = text_surface.get_rect(center=(self.width // 2, self.height // 3))
        self.point = rect.midleft

        self.count = 0
        self.max_count = 50

        self.pause = True

    def create_events(self, events):
        if self.loading == self.max_loading:
            pygame.event.post(pygame.event.Event(START_WINDOW))

    def render(self):
        pass

    def update(self, events):
        if self.count < self.max_count and self.loading % 100 == 20:
            self.count += 1

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

        text_surface = self.font.render(self.label + "." * self.number, False, RED)
        rect = text_surface.get_rect(midleft=self.point)
        self.screen.blit(text_surface, rect)

        rect = pygame.Rect(self.width // 100, self.height // 2, self.width // 100 * 98, self.height // 50)
        pygame.draw.rect(self.screen, GREY, rect)
        rect = pygame.Rect(self.width // 100, self.height // 2,
                           self.width // 100 * 98 / self.max_loading * self.loading, self.height // 50)
        pygame.draw.rect(self.screen, RED, rect)


class SelectionLevel(Window):
    def __init__(self, screen, count):
        self.count_players = count
        super().__init__(screen)

    def _set_presets(self):
        self.level_count = 0
        with open("./Support/levels.txt", 'r') as f:
            self.level_count = len(f.readlines())
        self.labels = ["level " + str(number + 1) for number in range(self.level_count)]
        self.label_size = (self.width // 10, self.height // 15)
        self.left = self.width // 20 * 9
        self.label_space = self.label_size[1] // 3
        self.top = self.label_space
        self.button = -1
        self.min_top = self.top - (self.label_size[1] + self.label_space) * self.level_count + self.height
        self.max_top = self.top
        self.down_pressed = False
        self.up_pressed = False
        self.back = [0, 0, self.width // 10, self.height // 20]

    def create_events(self, events):
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
                self.top += event.y * 3
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

        if self.up_pressed:
            self.top += 15
        if self.down_pressed:
            self.top -= 15

        if self.top < self.min_top:
            self.top = self.min_top
        if self.top > self.max_top:
            self.top = self.max_top

    def render(self):
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


# надо добавить класс окна настроек,
# выбора уровня и редактор уровней
