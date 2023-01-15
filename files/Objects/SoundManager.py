
from pygame import mixer

from files.Support.consts import BACKGROUND_MUSIC, STEP_VOLUME, NORMAL_EFFECTS_VOLUME, NORMAL_MUSIC_VOLUME, \
    START_EFFECT, TEST_EFFECT, HIT_EFFECT, READY_EFFECT

from files.Support.events import VOLUME_UP, STANDART_VOLUME, BACKGROUND_MUSIC_EVENT, VOLUME_DOWN, START_EFFECT_EVENT, \
    TEST_EFFECT_EVENT, HIT_EFFECT_EVENT, READY_EFFECT_EVENT


class SoundManager:
    """управляющий музыкой"""
    def __init__(self):
        self.step = STEP_VOLUME
        self.effect_volume = NORMAL_EFFECTS_VOLUME
        self.music_volume = NORMAL_MUSIC_VOLUME
        self.music_play = False

    def play(self, number: int = 0):
        """настройка и включение эффектов и музыки"""
        if number == 1:
            self.music_play = True
            mixer.music.load(BACKGROUND_MUSIC)
            mixer.music.play(-1)
            mixer.music.set_volume(self.music_play)
        elif number == 2:
            sound = mixer.Sound(START_EFFECT)
            sound.set_volume(self.effect_volume)
            sound.play()
        elif number == 3:
            sound = mixer.Sound(TEST_EFFECT)
            sound.set_volume(self.effect_volume)
            sound.play()
        elif number == 4:
            sound = mixer.Sound(HIT_EFFECT)
            sound.set_volume(self.effect_volume)
            sound.play()
        elif number == 5:
            sound = mixer.Sound(READY_EFFECT)
            sound.set_volume(self.effect_volume)
            sound.play()

    def volume_up(self, flag: bool = True):
        """увелечение громкости"""
        if flag:
            self.music_volume += self.step
        else:
            self.effect_volume += self.step
        if self.music_play and flag:
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
                self.play(1)
            elif event.type == START_EFFECT_EVENT:
                self.play(2)
            elif event.type == TEST_EFFECT_EVENT:
                self.play(3)
            elif event.type == HIT_EFFECT_EVENT:
                self.play(4)
            elif event.type == READY_EFFECT_EVENT:
                self.play(5)