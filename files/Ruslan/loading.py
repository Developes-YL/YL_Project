import pygame, sys, threading, os

pygame.init()
screen = pygame.display.set_mode((700, 500))
FONT = pygame.font.SysFont("Roboto", 100)
CLOCK = pygame.time.Clock()

WORK = 10000000

loading_bar = pygame.image.load("../images/Loading Bar.png")
loading_bar_rect = loading_bar.get_rect(midleft=(0, 500))
loading_finished = False
loading_progress = 0
loading_bar_width = 1

font = pygame.font.SysFont(None, 50)
img = font.render('LOADING...', True, 'RED')


def doWork():

	global loading_finished, loading_progress

	for i in range(WORK):
		math_equation = 523687 / 789456 * 89456
		loading_progress = i

	loading_finished = True


threading.Thread(target=doWork).start()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill("BLACK")

	loading_bar_width = loading_progress / WORK * 500

	loading_bar = pygame.transform.scale(loading_bar, (int(loading_bar_width), 30))
	loading_bar_rect = loading_bar.get_rect(midleft=(100, 400))

	screen.blit(loading_bar, loading_bar_rect)
	screen.blit(img, (450, 350))

	pygame.display.update()
	CLOCK.tick(60)