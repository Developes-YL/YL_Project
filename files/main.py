def checkImports(files="all", libraries="all") -> bool:
    """проверка на наличие файлов и библиотек;
    files передаётся в виде списка, 
    элемент -> название_папки/название_файла.расширение
    название папки указывается, если она есть;
    libraries передаётся в виде списка названий библиотек"""

    try:
        import os.path
    except:
        return False

    if files == "all":
        try:
            from Support.Consts import FILES
            files = FILES
        except:
            return False

    if libraries == "all":
        try:
            from Support.Consts import LIBRARIES
            libraries = LIBRARIES
        except:
            return False

    unfound_files = []
    for name in files:
        if not os.path.exists("./files/" + name):
            unfound_files.append(name)
    if unfound_files:
        print("не найдены все необходимые файлы, а точнее:\n" + '\n'.join(unfound_files))

    unfound_libraries = []
    for name in libraries:
        try:
            exec("import " + name)
        except:
            unfound_libraries.append(name)
    if unfound_libraries:
        print("не найдены все необходимые библиотеки, а точнее:\n" + '\n'.join(unfound_libraries))

    return (not (unfound_files and unfound_libraries))


class Manager:
    """данный класс отвечает за работу приложения в целом"""
    def __init__(self):
        self.pygameStart()

        self.stage = 0 # состояние игры

        self.running = False
        self.musicOn = False
        self.soundsOn = False

        self.keydown_handlers = defaultdict(list) # обработчики событий в других классах
        self.keyup_handlers = defaultdict(list) # обработчики событий в других классах

    def pygameStart(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.size = self.width, self.height = WINDOW_SIZE
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(TITLE)
        self.window = Window()

    def run(self):
        """запуск главного цикла"""
        self.running = True
        while self.running:
            self.render() # отрисовка деталей
            self.handle_events() # обработка событий
            if not self.running:
                break
            self.clock.tick(FPS)
            pygame.display.flip()
        pygame.quit()

    def handle_events(self):
        """вызов обработчиков событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
                break
            for type in range(COUNT_USER_EVENTS):
                # обработка пользоваетльских событий
                if event.type == pygame.USEREVENT + type:
                    for handler in self.keydown_handlers[event.type]:
                        handler(event)
                    break

    def render(self):
        """отрисовка элементов окна и подобных элементов"""
        # добавление нового обработчика событий
        self.keydown_handlers[pygame.USEREVENT].append(self.window.render)

        # создание события
        pygame.time.set_timer(pygame.USEREVENT, 1)
        # pygame.USEREVENT + 0 -> отрисовка деталей


if __name__ == "__main__":
    if checkImports():
        from Objects.Windows import *
        from Support.Consts import *
        import pygame
        from collections import defaultdict

        manager = Manager()
        manager.run()