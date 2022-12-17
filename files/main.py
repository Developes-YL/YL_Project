def checkImports(files="all", libraries="all") -> bool:
    """checking for files and libraries"""

    try:
        import os.path
    except:
        return False
    
    if files == "all":
        try:
            from files.Support.Consts import FILES
            files = FILES
        except:
            return False

    if libraries == "all":
        try:
            from files.Support.Consts import LIBRARIES
            libraries = LIBRARIES
        except:
            return False
        
    unfounded_files = []
    for name in files:
        try:
            file = open(name)
        except:
            unfounded_files.append(name)
    if unfounded_files:
        print("не найдены все необходимые файлы, а точнее:\n" + '\n'.join(unfounded_files))

    unfounded_libraries = []
    for name in libraries:
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
        self.pygameStart()

        self.stage = 0  # состояние игры

        self.running = False
        self.musicOn = False
        self.soundsOn = False

        self.render_handlers = []
        self.process_handlers = []
        self.create_handlers = []

        self.process_handlers.append(lambda x: self.changeWindow(x))

    def pygameStart(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.size = self.width, self.height = WINDOW_SIZE
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(TITLE)
        self.window = Window(self.screen)

    def run(self):
        self.running = True
        while self.running:
            self.screen.fill((0, 0, 0))
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

        events = pygame.event.get()
        
        # обработка первостепенных событий  (переключение окон и закртие приложения)
        self.window.createEvents(events) 
        for event in events:
            for handler in self.create_handlers:
                handler(event)
            
        events += pygame.event.get()

        if pygame.event.get(pygame.QUIT):
            self.running = False
            return None

        self.window.processEvents(events) # обработка событий и выполнение действий между кадрами 
        for event in events:
            for handler in self.process_handlers:
                handler(event)

        self.window.render() # отрисовка окна
        for handler in self.render_handlers:
            handler()

    def changeWindow(self, event):
        pass
        # создаем события для переключения окон в других классах
        # а здесь их обрабатываем
        #if event.type == PLANE_WINDOW:
        #    self.window = PlaneWindow(self.screen)


if __name__ == "__main__":
    if checkImports():
        from files.Objects.Windows import *
        from files.Support.Consts import *
        import pygame

        manager = Manager()
        manager.run()
