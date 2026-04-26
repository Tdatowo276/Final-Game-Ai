import pygame
from pathlib import Path
from src.utils import get_resource_path

_sound_effects = []
_bgm = None
bgm_volume = 0.5
sfx_index = 0

SFX_FILES = [
    "bubble-pop.wav",
    "moveee.wav",
    "tiengnuoc.mp3"
]
SFX_NAMES = [
    "Bong Bóng Nổ",
    "Rải Sỏi",
    "Nước Rơi"
]

def init_audio():
    global _sound_effects
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
    except Exception:
        return

    # Use get_resource_path to find assets even when bundled
    sound_folder = Path(get_resource_path("assets/sound"))
    
    # Load BGM
    bgm_path = sound_folder / "bgm.mp3"
    if not bgm_path.exists():
        bgm_path = sound_folder / "bmg.mp3"
    if bgm_path.exists():
        try:
            pygame.mixer.music.load(str(bgm_path))
            pygame.mixer.music.set_volume(bgm_volume)
        except Exception:
            pass

    # Load SFX
    _sound_effects = []
    for sfx_name in SFX_FILES:
        path = sound_folder / sfx_name
        if path.exists():
            try:
                snd = pygame.mixer.Sound(str(path))
                _sound_effects.append(snd)
            except Exception:
                _sound_effects.append(None)
        else:
            _sound_effects.append(None)

def play_bgm(loops=-1):
    try:
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy() is False:
            pygame.mixer.music.set_volume(bgm_volume)
            pygame.mixer.music.play(loops=loops)
    except Exception:
        pass

def play_move_sound():
    try:
        if 0 <= sfx_index < len(_sound_effects):
            sound = _sound_effects[sfx_index]
            if sound:
                # We can either use bgm_volume or keep SFX at 100%
                # Most users like SFX to be slightly quieter if BGM is quiet
                sound.set_volume(bgm_volume + 0.2 if bgm_volume < 0.8 else 1.0)
                sound.play()
    except Exception:
        pass

def stop_bgm():
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except Exception:
        pass

def adjust_bgm_volume(delta):
    global bgm_volume
    bgm_volume = max(0.0, min(1.0, bgm_volume + delta))
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(bgm_volume)
    except Exception:
        pass
    return bgm_volume

def cycle_sfx():
    global sfx_index
    sfx_index = (sfx_index + 1) % len(SFX_FILES)
    return SFX_NAMES[sfx_index]

def get_current_sfx_name():
    return SFX_NAMES[sfx_index]
