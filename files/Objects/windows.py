# все окна

from files.Objects.Game import Game
from files.Support.events import *
from files.Support.ui import *
from files.Support.colors import *


class Window:
    def __init__(self, screen):
        self.screen = screen
        self.size = self.width, self.height = map(int, self.screen.get_size())
        self.min_size = min(self.width, self.height)
        self.set_presets()

    def render(self):
        pass

    def create_events(self, events):
        pass

    def set_presets(self):
        pass

    def process_events(self, events):
        pass

    def render_text(self, text_size=0, text='text', color=WHITE, rect=(0, 0), font='Comic Sans MS'):
        my_font = pygame.font.SysFont(font, text_size)
        text_surface = my_font.render(text, False, color)
        center = (rect[0] + rect[2] // 2, rect[1] + rect[3] // 2)
        text_rect = text_surface.get_rect(center=center)
        self.screen.blit(text_surface, text_rect)


class StartWindow(Window):
    def set_presets(self):
        self.game = 0
        w, h = BG1.get_size()
        w_sc = self.width / w
        h_sc = self.height / 2 / h
        sc = min(w_sc, h_sc)
        self.bg = pygame.transform.scale(BG1, (w * sc, h * sc))
        self.colors = [(255, 0, 0), (255, 255, 255)]
        size = [247, 75]
        self.one_player = [((self.width - size[0]) // 2, self.height * 6 // 10, *size), 0]
        self.two_player = [((self.width - size[0]) // 2, self.height * 7 // 10, *size), 0]
        size = [154, 45]
        self.exit = [(self.width * 75 // 100, self.height * 9 // 10, *size), 0]

    def render(self):
        self.screen.blit(self.bg, ((self.width - self.bg.get_size()[0]) // 2, 0))
        self.render_text(64, '1 Player', self.colors[self.one_player[1]], self.one_player[0])
        self.render_text(64, '2 Player', self.colors[self.two_player[1]], self.two_player[0])
        self.render_text(64, 'Exit', self.colors[self.exit[1]], self.exit[0])

    def create_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game == 1:
                    pygame.event.post(pygame.event.Event(GAME_WINDOW, count=1))
                elif self.game == 2:
                    pygame.event.post(pygame.event.Event(GAME_WINDOW, count=2))
                elif self.game == 3:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def process_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                if pygame.Rect(self.one_player[0]).collidepoint(event.pos):
                    self.one_player[1] = 1
                    self.two_player[1] = 0
                    self.exit[1] = 0
                    self.game = 2
                elif pygame.Rect(self.two_player[0]).collidepoint(event.pos):
                    self.one_player[1] = 0
                    self.two_player[1] = 1
                    self.exit[1] = 0
                    self.game = 1
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


class LevelSelectionWindow(Window):
    pass


class LoadingWindow(Window):
    pass


class GameWindow(Window):
    def __init__(self, screen, count):
        self.count_players = count
        super().__init__(screen)

    def set_presets(self):
        self.game = Game(self.screen, self.count_players)

        self.game.start()

    def process_events(self, events):
        self.game.process_events(events)

    def render(self):
        self.game.render()

