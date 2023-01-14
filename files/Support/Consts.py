# главные константы приложения
WINDOW_SIZE = (0, 0)
FPS = 60
TITLE = "TANK 1990"

# sounds
BACKGROUND_MUSIC = "sounds/background_music.mp3"
START_EFFECT = "sounds/game_start.ogg"
TEST_EFFECT = "sounds/test_effect.ogg"
HIT_EFFECT = "sounds/hit_effect.ogg"
READY_EFFECT = "sounds/ready.ogg"

# игровые файлы
SOUNDS = [BACKGROUND_MUSIC, START_EFFECT, TEST_EFFECT, HIT_EFFECT, READY_EFFECT]
FILES = ["Objects/AI.py", "Objects/cells.py", "Objects/fields.py",
         "Objects/Game.py", "Objects/Player.py", "Objects/SoundManager.py", "Objects/Windows.py",
         "Support/colors.py", "Support/Consts.py", "Support/events.py", "Support/ui.py",
         "Support/levels.txt", "Support/ai_settings.txt"]
LIBRARIES = ["pygame"]

# игровые константы
FIELD_SIZE = (26, 26)

RELOAD_TIME = FPS * 1 // 2
MOVE_ANIMATION = FPS // 15

SPEED_ON_ICE = 0.5
BULLET_SPEED = 0.09
TANK_SPEED = 1 / 32
TANK_SIZE_KOEF = 0.85

GAME_END_FREEZE = FPS * 3 * 10
LEVELS_COUNT = 35

# константы, используемые для удобства разработки
RIGHT = 0
UP = 3
LEFT = 2
DOWN = 1

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

# Музыка
NORMAL_MUSIC_VOLUME = 0.08
NORMAL_EFFECTS_VOLUME = 0.2
STEP_VOLUME = 0.02
