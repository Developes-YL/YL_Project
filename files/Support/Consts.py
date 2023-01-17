# главные константы приложения
WINDOW_SIZE = (0, 0)
FPS = 60
TITLE = "TANK 1990"

# sounds
BACKGROUND_MUSIC = "sounds/background_music.mp3"
START_EFFECT = "sounds/game_start.ogg"
BOOM_EFFECT = "sounds/boom.ogg"
SHOT_EFFECT = "sounds/shot.ogg"
KILLED_EFFECT = "sounds/destroy.ogg"

# игровые файлы
SOUNDS = [BACKGROUND_MUSIC, START_EFFECT, KILLED_EFFECT, BOOM_EFFECT]
FILES = ["Objects/AI.py", "Objects/cells.py", "Objects/fields.py",
         "Objects/Game.py", "Objects/Player.py", "Objects/SoundManager.py", "Objects/windows.py",
         "Support/colors.py", "Support/consts.py", "Support/events.py", "Support/ui.py",
         "Support/levels.txt", "Support/ai_settings.txt"]
LIBRARIES = ["pygame"]

# игровые константы
FIELD_SIZE = (26, 26)

RELOAD_TIME = FPS * 1 // 2
MOVE_ANIMATION = FPS // 30

SPEED_ON_ICE = 0.5
BULLET_SPEED = 0.11
TANK_SPEED = 1 / 32
TANK_SIZE_KOEF = 0.85

GAME_END_FREEZE = FPS * 3 * 10
LEVELS_COUNT = 35

<<<<<<< Updated upstream:files/Support/Consts.py
PLAYER_LIVES = 1
=======
UPGRADE_CELLS_TIME = FPS * 200
BONUS_TIME = FPS * 2
BONUS_ANIMATION = 10
BONUS_LIFE = FPS * 9
>>>>>>> Stashed changes:files/Support/consts.py

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
NORMAL_MUSIC_VOLUME = 0.04
NORMAL_EFFECTS_VOLUME = 0.2
STEP_VOLUME = 0.02
