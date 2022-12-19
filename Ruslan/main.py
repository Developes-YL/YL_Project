# -*- coding: UTF-8 -*-
import pygame

pygame.init()
size = 700, 500
screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption('TANK 1990')
clock = pygame.time.Clock()
color = 0, 0, 0
color2 = 255, 0, 153

fs = pygame.image.load('images/fs.png')
back = pygame.image.load('images/back.png')
kir = pygame.image.load('images/kir.png')
beton = pygame.image.load('images/beton.png')
forest = pygame.image.load('images/forest.png')
base = pygame.image.load('images/base.png')
dbase = pygame.image.load('images/dbase.png')
water = pygame.image.load('images/water.png')
ggu = pygame.image.load('images/ggu.png')
e = pygame.image.load('images/e.png')

e_rect = e.get_rect()
e_rect.width = e_rect.height
slide_rect = e.get_rect()
slide_rect.width = slide_rect.height

level = 0
move = 0
matrix =0
x = 0
y = 0
a = matrix
enable = 0
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 18)
font3 = pygame.font.Font(None, 64)
zet = 0
initbase = True
basehp = 2
plives = 3
rect = []
booms = []


class Base:
    def __init__(self, basehp):
        self.basehp = basehp
        initbase = False

    def destroy(self):
        if self.basehp == 0:
            base = dbase

class Boom:
    pass

    def render(self, screen):
        screen.blit(e, self.e_rect, self.slide_rect)

    def step(self):
        pass

    def destroy(self):
        pass

class Bonus:
    pass

    def render(self, screen):
        screen.blit(self.image, (self.x * 20, self.y * 20))


class Shoot:
    def __init__(self, pos1, pos2, orient, sight):
        pass

    def step(self):
        pass

    def destroy(self, matrix):
        pass

    def render(self, screen):
        pass

class Player:
    def __init__(self, pos1, pos2):
        self.ggx = pos1 * 10
        self.ggy = pos2 * 10
        self.orient = 1
        self.hp = 25
        self.lives = 3
        self.move = 0
        self.ggu = ggu
        self.ggd = pygame.transform.rotate(self.ggu, 180)
        self.ggl = pygame.transform.rotate(self.ggu, 90)
        self.ggr = pygame.transform.rotate(self.ggu, 270)
        self.gg = self.ggu
        self.wall = 0
        self.rect = pygame.Rect(self.ggx * 2, self.ggy * 2, 20, 20)
        self.power = 2

    def moveP(self, key):

        pass

    def walls(self, matrix):
        pass

    def render(self, screen):
        screen.blit(self.gg, (self.ggx * 2, self.ggy * 2))

    def touch(self, i):
        pass


class Enemy:
    def __init__(self, tip, resp):
        pass

    def walls(self, matrix):
        pass
    def move(self):
        pass

    def render(self, screen):
        pass

    def enshoot(self):
        pass

    def touch(self):
        pass

def pole(a):
    pass

def poleFFF(a):
    pass

ggx = 9
ggy = 22
player = 1
player2 = 20
fight = 0
go = False
done = False
menu = font3.render(u'1 Player', 1, (255, 255, 10))
menupos = pygame.Rect(220, 340,247,75)
menu2 = font3.render(u'Exit', 1, (255, 255, 10))
menupos2 = pygame.Rect(600, 450,154,45)
menu3 = font3.render(u'2 Players', 1, (255, 255, 10))
menupos3 = pygame.Rect(220, 400,247,75)
def mmenu(go):
        global menu, menu2,menupos,menupos2, done, menu3, menupos3
        while not go:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                done = True
                                go = True
                        elif event.type == pygame.MOUSEMOTION:
                                if menupos2.collidepoint(event.pos):
                                    menu3 = font3.render(u'2 Players', 1, (255, 255, 10))
                                    menu2 = font3.render(u'Exit', 1, (255, 0, 0))
                                    menu = font3.render(u'1 Player', 1, (255, 255, 10))
                                    game = 2
                                elif menupos.collidepoint(event.pos):
                                    menu3 = font3.render(u'2 Players', 1, (255, 255, 10))
                                    menu = font3.render(u'1 Player', 1, (255, 0, 0))
                                    menu2 = font3.render(u'Exit', 1, (255, 255, 10))
                                    game = 1
                                elif menupos3.collidepoint(event.pos):
                                    menu3 = font3.render(u'2 Players', 1, (255, 0, 0))
                                    menu = font3.render(u'1 Player', 1, (255, 225, 10))
                                    menu2 = font3.render(u'Exit', 1, (255, 255, 10))
                                    game = 3
                                else:
                                    menu3 = font3.render(u'2 Players', 1, (255, 255, 10))
                                    menu = font3.render(u'1 Player', 1, (255, 255, 10))
                                    menu2 = font3.render(u'Exit', 1, (255, 255, 10))
                                    game = 0
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                if game == 1:
                                        go = True
                                        done = False
                                elif game == 2:
                                        go = True
                                        done = True
                                elif game == 3:
                                        go = True
                                        done = False
                screen.fill(color)
                screen.blit(back, (0, 0))
                screen.blit(menu, menupos)
                screen.blit(menu2, menupos2)
                screen.blit(menu3, menupos3)
                pygame.display.flip()
mmenu(go)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    fight -= 1
    if initbase == True:
        bbase = Base(basehp)
        initbase = False
    if player == 1:
        player -= 1
        play = Player(ggx, ggy)

    screen.fill(color)
    pygame.draw.rect(screen, color2, (0, 0, 500, 500), 5)

    if zet == 0:
        play.render(screen)
    poleFFF(matrix)
    if bbase.basehp < 1 or plives < 1:
        screen.blit(text5, textpos5)
        if reloads != 0:
            reloads -= 1
        else:
            time.sleep(1)
            reloads = 60
            go = True
            done = True

    pygame.display.flip()
    clock.tick(30)
