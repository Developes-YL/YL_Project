class Game:
    def __init__(self, screen, count=1, window_size=(900, 600)):
        self.window_size = window_size
        self.screen = screen
        self.count_players = count

    def start(self):
        pass

    def render(self):
        pass

    def process_events(self, events):
        for event in events:
            pass

    def reset(self):
        pass
