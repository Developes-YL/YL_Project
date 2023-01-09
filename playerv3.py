class Player(pygame.sprite.Sprite):
    def __init__(self, pos1, pos2, group, number=1, cell_size=30, pos=(0, 0)):
        super().__init__(group)
        self.px = pos1 * 10
        self.py = pos2 * 10
        self.group = group
        self.number = number
        self.start = pos
        self.lives = 3
        self.rect = pygame.Rect(*pos, cell_size, cell_size)
        self.image = pygame.transform.scale(TANK, (cell_size, cell_size))
        self.orient = 1
        self.hp = 100
        self.lives = 3
        self.move = 0
        self.wall = 0
        self.rect = pygame.Rect(self.px * 2, self.py * 2, 20, 20)
        self.power = 2

    def boom(self, flag):
        if not flag:
            self.lives -= 1
            exp = BigExplosion(self.group, self.rect[3], self.rect[0], self.rect[1])
            self.group.change_layer(exp, 2)
            if self.lives > 0:
                Player(self.group, self.number, self.rect[3], self.start)
                self.kill()
        return True

    def moveP(self, key):
        if self.orient == 1 and self.wall != 1:
            if key == 1:
                self.py -= 1
                self.wall = 0
            elif key != 0:
                self.orient = key
                self.move = 0
            if (self.py % 10) == 0:
                key = 0
                self.move = 0

            elif key == 0:
                self.py -= 1
                self.move = 1

        elif self.orient == 2 and self.wall != 2:
            if key == 2:
                self.py += 1
                self.wall = 0
            elif key != 0:
                self.orient = key
                self.move = 0
            if (self.py % 10) == 0:
                key = 0
                self.move = 0

            elif key == 0:
                self.py += 1
                self.move = 1

        elif self.orient == 3 and self.wall != 3:
            if key == 3:
                self.px -= 1
                self.wall = 0
            elif key != 0:
                self.orient = key
                self.move = 0
            if (self.px % 10) == 0:
                key = 0
                self.move = 0

            elif key == 0:
                self.px -= 1
                self.move = 1

        elif self.orient == 4 and self.wall != 4:
            if key == 4:
                self.px += 1
                self.wall = 0
            elif key != 0:
                self.orient = key
                self.move = 0
            if (self.px % 10) == 0:
                key = 0
                self.move = 0

            elif key == 0:
                self.px += 1
                self.move = 1

        else:
            self.move = 0
        self.rect = pygame.Rect(self.px * 2, self.py * 2, 20, 20)

    def walls(self, matrix):
        if (self.py % 10) == 0 and (self.px % 10) == 0:
            Y_axisd = matrix[self.py // 10 + 1][self.px // 10]
            Y_axisu = matrix[self.py // 10 - 1][self.px // 10]
            X_axisr = matrix[self.py // 10][self.px // 10 + 1]
            X_axisl = matrix[self.py // 10][self.px // 10 - 1]
            if (Y_axisd == 1 or Y_axisd == 2 or Y_axisd == 4 or Y_axisd == 6) and self.orient == 2:
                self.wall = 2
            elif (Y_axisu == 1 or Y_axisu == 2 or Y_axisu == 4 or Y_axisu == 6) and self.orient == 1:
                self.wall = 1
            elif (X_axisr == 1 or X_axisr == 2 or X_axisr == 4 or X_axisr == 6) and self.orient == 4:
                self.wall = 4
            elif (X_axisl == 1 or X_axisl == 2 or X_axisl == 4 or X_axisl == 6) and self.orient == 3:
                self.wall = 3
