
import pygame
from pygame import image


def load_image(name: str):
    """загрузка картинки, если такая есть"""
    try:
        img = image.load(name)
    except OSError:
        img = pygame.Surface((1, 1))
    return img


# backgrounds
BG1 = load_image('images/other/bg1.png')
SETTINGS1 = load_image('images/other/settings.png')

# cells
BRICK_IMAGE = load_image('images/cells/brick.png')
CONCRETE_IMAGE = load_image('images/cells/concrete.png')
WATER_IMAGE = load_image('images/cells/water1.png')
BUSH_IMAGE = load_image('images/cells/bush.png')
ICE_IMAGE = load_image('images/cells/ice.png')

# tanks
TANK = load_image('images/tank_1_player.png')
TANK2 = image.load('images/original/tank_2_player.png')
TANK_PLAYER_1 = [TANK, TANK2]

TANK_AI_1_1 = load_image('images/tanks/TANK_AI_1_1.png')
TANK_AI_1_2 = load_image('images/tanks/TANK_AI_1_2.png')
TANK_AI_1 = [TANK_AI_1_1, TANK_AI_1_2]

TANK_AI_2_1 = load_image('images/tanks/TANK_AI_2_1.png')
TANK_AI_2_2 = load_image('images/tanks/TANK_AI_2_2.png')
TANK_AI_2 = [TANK_AI_2_1, TANK_AI_2_2]

TANK_AI_1_ = load_image('images/tanks/tank_1_ai.png')
TANK_AI_2_ = load_image('images/tanks/tank_2_ai.png')
TANK_AI_3 = load_image('images/tanks/tank_3_ai.png')
TANK_AI_4 = load_image('images/tanks/tank_4_ai.png')

TANK_AI = [TANK_AI_1, TANK_AI_2]

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
