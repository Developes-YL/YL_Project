# главные константы приложения
WINDOW_SIZE = (0, 0)
FPS = 60
TITLE = "TANK 1990"

FILES = []
LIBRARIES = []

# игровые константы
FIELD_SIZE = (26, 26)

RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3

BULLET = "Bullet"
AI = "AI"
PLAYER = "Player"
BRICK = "Brick"
CONCRETE = "Concrete"
BUSH = "Bush"
WATER = "Water"
EXPLOSION = "Explosion"
BORDER = "Border"
ICE = "Ice"
BIG_EXPLOSION = "BigExplosion"

NON_CONFLICT_OBJECTS = [BUSH, ICE, EXPLOSION, BIG_EXPLOSION]

RELOAD_TIME = FPS * 3 // 2
MOVE_ANIMATION = FPS // 30

SPEED_ON_ICE = 0.5
BULLET_SPEED = 0.05

#Музыка

VOL = 0.06
VOL_EFFECTS = 0.2
