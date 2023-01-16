# главные константы приложения
WINDOW_SIZE = (0, 0)
FPS = 60
TITLE = "TANK 2023"

# звуковые файлы
BACKGROUND_MUSIC = "sounds/background_music.mp3"
START_EFFECT = "sounds/game_start.ogg"
BOOM_EFFECT = "sounds/boom.ogg"
SHOT_EFFECT = "sounds/shot.ogg"
KILLED_EFFECT = "sounds/destroy.ogg"

# игровые файлы
SOUNDS = [BACKGROUND_MUSIC, START_EFFECT, KILLED_EFFECT, BOOM_EFFECT, SHOT_EFFECT]
FILES = ["Objects/AI.py", "Objects/cells.py", "Objects/Field.py",
         "Objects/Game.py", "Objects/Player.py", "Objects/SoundManager.py", "Objects/windows.py",
         "Objects/Bullet.py", "Objects/explosions.py",
         "Support/colors.py", "Support/consts.py", "Support/events.py", "Support/ui.py",
         "Support/levels.txt", "Support/ai_settings.txt", "Support/company.txt", "Support/ai_queue.txt"]
LIBRARIES = ["pygame", "random"]

# игровые константы
FIELD_SIZE = (26, 26)
LEVELS_COUNT = 35

RELOAD_TIME = FPS * 3 // 4
MOVE_ANIMATION = FPS // 30
SPEED_ON_ICE = 0.5
BULLET_SPEED = 0.13
TANK_SPEED = 1 / 32
TANK_SIZE_KOEF = 0.85
PLAYER_LIVES = 3

GAME_END_FREEZE = FPS * 3 * 10

UPGRADE_CELLS_TIME = FPS * 200
BONUS_TIME = FPS * 15
BONUS_ANIMATION = 10
BONUS_LIFE = FPS * 7

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
BONUS = "Bonus"

NON_CONFLICT_OBJECTS = [BUSH, ICE, EXPLOSION, BONUS]

# звуковые константы
NORMAL_MUSIC_VOLUME = 0.8
NORMAL_EFFECTS_VOLUME = 0.4
STEP_VOLUME = 0.02
