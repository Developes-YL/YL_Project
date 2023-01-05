# -*- coding: UTF-8 -*-
import pygame

pygame.init()
size = 700, 500
screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption('TANK 1990')
clock = pygame.time.Clock()
color = 0, 0, 0
font3 = pygame.font.Font(None, 64)
go = False
done = False
lvl1 = font3.render(u'Level 1', 1, (255, 0, 0))
menupos = pygame.Rect(250, 60, 200, 75)
back_btn = font3.render(u'Back', 1, (255, 0, 0))
menupos2 = pygame.Rect(590, 450, 154, 45)
lvl2 = font3.render(u'Level 2', 1, (255, 0, 0))
menupos3 = pygame.Rect(250, 120, 200, 75)
lvl3 = font3.render(u'Level 3', 1, (255, 0, 0))
menupos4 = pygame.Rect(250, 180, 200, 75)
lvl4 = font3.render(u'Level 4', 1, (255, 0, 0))
menupos5 = pygame.Rect(250, 240, 200, 75)
lvl5 = font3.render(u'Level 5', 1, (255, 0, 0))
menupos6 = pygame.Rect(250, 300, 200, 75)


def mmenu(go):
    global lvl1, back_btn, menupos, menupos2, done, lvl2, menupos3, lvl3, menupos4, lvl4, menupos5, lvl5, menupos6
    while not go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                go = True
            elif event.type == pygame.MOUSEMOTION:
                if menupos2.collidepoint(event.pos):
                    lvl2 = font3.render(u'Level 2', 1, (255, 0, 0))
                    back_btn = font3.render(u'Back', 1, (255, 255, 255))
                    lvl1 = font3.render(u'Level 1', 1, (255, 0, 0))
                    lvl3 = font3.render(u'Level 3', 1, (255, 0, 0))
                    lvl4 = font3.render(u'Level 4', 1, (255, 0, 0))
                    lvl5 = font3.render(u'Level 5', 1, (255, 0, 0))
                    game = 2
                elif menupos.collidepoint(event.pos):
                    lvl2 = font3.render(u'Level 2', 1, (255, 0, 0))
                    lvl1 = font3.render(u'Level 1', 1, (255, 255, 255))
                    back_btn = font3.render(u'Back', 1, (255, 0, 0))
                    lvl3 = font3.render(u'Level 3', 1, (255, 0, 0))
                    lvl4 = font3.render(u'Level 4', 1, (255, 0, 0))
                    lvl5 = font3.render(u'Level 5', 1, (255, 0, 0))
                    game = 1
                elif menupos3.collidepoint(event.pos):
                    lvl2 = font3.render(u'Level 2', 1, (255, 255, 255))
                    lvl1 = font3.render(u'Level 1', 1, (255, 0, 0))
                    back_btn = font3.render(u'Back', 1, (255, 0, 0))
                    lvl3 = font3.render(u'Level 3', 1, (255, 0, 0))
                    lvl4 = font3.render(u'Level 4', 1, (255, 0, 0))
                    lvl5 = font3.render(u'Level 5', 1, (255, 0, 0))
                    game = 3
                elif menupos4.collidepoint(event.pos):
                    lvl2 = font3.render(u'Level 2', 1, (255, 0, 0))
                    lvl1 = font3.render(u'Level 1', 1, (255, 0, 0))
                    back_btn = font3.render(u'Back', 1, (255, 0, 0))
                    lvl3 = font3.render(u'Level 3', 1, (255, 255, 255))
                    lvl4 = font3.render(u'Level 4', 1, (255, 0, 0))
                    lvl5 = font3.render(u'Level 5', 1, (255, 0, 0))
                    game = 3
                elif menupos5.collidepoint(event.pos):
                    lvl2 = font3.render(u'Level 2', 1, (255, 0, 0))
                    lvl1 = font3.render(u'Level 1', 1, (255, 0, 0))
                    back_btn = font3.render(u'Back', 1, (255, 0, 0))
                    lvl3 = font3.render(u'Level 3', 1, (255, 0, 0))
                    lvl4 = font3.render(u'Level 4', 1, (255, 255, 255))
                    lvl5 = font3.render(u'Level 5', 1, (255, 0, 0))
                    game = 3
                elif menupos6.collidepoint(event.pos):
                    lvl2 = font3.render(u'Level 2', 1, (255, 0, 0))
                    lvl1 = font3.render(u'Level 1', 1, (255, 0, 0))
                    back_btn = font3.render(u'Back', 1, (255, 0, 0))
                    lvl3 = font3.render(u'Level 3', 1, (255, 0, 0))
                    lvl4 = font3.render(u'Level 4', 1, (255, 0, 0))
                    lvl5 = font3.render(u'Level 5', 1, (255, 255, 255))
                    game = 3
                else:
                    lvl2 = font3.render(u'Level 2', 1, (255, 0, 0))
                    lvl1 = font3.render(u'Level 1', 1, (255, 0, 0))
                    back_btn = font3.render(u'Back', 1, (255, 0, 0))
                    lvl3 = font3.render(u'Level 3', 1, (255, 0, 0))
                    lvl4 = font3.render(u'Level 4', 1, (255, 0, 0))
                    lvl5 = font3.render(u'Level 5', 1, (255, 0, 0))
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
        screen.blit(lvl1, menupos)
        screen.blit(back_btn, menupos2)
        screen.blit(lvl2, menupos3)
        screen.blit(lvl3, menupos4)
        screen.blit(lvl4, menupos5)
        screen.blit(lvl5, menupos6)
        pygame.display.flip()

mmenu(go)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(color)
    pygame.draw.rect(screen, color, (0, 0, 500, 500), 5)
    pygame.display.flip()
    clock.tick(30)