# поля для игры и для рисования новых уровней
import pygame

from files.Objects.cells import *
from files.Support.Consts import *
from files.Support.colors import *


class Field1:
    def __init__(self, screen, group, level=0, size=(500, 500)):
        self.screen = screen
        self.level = level
        self.group = group

        self.cell_size = size[1] // (FIELD_SIZE[1] + 1)
        self.left = (size[0] - self.cell_size * FIELD_SIZE[0]) // 2
        self.top = self.cell_size // 2
        self.rect = (self.left, self.top, self.cell_size * FIELD_SIZE[0], self.cell_size * FIELD_SIZE[1])

        self.create_cells()

    def get_positions(self):
        positions = {"ai": [], "player": []}

        # 1st
        pos = (self.left + self.cell_size * (FIELD_SIZE[0] // 2 - 5), self.top + self.cell_size * (FIELD_SIZE[1] - 2))
        positions["player"].append(pos)
        # 2nd
        pos = (self.left + self.cell_size * (FIELD_SIZE[0] // 2 + 3), self.top + self.cell_size * (FIELD_SIZE[1] - 2))
        positions["player"].append(pos)

        # 1st
        pos = (self.left, self.top)
        positions["ai"].append([*pos, 0, 0])
        # 2nd
        pos = (self.left + self.cell_size * (FIELD_SIZE[0] // 2 - 1), self.top)
        positions["ai"].append([*pos, 13, 0])
        # 3rd
        pos = (self.left + self.cell_size * (FIELD_SIZE[0] - 2), self.top)
        positions["ai"].append([*pos, 25, 0])

        return positions

    def get_cell_size(self):
        return self.cell_size

    def create_cells(self):
        field = ""
        with open("./Support/levels.txt", 'r') as f:
            field += f.readlines()[self.level]
        for x in range(FIELD_SIZE[0]):
            for y in range(FIELD_SIZE[1]):
                pos = (self.left + x * self.cell_size, self.top + y * self.cell_size)
                if field[x * FIELD_SIZE[0] + y] == "1":
                    Brick(self.cell_size, pos, self.group)
                if field[x * FIELD_SIZE[0] + y] == "2":
                    Concrete(self.cell_size, pos, self.group)
                if field[x * FIELD_SIZE[0] + y] == "3":
                    Forest(self.cell_size, pos, self.group)
                if field[x * FIELD_SIZE[0] + y] == "4":
                    Ice(self.cell_size, pos, self.group)
                if field[x * FIELD_SIZE[0] + y] == "5":
                    Water(self.cell_size, pos, self.group)

        # границы поля
        # left
        Border(self.group, (self.left - 1, self.top - 1, 1, self.cell_size * FIELD_SIZE[1]))
        # right
        Border(self.group, (self.left + self.cell_size * FIELD_SIZE[0],
                            self.top - 1, 1, self.cell_size * FIELD_SIZE[1]))
        # top
        Border(self.group, (self.left - 1, self.top - 1, self.cell_size * FIELD_SIZE[0], 1))
        # bottom
        Border(self.group, (self.left - 1, self.top + self.cell_size * FIELD_SIZE[1] + 1,
                            self.cell_size * FIELD_SIZE[0], 1))


class Border(pygame.sprite.Sprite):
    def __init__(self, group, rect):
        super().__init__(group)
        self.image = pygame.Surface(rect[2:])
        self.rect = pygame.Rect(rect)
