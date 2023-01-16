
import pygame
from pygame import image


def load_image(name: str):
    """загрузка картинки, если такая есть"""
    try:
        img = image.load(name)
    except FileNotFoundError:
        print("Не найдена картинка " + name)
        img = pygame.Surface((1, 1))
    return img


# фоны
BG1 = load_image('images/other/bg1.png')
BG_WIN = load_image('images/other/winner.png')
BG_LOSE = load_image('images/other/defeat.png')
SETTINGS1 = load_image('images/other/settings.png')

# клетки
BRICK_IMAGE = load_image('images/cells/brick.png')
CONCRETE_IMAGE = load_image('images/cells/concrete.png')
WATER_IMAGE = load_image('images/cells/water1.png')
BUSH_IMAGE = load_image('images/cells/bush.png')
ICE_IMAGE = load_image('images/cells/ice.png')

BASE_1_IMAGE = load_image('images/cells/BASE_1.png')
BASE_2_IMAGE = load_image('images/cells/BASE_2.png')

STAR_BONUS = load_image('images/cells/star.png')
GRENADE_BONUS = load_image('images/cells/GRENADE.png')
SHOVEL_BONUS = load_image('images/cells/SHOVEL.png')

# танки
# игрока:
TANK_PLAYER_1_1 = load_image('images/tanks/TANK_PLAYER_1_1.png')
TANK_PLAYER_1_2 = load_image('images/tanks/TANK_PLAYER_1_2.png')
TANK_PLAYER_1 = [TANK_PLAYER_1_1, TANK_PLAYER_1_2]

TANK_PLAYER_4_1 = load_image('images/tanks/TANK_PLAYER_4_1.png')
TANK_PLAYER_4_2 = load_image('images/tanks/TANK_PLAYER_4_2.png')
TANK_PLAYER_4 = [TANK_PLAYER_4_1, TANK_PLAYER_4_2]

TANK_PLAYER = [TANK_PLAYER_1, TANK_PLAYER_4]

# бота:
TANK_AI_1_1_G = load_image('images/tanks/TANK_AI_1_1_G.png')
TANK_AI_1_2_G = load_image('images/tanks/TANK_AI_1_2_G.png')
TANK_AI_1_1_R = load_image('images/tanks/TANK_AI_1_1_R.png')
TANK_AI_1_2_R = load_image('images/tanks/TANK_AI_1_2_R.png')
TANK_AI_1_1_GR = load_image('images/tanks/TANK_AI_1_1_GR.png')
TANK_AI_1_2_GR = load_image('images/tanks/TANK_AI_1_2_GR.png')
TANK_AI_1 = [[TANK_AI_1_1_G, TANK_AI_1_2_G], [TANK_AI_1_1_R, TANK_AI_1_2_R], [TANK_AI_1_1_GR, TANK_AI_1_2_GR]]

TANK_AI_2_1_G = load_image('images/tanks/TANK_AI_2_1_G.png')
TANK_AI_2_2_G = load_image('images/tanks/TANK_AI_2_2_G.png')
TANK_AI_2_1_R = load_image('images/tanks/TANK_AI_2_1_R.png')
TANK_AI_2_2_R = load_image('images/tanks/TANK_AI_2_2_R.png')
TANK_AI_2_1_GR = load_image('images/tanks/TANK_AI_2_1_GR.png')
TANK_AI_2_2_GR = load_image('images/tanks/TANK_AI_2_2_GR.png')
TANK_AI_2 = [[TANK_AI_2_1_G, TANK_AI_2_2_G], [TANK_AI_2_1_R, TANK_AI_2_2_R], [TANK_AI_2_1_GR, TANK_AI_2_2_GR]]

TANK_AI_3_1_G = load_image('images/tanks/TANK_AI_3_1_G.png')
TANK_AI_3_2_G = load_image('images/tanks/TANK_AI_3_2_G.png')
TANK_AI_3_1_R = load_image('images/tanks/TANK_AI_3_1_R.png')
TANK_AI_3_2_R = load_image('images/tanks/TANK_AI_3_2_R.png')
TANK_AI_3_1_GR = load_image('images/tanks/TANK_AI_3_1_GR.png')
TANK_AI_3_2_GR = load_image('images/tanks/TANK_AI_3_2_GR.png')
TANK_AI_3 = [[TANK_AI_3_1_G, TANK_AI_3_2_G], [TANK_AI_3_1_R, TANK_AI_3_2_R], [TANK_AI_3_1_GR, TANK_AI_3_2_GR]]

TANK_AI_4_1_G = load_image('images/tanks/TANK_AI_4_1_G.png')
TANK_AI_4_2_G = load_image('images/tanks/TANK_AI_4_2_G.png')
TANK_AI_4_1_R = load_image('images/tanks/TANK_AI_4_1_R.png')
TANK_AI_4_2_R = load_image('images/tanks/TANK_AI_4_2_R.png')
TANK_AI_4_1_GR = load_image('images/tanks/TANK_AI_4_1_GR.png')
TANK_AI_4_2_GR = load_image('images/tanks/TANK_AI_4_2_GR.png')
TANK_AI_4 = [[TANK_AI_4_1_G, TANK_AI_4_2_G], [TANK_AI_4_1_R, TANK_AI_4_2_R], [TANK_AI_4_1_GR, TANK_AI_4_2_GR]]

TANK_AI = [TANK_AI_1, TANK_AI_2, TANK_AI_3, TANK_AI_4]

# other
BULLET_IMAGE = load_image('images/cells/bullet.png')

EXPLOSION_1 = load_image('images/animations/explosion_1.png')
EXPLOSION_2 = load_image('images/animations/explosion_2.png')
EXPLOSION_3 = load_image('images/animations/explosion_3.png')

PAUSE_RED = load_image('images/buttons/PAUSE_RED.png')
PAUSE_WHITE = load_image('images/buttons/PAUSE_WHITE.png')
PLAY_RED = load_image('images/buttons/PLAY_RED.png')
PLAY_WHITE = load_image('images/buttons/PLAY_WHITE.png')
RESTART_RED = load_image('images/buttons/RESTART_RED.png')
RESTART_WHITE = load_image('images/buttons/RESTART_WHITE.png')
