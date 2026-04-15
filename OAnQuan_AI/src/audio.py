import pygame
from pathlib import Path

_sound_effects = {}
_bgm = None


def init_audio():
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
    except Exception:
        return

    sound_folder = Path(__file__).resolve().parent.parent / "assets" / "sound"
    bgm_path = sound_folder / "bgm.mp3"
    move_sound_path = sound_folder / "moveee.wav"

    if not bgm_path.exists():
        alt_bgm = sound_folder / "bmg.mp3"
        if alt_bgm.exists():
            bgm_path = alt_bgm

    if not move_sound_path.exists():
        alt_move = sound_folder / "move.mp3"
        if alt_move.exists():
            move_sound_path = alt_move

    if bgm_path.exists():
        try:
            pygame.mixer.music.load(str(bgm_path))
        except Exception:
            pass

    if move_sound_path.exists():
        try:
            _sound_effects["move"] = pygame.mixer.Sound(str(move_sound_path))
        except Exception:
            pass


def play_bgm(loops=-1):
    try:
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy() is False:
            pygame.mixer.music.play(loops=loops)
    except Exception:
        pass


def play_move_sound():
    try:
        sound = _sound_effects.get("move")
        if sound:
            sound.play()
    except Exception:
        pass


def stop_bgm():
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except Exception:
        pass
