# поля для игры и для рисования новых уровней
import copy

import pygame

from files.Objects.cells import *
from files.Support.Consts import *


class Field1:
    def __init__(self, screen, level=0, cell_size=30):
        self.screen = screen
        self.level = level
        self.cells = pygame.sprite.Group()
        self.size_cell = cell_size
        self.left = 25
        self.top = 25
        self.create_cells()

    def create_cells(self):
        field = ""
        with open("./Support/levels.txt", 'r') as f:
            field += f.readlines()[self.level]
        for x in range(FIELD_SIZE[0]):
            for y in range(FIELD_SIZE[1]):
                pos = (self.left + x * self.size_cell, self.top + y * self.size_cell)
                print(x, y, self.size_cell, pos)
                if field[x * FIELD_SIZE[0] + y] == "1":
                    Brick(self.size_cell, pos, self.cells)
                if field[x * FIELD_SIZE[0] + y] == "2":
                    Concrete(self.size_cell, pos, self.cells)
                if field[x * FIELD_SIZE[0] + y] == "3":
                    Forest(self.size_cell, pos, self.cells)
                if field[x * FIELD_SIZE[0] + y] == "4":
                    Ice(self.size_cell, pos, self.cells)
                if field[x * FIELD_SIZE[0] + y] == "5":
                    Water(self.size_cell, pos, self.cells)

    def reset(self):
        pass

    def update(self):
        self.cells.update()

    def render(self):
        self.cells.draw(self.screen)
