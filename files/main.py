
def check_imports(files_list="all", libraries_list="all") -> bool:
    """проверка на наличие файлов"""
    # скрипты, текстовые документы и спрайты
    if files_list == "all":
        try:
            from files.Support.Consts import FILES, SOUNDS
            files_list = FILES + SOUNDS
        except ImportError:
            print("Файл files.Support.Consts не найден")
            return False

    # библиотеки
    if libraries_list == "all":
        try:
            from files.Support.Consts import LIBRARIES
            libraries_list = LIBRARIES
        except ImportError:
            print("Файл files.Support.Consts не найден")
            return False
        
    unfounded_files = []
    for name in files_list:
        try:
            open(name)
        except OSError:
            unfounded_files.append(name)
    if unfounded_files:
        print("не найдены все необходимые файлы, а точнее:\n" + '\n'.join(unfounded_files))

    unfounded_libraries = []
    for name in libraries_list:
        try:
            exec("import " + name)
        except ImportError:
            unfounded_libraries.append(name)
    if unfounded_libraries:
        print("не найдены все необходимые библиотеки, а точнее:\n" + '\n'.join(unfounded_libraries))

    return not (unfounded_files + unfounded_libraries)


class Manager:
    """данный класс отвечает за работу приложения в целом"""
    def __init__(self):
        # настройка игры
        self.running = True

        pygame.init()
        self.clock = pygame.time.Clock()
        self.size = self.width, self.height = WINDOW_SIZE
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        pygame.display.set_caption(TITLE)
        self.window = LoadingWindow(self.screen)

        self.soundManager = SoundManager()

    def run(self):
        """запуск главного цикла"""
        # включение фоновой музыки
        pygame.event.post(pygame.event.Event(BACKGROUND_MUSIC_EVENT))

        while self.running:
            self.screen.fill(BLACK)
            self.handle_events()  # обработка событий
            if not self.running:
                break
            self.clock.tick(FPS)
            pygame.display.flip()
        pygame.quit()

    def handle_events(self):
        """обработка событий"""
        if pygame.event.get(pygame.QUIT):
            self.running = False
            return None

        # обработка первостепенных событий (например, переключение окон и закрытие приложения)
        events = pygame.event.get()
        self.window.create_events(events)

        events += pygame.event.get()  # обновление новых событий

        if pygame.QUIT in [event.type for event in events]:
            self.running = False
            return None

        for event in events:
            self.change_window(event)

        events += pygame.event.get()

        # обработка событий и выполнение действий между кадрами
        self.window.update(events)

        events += pygame.event.get()

        # обработка событий со звуком
        self.soundManager.update(events)

        events += pygame.event.get()

        if pygame.QUIT in events:
            self.running = False
            return None

        # отрисовка окна
        self.window.render()

    def change_window(self, event):
        """смена окон посредством обработки событий"""
        if event.type == GAME_WINDOW:
            self.window = GameWindow(self.screen, event.count, event.level)
        elif event.type == START_WINDOW:
            self.window = StartWindow(self.screen)
        elif event.type == LEVEL_SELECTION:
            self.window = SelectionLevel(self.screen, event.count)
        elif event.type == SETTINGS_WINDOW:
            self.window = SettingsWindow(self.screen)
        elif event.type == FINISH_WINDOW:
            self.window = EndWindow(self.screen, event.settings)

if __name__ == "__main__":
    if check_imports():
        from Objects.Windows import *
        from Support.Consts import WINDOW_SIZE, TITLE, FPS
        from Objects.SoundManager import SoundManager
        import pygame

        manager = Manager()
        manager.run()  # запуск игры
