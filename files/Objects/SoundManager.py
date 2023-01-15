
from pygame import mixer

from files.Support.consts import BACKGROUND_MUSIC, STEP_VOLUME, NORMAL_EFFECTS_VOLUME, NORMAL_MUSIC_VOLUME, \
    START_EFFECT, BOOM_EFFECT, KILLED_EFFECT, SHOT_EFFECT

from files.Support.events import VOLUME_UP, STANDART_VOLUME, BACKGROUND_MUSIC_EVENT, VOLUME_DOWN, START_EFFECT_EVENT, \
    AI_DESTROYED, PLAYER_KILLED, SHOT_EFFECT_EVENT


class SoundManager:
    """управляющий музыкой"""
    def __init__(self):
        self.step = STEP_VOLUME
        self.effect_volume = NORMAL_EFFECTS_VOLUME
        self.music_volume = NORMAL_MUSIC_VOLUME
        self.music_play = False

    def volume_up(self, is_music: bool = True):
        """увелечение громкости"""
        if is_music:
            self.music_volume += self.step
        else:
            self.effect_volume += self.step
        if self.music_play and is_music:
            mixer.music.set_volume(self.music_volume)

    def volume_down(self, is_music: bool = True):
        """уменьшение громкости"""
        if is_music:
            self.music_volume = max(self.music_volume - self.step, 0)
        else:
            self.effect_volume = max(self.effect_volume - self.step, 0)
        if self.music_play and is_music:
            mixer.music.set_volume(self.music_volume)

    def standart_volume(self, is_music: bool = True):
        """возрват звука по умолчанию"""
        if is_music:
            self.music_volume = NORMAL_MUSIC_VOLUME
        else:
            self.effect_volume = NORMAL_EFFECTS_VOLUME
        if self.music_play and is_music:
            mixer.music.set_volume(self.music_volume)

    def update(self, events):
        """обработка звуковых событий"""
        for event in events:
            if event.type == VOLUME_UP:
                self.volume_up(event.music)
            elif event.type == VOLUME_DOWN:
                self.volume_down(event.music)
            elif event.type == STANDART_VOLUME:
                self.standart_volume(event.music)

            elif event.type == BACKGROUND_MUSIC_EVENT:
                self.music_play = True
                mixer.music.load(BACKGROUND_MUSIC)
                mixer.music.play(-1)
                mixer.music.set_volume(self.music_play)

            elif event.type == START_EFFECT_EVENT:
                sound = mixer.Sound(START_EFFECT)
                sound.set_volume(self.effect_volume)
                sound.play()
            elif event.type == SHOT_EFFECT_EVENT:
                sound = mixer.Sound(SHOT_EFFECT)
                sound.set_volume(self.effect_volume)
                sound.play()
            elif event.type == AI_DESTROYED:
                sound = mixer.Sound(BOOM_EFFECT)
                sound.set_volume(self.effect_volume * 15)
                sound.play()
            elif event.type == PLAYER_KILLED:
                sound = mixer.Sound(KILLED_EFFECT)
                sound.set_volume(self.effect_volume * 20)
                sound.play()
