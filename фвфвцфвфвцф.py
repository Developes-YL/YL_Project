import pygame

pygame.init()
size = 600, 600
screen = pygame.display.set_mode(size)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[1] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                 self.board[y][x])

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell):
        for x in range(self.height):
            self.board[x][cell[1]] = (self.board[x][cell[1]] + 1) % 2
        for y in range(self.width):
            self.board[cell[0]][y] = (self.board[cell[0]][y] + 1) % 2
        self.board[cell[0]][cell[1]] = (self.board[cell[0]][cell[1]] + 1) % 2

    def get_cell(self, pos):
        if self.left <= pos[1] < self.left + self.height * self.cell_size and \
                self.top <= pos[0] < self.top + self.width * self.cell_size:
            return (int((pos[1] - self.left) / self.cell_size), int((pos[0] - self.top) / self.cell_size))
        else:
            return None

    def get_click(self, pos):
        cell = self.get_cell(pos)
        if cell != None:
            self.on_click(cell)


board = Board(5, 7)
board.set_view(100, 100, 50)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()
pygame.quit()