# Audio management for music and sound effects
import os
import pygame

# Initialize music
pygame.mixer.init()

# Global state
music_muted = False
current_music = None  # Track what music is currently playing: "intro", "theme", or None
volume_level = 0.7  # Default volume level (0.0 to 1.0)

# Initialize volume
pygame.mixer.music.set_volume(volume_level)

# Import theme music mapping
from constants import THEME_MUSIC


def set_volume(volume):
    """Set the volume level (0.0 to 1.0)"""
    global volume_level
    volume_level = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
    try:
        pygame.mixer.music.set_volume(volume_level)
    except Exception:
        pass


def get_volume():
    """Get the current volume level (0.0 to 1.0)"""
    return volume_level


def play_music(theme="naruto"):
    """Play theme-specific background music"""
    global music_muted, current_music, volume_level
    if music_muted:
        return
    
    music_file = THEME_MUSIC.get(theme, "narutomusic.mp3")
    if os.path.exists(music_file):
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(volume_level)
            pygame.mixer.music.play(-1)
            current_music = "theme"
        except Exception:
            pass
    # Fallback to naruto music if theme music doesn't exist
    elif os.path.exists("narutomusic.mp3"):
        try:
            pygame.mixer.music.load("narutomusic.mp3")
            pygame.mixer.music.set_volume(volume_level)
            pygame.mixer.music.play(-1)
            current_music = "theme"
        except Exception:
            pass


def stop_music():
    global current_music
    try:
        pygame.mixer.music.stop()
        current_music = None
    except Exception:
        pass


def play_intro(force=False):
    """Play intro music. If force=False, only plays if not already playing."""
    global music_muted, current_music, volume_level
    if not music_muted and os.path.exists("intro.mp3"):
        # Only play if not already playing intro (unless forced)
        if not force and current_music == "intro" and pygame.mixer.music.get_busy():
            return
        try:
            pygame.mixer.music.load("intro.mp3")
            pygame.mixer.music.set_volume(volume_level)
            pygame.mixer.music.play(-1)
            current_music = "intro"
        except Exception:
            pass


def stop_intro():
    global current_music
    try:
        pygame.mixer.music.stop()
        current_music = None
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


def is_muted():
    """Check if music is currently muted"""
    return music_muted


def load_sound_effects():
    """Load sound effect files"""
    clap_sound = (
        pygame.mixer.Sound("clapsound.mp3") if os.path.exists("clapsound.mp3") else None
    )
    lose_sound = (
        pygame.mixer.Sound("losesound.mp3") if os.path.exists("losesound.mp3") else None
    )
    return clap_sound, lose_sound

