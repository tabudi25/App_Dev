# Navigation and frame switching functions
import tkinter as tk
from audio import play_intro, stop_music, play_music

# Global state
current_theme = "naruto"
themes_frame_ref = None


def go_to(frame, home_frame=None):
    """Navigate to a specific frame"""
    frame.lift()
    # If we returned to home, ensure intro is playing (unless muted)
    if home_frame and frame is home_frame:
        try:
            play_intro()
        except Exception:
            pass


def exit_app(root):
    """Exit the application"""
    root.destroy()


def go_to_narutogame(size=4, naruto_frame=None, game_frame=None):
    """Navigate to Naruto game"""
    global current_theme
    from game_logic import reset_game
    current_theme = "naruto"
    if naruto_frame:
        naruto_frame.lower()
    if game_frame:
        game_frame.lift()
    play_music("naruto")
    reset_game(size, theme=current_theme)


def go_to_opgame(size=4, onepiece_frame=None, game_frame=None):
    """Navigate to One Piece game"""
    global current_theme
    from game_logic import reset_game
    current_theme = "op"
    if onepiece_frame:
        onepiece_frame.lower()
    if game_frame:
        game_frame.lift()
    play_music("op")
    reset_game(size, theme=current_theme)


def go_to_slamgame(size=4, slamdunk_frame=None, game_frame=None):
    """Navigate to Slam Dunk game"""
    global current_theme
    from game_logic import reset_game
    current_theme = "slam"
    if slamdunk_frame:
        slamdunk_frame.lower()
    if game_frame:
        game_frame.lift()
    play_music("slam")
    reset_game(size, theme=current_theme)


def go_to_dbgame(size=4, dragonball_frame=None, game_frame=None):
    """Navigate to Dragon Ball game"""
    global current_theme
    from game_logic import reset_game
    current_theme = "db"
    if dragonball_frame:
        dragonball_frame.lower()
    if game_frame:
        game_frame.lift()
    play_music("db")
    reset_game(size, theme=current_theme)


def go_to_bleachgame(size=4, bleach_frame=None, game_frame=None):
    """Navigate to Bleach game"""
    global current_theme
    from game_logic import reset_game
    current_theme = "bleach"
    if bleach_frame:
        bleach_frame.lower()
    if game_frame:
        game_frame.lift()
    play_music("bleach")
    reset_game(size, theme=current_theme)


def back_to_themes(game_frame=None, themes_frame=None, result_label=None, 
                   win_overlay=None, flip_overlay=None, time_overlay=None,
                   pause_menu_box=None, clap_sound=None, lose_sound=None):
    """Return to theme menu, reset states"""
    from game_logic import cancel_timer
    
    cancel_timer()
    stop_music()
    if clap_sound:
        clap_sound.stop()
    if lose_sound:
        lose_sound.stop()
    if result_label:
        result_label.config(text="")
        result_label.lower()
    if win_overlay:
        win_overlay.lower()
    if flip_overlay:
        flip_overlay.lower()
    if time_overlay:
        time_overlay.lower()
    if pause_menu_box:
        pause_menu_box.lower()
    if game_frame:
        game_frame.lower()
    if themes_frame:
        themes_frame.lift()


def get_current_theme():
    """Get the current theme"""
    return current_theme


def set_themes_frame(themes_frame):
    """Set the themes frame reference"""
    global themes_frame_ref
    themes_frame_ref = themes_frame


def get_themes_frame():
    """Get the themes frame reference"""
    return themes_frame_ref

