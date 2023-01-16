import pygame

from files.Objects.cells import Water, Ice, Bush, Concrete, Brick, Base1
from files.Support.consts import FIELD_SIZE


class Field:
    def __init__(self, screen: pygame.display, group: pygame.sprite.LayeredUpdates,
                 size: tuple = (500, 500), level: int = 0):
        self.screen = screen
        self.level = level
        self.group = group

        self.cell_size = size[1] // (FIELD_SIZE[1] + 1)
        self.left = (size[0] - self.cell_size * FIELD_SIZE[0]) // 2
        self.top = self.cell_size // 2
        self.rect = (self.left, self.top, self.cell_size * FIELD_SIZE[0], self.cell_size * FIELD_SIZE[1])

        self.base_cells = []
        self._create_cells()

    def get_positions(self) -> dict:
        # точки появления танков
        positions = {"ai": [], "player": [], "bonuses": []}

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

        # точки появления бонусов
        left = self.cell_size * 3 + self.left
        top = self.cell_size * 3 + self.top
        for x in range(4):
            for y in range(4):
                pos = left + self.cell_size * x * 6, top + self.cell_size * y * 6
                positions["bonuses"].append(pos)

        return positions

    def get_cell_size(self) -> int:
        return self.cell_size

    def get_size(self) -> list:
        return [self.left, self.top, self.cell_size * FIELD_SIZE[0], self.cell_size * FIELD_SIZE[1]]

    def reset(self):
        self._create_cells()

    def upgrade_base_cells(self):
        for brick in self.base_cells:
            brick.upgrade(self.base_cells)

    def degrade_base_cells(self):
        for brick in self.base_cells:
            brick.degrade(self.base_cells)

    def _create_cells(self):
        field = ""
        try:
            with open("./Support/levels.txt", 'r') as f:
                field += f.readlines()[self.level]
        except FileNotFoundError or IndexError as exc:
            print("ошибка при чтении ./Support/levels.txt")
            field += "0" * 309 + "666" + "0" * 26 + "67" + "0" * 24 + "6" + "0" * 25 + "666" + "0" * 283

        for x in range(FIELD_SIZE[0]):
            for y in range(FIELD_SIZE[1]):
                pos = (self.left + x * self.cell_size, self.top + y * self.cell_size)
                preset = self.group, self.cell_size, pos
                cell = field[x * FIELD_SIZE[0] + y]

                if cell == "1":
                    Brick(*preset)
                elif cell == "2":
                    Concrete(*preset)
                elif cell == "3":
                    Bush(*preset)
                elif cell == "4":
                    Ice(*preset)
                elif cell == "5":
                    Water(*preset)
                elif cell == "6":
                    self.base_cells.append(Brick(*preset))  # кирпичи вокруг базы
                elif cell == "7":
                    pr = list(preset)
                    pr[1] *= 2
                    Base1(*pr)

        # границы поля
        # left
        Border(self.group, (self.left - 51, self.top - 1, 50, self.cell_size * FIELD_SIZE[1]))
        # right
        Border(self.group, (self.left + self.cell_size * FIELD_SIZE[0],
                            self.top - 1, 51, self.cell_size * FIELD_SIZE[1]))
        # top
        Border(self.group, (self.left - 1, self.top - 51, self.cell_size * FIELD_SIZE[0], 50))
        # bottom
        Border(self.group, (self.left - 1, self.top + self.cell_size * FIELD_SIZE[1] + 1,
                            self.cell_size * FIELD_SIZE[0], 50))


class Border(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.LayeredUpdates, rect: tuple = (0, 0, 0, 0)):
        super().__init__(group)
        self.image = pygame.Surface(rect[2:])
        self.rect = pygame.Rect(rect)

    def boom(self, flag: bool = False) -> bool:
        return True
