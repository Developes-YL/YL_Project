import pygame

pygame.init()

pygame.mixer.music.load("sounds/background_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.06)
game_start = pygame.mixer.Sound('sounds/game_start.ogg')
game_start.set_volume(0.06)

def check_imports(files_list="all", libraries_list="all") -> bool:
    """checking for files and libraries"""

    try:
        import os.path
    except:
        return False
    
    if files_list == "all":
        try:
            from files.Support.Consts import FILES
            files_list = FILES
        except:
            return False

    if libraries_list == "all":
        try:
            from files.Support.Consts import LIBRARIES
            libraries_list = LIBRARIES
        except:
            return False
        
    unfounded_files = []
    for name in files_list:
        try:
            open(name)
        except:
            unfounded_files.append(name)
    if unfounded_files:
        print("не найдены все необходимые файлы, а точнее:\n" + '\n'.join(unfounded_files))

    unfounded_libraries = []
    for name in libraries_list:
        try:
            exec("import " + name)
        except:
            unfounded_libraries.append(name)
    if unfounded_libraries:
        print("не найдены все необходимые библиотеки, а точнее:\n" + '\n'.join(unfounded_libraries))

    return not (unfounded_files + unfounded_libraries)


class Manager:
    """данный класс отвечает за работу приложения в целом"""
    def __init__(self):
        # настройка игры
        self.running = False
        self.musicOn = False
        self.soundsOn = False

        pygame.init()
        self.clock = pygame.time.Clock()
        self.size = self.width, self.height = WINDOW_SIZE
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        pygame.display.set_caption(TITLE)
        # self.window = SelectionLevel(self.screen)
        self.window = LoadingWindow(self.screen)

    def run(self):
        """start main loop"""
        self.running = True
        while self.running:
            self.screen.fill(BLACK)
            self.handle_events()  # обработка событий
            if not self.running:
                break
            self.clock.tick(FPS)
            pygame.display.flip()
        pygame.quit()

    def handle_events(self):
        if pygame.event.get(pygame.QUIT):
            self.running = False
            return None

        # обработка первостепенных событий  (переключение окон и закрытие приложения)
        events = pygame.event.get()
        self.window.create_events(events)

        events += pygame.event.get()
        if pygame.QUIT in [event.type for event in events]:
            self.running = False
            return None
        #
        for event in events:
            self.change_window(event)

        # обработка событий и выполнение действий между кадрами
        self.window.update(events)

        if pygame.QUIT in pygame.event.get():
            self.running = False
            return None

        self.window.render()  # отрисовка окна

    def change_window(self, event):
        # смена окон происходит посредством создания новых событий
        # пользовательские события смотри в файле files/Support/events.py
        if event.type == GAME_WINDOW:
            self.window = GameWindow(self.screen, event.count, event.level)
            game_start.set_volume(VOL_EFFECTS)
            game_start.play()
        elif event.type == START_WINDOW:
            self.window = StartWindow(self.screen)
        elif event.type == LEVEL_SELECTION:
            self.window = SelectionLevel(self.screen, event.count)
        elif event.type == SETTINGS_WINDOW:
            self.window = SettingsWindow(self.screen)

        # остальные окна добавляем так:
        # if event.type == <NAME_WINDOW>:
        #    self.window = <NameClassWindow>(self.screen)


if __name__ == "__main__":
    if check_imports():
        from Objects.Windows import *
        from Support.Consts import *
        import pygame

        manager = Manager()
        manager.run()
