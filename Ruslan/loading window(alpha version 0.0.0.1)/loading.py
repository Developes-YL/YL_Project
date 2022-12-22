import pygame, sys, threading

pygame.init()
screen = pygame.display.set_mode((1280, 720))
FONT = pygame.font.SysFont("Roboto", 100)
CLOCK = pygame.time.Clock()

WORK = 10000000

LOADING_BG = pygame.image.load("Loading Bar Background.png")
LOADING_BG_RECT = LOADING_BG.get_rect(center=(640, 360))

loading_bar = pygame.image.load("Loading Bar.png")
loading_bar_rect = loading_bar.get_rect(midleft=(280, 360))
loading_finished = False
loading_progress = 0
loading_bar_width = 8

font = pygame.font.SysFont(None, 90)
img = font.render('LOADING...', True, '#e24167')


def doWork():

	global loading_finished, loading_progress

	for i in range(WORK):
		math_equation = 523687 / 789456 * 89456
		loading_progress = i

	loading_finished = True

finished = FONT.render("Done!", True, "white")
finished_rect = finished.get_rect(center=(640, 360))

threading.Thread(target=doWork).start()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill("#0d0e2e")


	loading_bar_width = loading_progress / WORK * 720

	loading_bar = pygame.transform.scale(loading_bar, (int(loading_bar_width), 150))
	loading_bar_rect = loading_bar.get_rect(midleft=(280, 360))

	screen.blit(LOADING_BG, LOADING_BG_RECT)
	screen.blit(loading_bar, loading_bar_rect)
	screen.blit(img, (500, 180))

	pygame.display.update()
	CLOCK.tick(60)