# Audio management for music and sound effects
import os
import pygame

# Initialize music
pygame.mixer.init()

# Global state
music_muted = False

# Import theme music mapping
from constants import THEME_MUSIC


def play_music(theme="naruto"):
    """Play theme-specific background music"""
    global music_muted
    if music_muted:
        return
    
    music_file = THEME_MUSIC.get(theme, "narutomusic.mp3")
    if os.path.exists(music_file):
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)
        except Exception:
            pass
    # Fallback to naruto music if theme music doesn't exist
    elif os.path.exists("narutomusic.mp3"):
        try:
            pygame.mixer.music.load("narutomusic.mp3")
            pygame.mixer.music.play(-1)
        except Exception:
            pass


def stop_music():
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass


def play_intro():
    global music_muted
    if not music_muted and os.path.exists("intro.mp3"):
        try:
            pygame.mixer.music.load("intro.mp3")
            pygame.mixer.music.play(-1)
        except Exception:
            pass


def stop_intro():
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass


def toggle_mute(mute_btn=None):
    global music_muted
    music_muted = not music_muted
    if music_muted:
        stop_music()
        if mute_btn:
            mute_btn.configure(text="🔇")  # Muted icon
    else:
        play_intro()
        if mute_btn:
            mute_btn.configure(text="🔊")  # Unmuted icon


def load_sound_effects():
    """Load sound effect files"""
    clap_sound = (
        pygame.mixer.Sound("clapsound.mp3") if os.path.exists("clapsound.mp3") else None
    )
    lose_sound = (
        pygame.mixer.Sound("losesound.mp3") if os.path.exists("losesound.mp3") else None
    )
    return clap_sound, lose_sound

