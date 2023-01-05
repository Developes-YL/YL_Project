# все окна

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
        w_sc = self.width / w
        h_sc = self.height / 2 / h
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
                    pygame.event.post(pygame.event.Event(GAME_WINDOW, count=1))
                elif self.game == 2:
                    pygame.event.post(pygame.event.Event(GAME_WINDOW, count=2))
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
    def __init__(self, screen, count):
        self.count_players = count  # количество игроков
        super().__init__(screen)

    def _set_presets(self):
        self.game = Game(self.screen, self.count_players)

    def update(self, events):
        # надо добавить кнопки перезапуска уровня,
        # выхода из него и кнопки активации бонусов

        self.game.process_events(events)

    def render(self):
        # надо добавить кнопки перезапуска уровня,
        # выхода из него и кнопки активации бонусов
        self.game.render()


# надо добавить класс окна настроек,
# выбора уровня и редактор уровней
