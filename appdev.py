# FULL CODE: Multi-theme Flip Memory Game (shared game frame; different image sets per theme)
# Save as e.g. memory_game.py and run with Python 3 (Pillow & pygame required).
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import customtkinter as ctk
import random, time, pygame, os
from tkinter import font

import pywinstyles


# --- Initialize music ---
pygame.mixer.init()

# --- Load custom font ---
def load_custom_font():
    """Load Arcade Classic font with multiple fallback methods"""
    # Check if font file exists in the directory
    font_files = ["Arcade Classic.ttf", "ARCADECLASSIC.TTF", "ArcadeClassic.ttf", "ArcadeClassic.otf", 
                  "arcadeclassic.ttf", "arcadeclassic.otf", "Arcade Classic.otf",
                  "PressStart2P.ttf", "PressStart2P.otf", "pressstart2p.ttf", "pressstart2p.otf",
                  "ARCADECLASSIC.OTF"]
    font_file_found = None
    
    for font_file in font_files:
        if os.path.exists(font_file):
            font_file_found = font_file
            print(f"Found font file: {font_file}")
            break
    
    if font_file_found:
        try:
            # First, try to install the font to Windows
            try:
                import shutil
                fonts_dir = os.path.join(os.environ['WINDIR'], 'Fonts')
                font_dest = os.path.join(fonts_dir, os.path.basename(font_file_found))
                
                # Copy font to Windows Fonts directory if not already there
                if not os.path.exists(font_dest):
                    try:
                        shutil.copy2(font_file_found, font_dest)
                        print(f"Font copied to Windows Fonts directory")
                    except PermissionError:
                        print(f"Note: Could not copy font automatically. Please install {font_file_found} manually.")
                else:
                    print(f"Font already in Windows Fonts directory")
                
                # Try to register font using win32api if available
                try:
                    import win32api
                    import win32con
                    win32api.AddFontResource(font_dest)
                    win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_FONTCHANGE, 0, 0)
                    print(f"Font registered with Windows")
                except ImportError:
                    pass  # pywin32 not available, but font is copied
                except Exception as e:
                    print(f"Note: Could not register font: {e}")
            except Exception as e:
                print(f"Note: Font installation attempt: {e}")
            
            # Now try to load the font
            import tkinter.font as tkfont
            root_temp = tk.Tk()
            root_temp.withdraw()  # Hide the temporary window
            
            # Determine font family name from file
            if "PressStart2P" in font_file_found or "pressstart2p" in font_file_found:
                font_family = "Press Start 2P"
            else:
                font_family = "Arcade Classic"
            
            # Try to load font by family name (after installation attempt)
            try:
                custom_font = tkfont.Font(family=font_family, size=12)
                actual_font = custom_font.actual()
                actual_family = actual_font.get('family', '')
                
                # Check if it actually loaded the right font (not a fallback)
                if font_family.lower() in actual_family.lower() or 'arcade' in actual_family.lower():
                    root_temp.destroy()
                    print(f"Successfully loaded font: {actual_family}")
                    return actual_family
                else:
                    # Font not installed yet, but we'll return the name anyway
                    print(f"Font '{font_family}' not yet available, but will be used when installed")
                    root_temp.destroy()
                    return font_family
            except Exception as e:
                print(f"Could not load font by name: {e}")
                root_temp.destroy()
                return font_family
        except Exception as e:
            print(f"Error loading font file: {e}")
    
    # Try different arcade font name variations (most common first)
    font_candidates = [
        "Arcade Classic", "ArcadeClassic", "ARCADECLASSIC", "Arcade Classic Regular",
        "Press Start 2P", "PressStart2P", "Press Start",
        "Arcade", "Arcade Interlaced", "Arcade Rounded", "Arcade Normal",
        "Courier New", "Lucida Console", "Consolas", "Fixedsys", "Terminal"  # Monospace fallbacks with retro feel
    ]
    
    for font_candidate in font_candidates:
        try:
            # Try to create a font object
            test_font = font.Font(family=font_candidate, size=12)
            # Verify it actually works
            test_font.actual()
            # If successful, return the font name
            print(f"Using system font: {font_candidate}")
            return font_candidate
        except:
            continue
    
    # If all attempts fail, use monospace fallback (more arcade-like than Arial)
    print("Arcade Classic font not found, using Courier New as fallback")
    print("To get Arcade Classic font, download from: https://www.dafont.com/arcade-classic.font")
    return "Courier New"

font_name = load_custom_font()
print(f"Using font: {font_name}")

# Check if font is actually working
if font_name == "Arcade Classic":
    try:
        # Create a test root to check font
        test_root = tk.Tk()
        test_root.withdraw()
        test_font = font.Font(family="Arcade Classic", size=12)
        actual = test_font.actual()
        test_root.destroy()
        
        if 'arcade' not in actual.get('family', '').lower():
            print("\n" + "="*70)
            print("⚠️  WARNING: Arcade Classic font may not be installed!")
            print("="*70)
            print("To install the font:")
            print("1. Right-click on 'Arcade Classic.ttf' in this folder")
            print("2. Select 'Install' or 'Install for all users'")
            print("3. Restart this application")
            print("="*70 + "\n")
    except:
        pass

# --- Colors / constants ---
COLOR_BG_PANEL = "#000000"
COLOR_PANEL_ACCENT = "#34495e"
COLOR_BTN_TEXT = "white"


# --- Music / SFX helpers ---
music_muted = False

# Theme-specific music files mapping
theme_music = {
    "naruto": "narutomusic.mp3",
    "op": "onepiecemusic.mp3",
    "slam": "slamdunkmusic.mp3",
    "db": "dragonballmusic.mp3",
    "bleach": "bleachmusic.mp3",
}

def play_music(theme="naruto"):
    """Play theme-specific background music"""
    global music_muted
    if music_muted:
        return
    
    music_file = theme_music.get(theme, "narutomusic.mp3")
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

def toggle_mute():
    global music_muted
    music_muted = not music_muted
    if music_muted:
        stop_music()
        mute_btn.configure(text="🔊 Unmute")
    else:
        play_intro()
        mute_btn.configure(text="🔇 Mute")


clap_sound = (
    pygame.mixer.Sound("clapsound.mp3") if os.path.exists("clapsound.mp3") else None
)
lose_sound = (
    pygame.mixer.Sound("losesound.mp3") if os.path.exists("losesound.mp3") else None
)

# --- Window ---
root = tk.Tk()
root.geometry("1920x1090")
root.title("Flip Memory Game")

# After root window is created, verify and install font if needed
try:
    # Check if font file exists and install it
    font_file = "Arcade Classic.ttf"
    if os.path.exists(font_file):
        try:
            import shutil
            fonts_dir = os.path.join(os.environ['WINDIR'], 'Fonts')
            font_dest = os.path.join(fonts_dir, font_file)
            
            # Copy to Windows Fonts if not there
            if not os.path.exists(font_dest):
                try:
                    shutil.copy2(font_file, font_dest)
                    print(f"Installed font to: {font_dest}")
                except PermissionError:
                    print(f"Please install {font_file} manually: Right-click -> Install")
            
            # Try to load font by name to verify it works
            try:
                test_font = font.Font(family="Arcade Classic", size=12)
                actual = test_font.actual()
                actual_family = actual.get('family', 'Unknown')
                if 'arcade' in actual_family.lower() or 'Arcade Classic' in actual_family:
                    print(f"Font verified and working: {actual_family}")
                else:
                    print(f"Font may need manual installation. Current: {actual_family}")
            except Exception as e:
                print(f"Font verification: {e}")
        except Exception as e:
            print(f"Font installation check: {e}")
except Exception as e:
    pass

# --- Frames (screens) ---
home_frame = tk.Frame(root)
themes_frame = tk.Frame(root)
naruto_frame = tk.Frame(root)
onepiece_frame = tk.Frame(root)
slamdunk_frame = tk.Frame(root)
dragonball_frame = tk.Frame(root)
bleach_frame = tk.Frame(root)
game_frame = tk.Frame(root, bg=COLOR_BG_PANEL)
side_panel = tk.Frame(root, bg=COLOR_BG_PANEL)

ALL_FRAMES = [
    home_frame,
    themes_frame,
    naruto_frame,
    onepiece_frame,
    slamdunk_frame,
    dragonball_frame,
    bleach_frame,
    game_frame,
    side_panel,
]

for f in ALL_FRAMES:
    f.place(relwidth=1, relheight=1)
home_frame.lift()
play_intro()


# --- Background helper ---
def set_bg(frame, path):
    if os.path.exists(path):
        try:
            img = PhotoImage(file=path)
            tk.Label(frame, image=img).place(x=0, y=0, relwidth=1, relheight=1)
            frame.bg_img = img
        except Exception:
            pass


# try to set common background images (if available)
set_bg(home_frame, "homep1.PNG")
set_bg(themes_frame, "themes.PNG")
set_bg(naruto_frame, "narutobg.png")
set_bg(onepiece_frame, "onepiecebg.png")
set_bg(slamdunk_frame, "slamD.png")
set_bg(dragonball_frame, "dragonballbg.png")
set_bg(bleach_frame, "bleachbg.png")
set_bg(game_frame, "narutogamebg.png")


# --- Navigation helpers ---
def go_to(frame):
    frame.lift()
    # If we returned to home, ensure intro is playing (unless muted)
    if frame is home_frame:
        try:
            # Only start intro if nothing is currently playing, or current music is not intro
            # We cannot inspect current track reliably; simply restart intro to be safe
            play_intro()
        except Exception:
            pass


current_theme = "naruto"


def exit_app():
    root.destroy()


def go_to_narutogame(size=4):
    global current_theme
    current_theme = "naruto"
    naruto_frame.lower()
    game_frame.lift()
    # Switch from intro to in-game music
    play_music("naruto")
    reset_game(size, theme=current_theme)


def go_to_opgame(size=4):
    global current_theme
    current_theme = "op"
    onepiece_frame.lower()
    game_frame.lift()
    play_music("op")
    reset_game(size, theme=current_theme)


def go_to_slamgame(size=4):
    global current_theme
    current_theme = "slam"
    slamdunk_frame.lower()
    game_frame.lift()
    play_music("slam")
    reset_game(size, theme=current_theme)


def go_to_dbgame(size=4):
    global current_theme
    current_theme = "db"
    dragonball_frame.lower()
    game_frame.lift()
    play_music("db")
    reset_game(size, theme=current_theme)


def go_to_bleachgame(size=4):
    global current_theme
    current_theme = "bleach"
    bleach_frame.lower()
    game_frame.lift()
    play_music("bleach")
    reset_game(size, theme=current_theme)


# --- Game settings & globals ---
card_size = (120, 120)
time_limit = 60  # Will be set dynamically based on grid size
flip_limit = 20  # Will be set dynamically based on grid size
points_per_match = 5  # Will be set dynamically based on grid size

first_card = None
second_card = None
buttons = []
flipped_cards = []
card_images = []
score = 0
flips = 0
time_left = time_limit
timer_running = True
timer_id = None
grid_size = 4
paused = False
consecutive_failed_flips = 0  # Track consecutive failed flips for hint
hint_shown = False  # Track if hint is currently shown
hint_timer = None  # Timer for hint display

# --- Game UI ---
# === GAME FRAME LAYOUT ===
game_frame.grid_rowconfigure(
    1, weight=1
)  # Ang row=1 sa game_frame mu-expand (flexible height)
game_frame.grid_columnconfigure(
    0, weight=1
)  # Ang col=0 sa game_frame mu-expand (flexible width)

# === SCORE PANEL (left side labels) ===
score_panel = tk.Frame(
    game_frame, bg=COLOR_PANEL_ACCENT
)  # Container panel para sa score
score_panel.grid(
    row=0, column=0, padx=20, sticky="w"
)  # Gibutang sa row=0 col=0, left aligned
score_label = tk.Label(
    score_panel, text="Score: 0", font=(font_name, 18, "bold"), fg="white", bg=COLOR_PANEL_ACCENT
)  # Label para score
score_label.pack(side="left", padx=(6, 12))  # Gibutang left sa sulod sa panel

# === FLIPS & TIMER LABELS (top center & right) ===
flips_label = tk.Label(
    game_frame,
    text=f"Flips: 0/{flip_limit}",
    font=(font_name, 18, "bold"),
    fg="white",
    bg=COLOR_PANEL_ACCENT,
)  # Label para flips count
flips_label.grid(row=0, column=1, padx=20)  # Gibutang sa row=0 col=1

timer_label = tk.Label(
    game_frame,
    text="Time: 60s",  # Initial display, will be updated when game starts
    font=(font_name, 18, "bold"),
    fg="white",
    bg=COLOR_PANEL_ACCENT,
)  # Label para countdown timer
timer_label.grid(row=0, column=2, padx=20)  # Gibutang sa row=0 col=2

# === PAUSE MENU BOX ===
pause_menu_box = tk.Frame(game_frame, bg="black", bd=4, relief="ridge")
pause_menu_box.place(relx=0.5, rely=0.5, anchor="center", width=450, height=350)
pause_menu_box.lower()

pause_menu_title = tk.Label(
    pause_menu_box,
    text="Game Paused",
    font=(font_name, 32, "bold"),
    fg="#FF6B6B",
    bg="black",
)
pause_menu_title.pack(pady=(30, 20))

pause_menu_buttons = tk.Frame(pause_menu_box, bg="black")
pause_menu_buttons.pack(pady=20)

def on_menu_resume():
    """Resume the game from menu"""
    global paused, timer_running, current_theme
    paused = False
    timer_running = True
    pause_menu_box.lower()
    play_music(current_theme)
    update_timer()

def on_menu_reset():
    """Reset game from menu"""
    pause_menu_box.lower()
    reset_game(grid_size, theme=current_theme)

def on_menu_back():
    """Go back to themes from menu"""
    pause_menu_box.lower()
    back_to_themes()

menu_resume_btn = ctk.CTkButton(
    pause_menu_buttons,
    text="Resume",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="black",
    hover_color="#FF5252",
    text_color="white",
    width=180,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=on_menu_resume,
)
menu_resume_btn.pack(pady=10)

menu_reset_btn = ctk.CTkButton(
    pause_menu_buttons,
    text="Reset",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="black",
    hover_color="#FF5252",
    text_color="white",
    width=180,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=on_menu_reset,
)
menu_reset_btn.pack(pady=10)

menu_back_btn = ctk.CTkButton(
    pause_menu_buttons,
    text="Back",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="black",
    hover_color="#FF5252",
    text_color="white",
    width=180,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=on_menu_back,
)
menu_back_btn.pack(pady=10)

# === SIDE PANEL REMOVED - buttons now positioned directly on game frame ===

# === BUTTON CONFIGURATION (shared style) ===
btn_cfg = {
    "font": (font_name, 14, "bold"),
    "fg": COLOR_BTN_TEXT,
    "width": 12,
    "height": 2,
    "cursor": "hand2",
    "bd": 0,
    "relief": "flat",
}


# === MENU ICON HANDLER ===
def on_menu_click():
    """Open pause menu and pause the game"""
    global paused, timer_running
    if not paused:  # Only pause if not already paused
        paused = True
        timer_running = False
        stop_music()
        pause_menu_box.lift()


# === BACK TO THEMES HANDLER ===
def back_to_themes():
    """Return to theme menu, reset states"""
    global timer_running, paused, time_left
    timer_running = False
    paused = False
    cancel_timer()  # Stop timer
    time_left = time_limit
    stop_music()  # Stop bg music
    if clap_sound:
        clap_sound.stop()  # Stop clap if playing
    if lose_sound:
        lose_sound.stop()  # Stop lose if playing
    result_label.config(text="")  # Clear result text
    result_label.lower()  # Hide result text
    win_overlay.lower()  # Hide win overlay
    flip_overlay.lower()  # Hide flip overlay
    time_overlay.lower()  # Hide time overlay
    pause_menu_box.lower()  # Hide pause menu
    game_frame.lower()  # Hide game frame
    themes_frame.lift()  # Show themes menu


# === MENU ICON BUTTON ===
# Menu icon button - top left corner
menu_icon_btn = ctk.CTkButton(
    game_frame,
    text="☰",
    fg_color="#FF6B6B",
    bg_color="transparent",
    hover_color="#FF5252",
    text_color="white",
    font=(font_name, 32, "bold"),
    width=60,
    height=60,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=on_menu_click,
)
pywinstyles.set_opacity(menu_icon_btn, color=COLOR_BG_PANEL)
menu_icon_btn.place(relx=0.9, rely=0.05, anchor="nw")  # Top left corner

# === BOARD FRAME (main card grid area) ===
board_frame = tk.Frame(game_frame, bg=COLOR_BG_PANEL)  # Board container for cards
board_frame.place(relx=0.5, rely=0.45, anchor="center")  # Positioned center
pywinstyles.set_opacity(board_frame, color=COLOR_BG_PANEL)

# === RESULT LABEL (for overlay messages like win/lose) ===
result_label = tk.Label(
    game_frame, text="", font=(font_name, 40, "bold"), fg="yellow", bg="black"
)  # Big text for result
result_label.place(relx=0.5, rely=0.5, anchor="center")  # Center screen
result_label.lower()  # Hide by default


# --- WIN OVERLAY BOX ---
win_overlay = tk.Frame(game_frame, bg="black", bd=4, relief="ridge")
win_overlay.place(relx=0.5, rely=0.5, anchor="center", width=400, height=250)
win_overlay.lower()

win_msg = tk.Label(
    win_overlay, text="You Win!", font=(font_name, 28, "bold"), fg="lime", bg="black"
)
win_msg.pack(pady=(15, 5))
win_stats = tk.Label(win_overlay, text="", font=(font_name, 16, "bold"), fg="white", bg="black")
win_stats.pack(pady=10)


def on_win_reset():
    win_overlay.lower()
    reset_game(grid_size, theme=current_theme)


def on_win_back():
    win_overlay.lower()
    back_to_themes()


def on_time_reset():
    time_overlay.lower()
    reset_game(grid_size, theme=current_theme)


def on_time_back():
    time_overlay.lower()
    back_to_themes()


def on_flip_reset():
    flip_overlay.lower()
    reset_game(grid_size, theme=current_theme)


def on_flip_back():
    flip_overlay.lower()
    back_to_themes()


win_btns = tk.Frame(win_overlay, bg="black")
win_btns.pack(side="bottom", pady=15)

win_reset_btn = ctk.CTkButton(
    win_btns,
    text="Reset",
    font=(font_name, 14, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    hover_color="#FF5252",
    text_color="white",
    width=100,
    corner_radius=12,
    border_width=2,
    border_color="#FFFFFF",
    command=on_win_reset,
)
pywinstyles.set_opacity(win_reset_btn, color="#000001")
win_reset_btn.pack(side="left", padx=10)

win_back_btn = ctk.CTkButton(
    win_btns,
    text="Back",
    font=(font_name, 14, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    hover_color="#FF5252",
    text_color="white",
    width=100,
    corner_radius=12,
    border_width=2,
    border_color="#FFFFFF",
    command=on_win_back,
)
pywinstyles.set_opacity(win_back_btn, color="#000001")
win_back_btn.pack(side="right", padx=10)

# --- FLIP OVERLAY BOX ---
flip_overlay = tk.Frame(game_frame, bg="black", bd=4, relief="ridge")
flip_overlay.place(relx=0.5, rely=0.5, anchor="center", width=400, height=250)
flip_overlay.lower()

flip_msg = tk.Label(
    flip_overlay,
    text="Flip Limit Reached!",
    font=(font_name, 24, "bold"),
    fg="red",
    bg="black",
)
flip_msg.pack(pady=(15, 5))
flip_stats = tk.Label(flip_overlay, text="", font=(font_name, 16, "bold"), fg="white", bg="black")
flip_stats.pack(pady=10)

flip_reset_btn = ctk.CTkButton(
    flip_overlay,
    text="⟳ Reset",
    font=(font_name, 14, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    hover_color="#FF5252",
    text_color="white",
    width=100,
    corner_radius=12,
    border_width=2,
    border_color="#FFFFFF",
    command=on_flip_reset,
)
pywinstyles.set_opacity(flip_reset_btn, color="#000001")
flip_reset_btn.pack(side="left", padx=10)

flip_back_btn = ctk.CTkButton(
    flip_overlay,
    text="Back",
    font=(font_name, 14, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    hover_color="#FF5252",
    text_color="white",
    width=100,
    corner_radius=12,
    border_width=2,
    border_color="#FFFFFF",
    command=on_flip_back,
)
pywinstyles.set_opacity(flip_back_btn, color="#000001")
flip_back_btn.pack(side="right", padx=10)

# --- TIME OVERLAY BOX ---
time_overlay = tk.Frame(game_frame, bg="black", bd=4, relief="ridge")
time_overlay.place(relx=0.5, rely=0.5, anchor="center", width=400, height=250)
time_overlay.lower()

time_msg = tk.Label(
    time_overlay, text="Time's Up!", font=(font_name, 24, "bold"), fg="red", bg="black"
)
time_msg.pack(pady=(15, 5))
time_stats = tk.Label(time_overlay, text="", font=(font_name, 16, "bold"), fg="white", bg="black")
time_stats.pack(pady=10)

time_reset_btn = ctk.CTkButton(
    time_overlay,
    text="⟳ Reset",
    font=(font_name, 14, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    hover_color="#FF5252",
    text_color="white",
    width=100,
    corner_radius=12,
    border_width=2,
    border_color="#FFFFFF",
    command=on_time_reset,
)
pywinstyles.set_opacity(time_reset_btn, color="#000001")
time_reset_btn.pack(side="left", padx=10)

time_back_btn = ctk.CTkButton(
    time_overlay,
    text="Back",
    font=(font_name, 14, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    hover_color="#FF5252",
    text_color="white",
    width=100,
    corner_radius=12,
    border_width=2,
    border_color="#FFFFFF",
    command=on_time_back,
)
pywinstyles.set_opacity(time_back_btn, color="#000001")
time_back_btn.pack(side="right", padx=10)

# --- Card back/cover image ---
def load_back_image(size=(120, 120)):
    """Load card back image, or create gray placeholder if not found"""
    if os.path.exists("narutocover.jpeg"):
        try:
            img = Image.open("narutocover.jpeg").resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            pass
    # Fallback to gray placeholder if image not found
    return ImageTk.PhotoImage(Image.new("RGB", size, color="gray"))

back_image = load_back_image()

# --- Theme image paths ---
naruto_paths_4x4 = [f"naruto{i}.png" for i in range(1, 9)]
naruto_paths_6x6 = [f"naruto{i}.png" for i in range(1, 19)]
naruto_paths_8x8 = [f"naruto{i}.png" for i in range(1, 33)]
op_paths_4x4 = [f"op{i}.png" for i in range(1, 9)]
op_paths_6x6 = [f"op{i}.png" for i in range(1, 19)]
op_paths_8x8 = [f"op{i}.png" for i in range(1, 33)]
slam_paths_4x4 = [f"slam{i}.png" for i in range(1, 9)]
slam_paths_6x6 = [f"slam{i}.png" for i in range(1, 19)]
slam_paths_8x8 = [f"slam{i}.png" for i in range(1, 33)]
db_paths_4x4 = [f"db{i}.png" for i in range(1, 9)]
db_paths_6x6 = [f"db{i}.png" for i in range(1, 19)]
db_paths_8x8 = [f"db{i}.png" for i in range(1, 33)]
bleach_paths_4x4 = [f"bleach{i}.png" for i in range(1, 9)]
bleach_paths_6x6 = [f"bleach{i}.png" for i in range(1, 19)]
bleach_paths_8x8 = [f"bleach{i}.png" for i in range(1, 33)]

theme_images = {
    "naruto": {4: naruto_paths_4x4, 6: naruto_paths_6x6, 8: naruto_paths_8x8},
    "op": {4: op_paths_4x4, 6: op_paths_6x6, 8: op_paths_8x8},
    "slam": {4: slam_paths_4x4, 6: slam_paths_6x6, 8: slam_paths_8x8},
    "db": {4: db_paths_4x4, 6: db_paths_6x6, 8: db_paths_8x8},
    "bleach": {4: bleach_paths_4x4, 6: bleach_paths_6x6, 8: bleach_paths_8x8},
}


# --- Load images safely ---
def load_theme_images(paths, needed, size):
    imgs = []
    for p in paths:
        if os.path.exists(p):
            try:
                img = Image.open(p).resize(size)
                imgs.append(ImageTk.PhotoImage(img))
            except Exception:
                pass
    while len(imgs) < needed:
        k = len(imgs)
        r, g, b = (k * 73) % 256, (k * 37) % 256, (k * 151) % 256
        img = Image.new("RGB", size, (r, g, b))
        imgs.append(ImageTk.PhotoImage(img))
    return imgs[:needed]


# --- Timer / mechanics ---
def update_timer():
    global time_left, timer_id, timer_running
    if timer_running and not paused:
        time_left -= 1
        # Format time display: show minutes and seconds for times >= 60 seconds
        if time_left >= 60:
            minutes = time_left // 60
            seconds = time_left % 60
            if seconds > 0:
                timer_label.config(text=f"Time: {minutes}m {seconds}s")
            else:
                timer_label.config(text=f"Time: {minutes}m")
        else:
            timer_label.config(text=f"Time: {time_left}s")
        if time_left <= 0:
            game_over("Time's up! You lose.")
        else:
            timer_id = root.after(1000, update_timer)


def cancel_timer():
    global timer_id
    if timer_id:
        try:
            root.after_cancel(timer_id)
        except Exception:
            pass
        timer_id = None


def cancel_hint_timer():
    global hint_timer
    if hint_timer:
        try:
            root.after_cancel(hint_timer)
        except Exception:
            pass
        hint_timer = None


def show_hint():
    """Show hint by making matching cards glow"""
    global hint_shown, hint_timer
    
    if hint_shown:
        return
    
    hint_shown = True
    
    # Find pairs that haven't been matched yet
    unmatched_pairs = []
    for i in range(len(card_images)):
        if i not in flipped_cards:
            for j in range(i + 1, len(card_images)):
                if j not in flipped_cards and card_images[i] == card_images[j]:
                    unmatched_pairs.append((i, j))
                    break
    
    if unmatched_pairs:
        # Show the first unmatched pair
        card1_idx, card2_idx = unmatched_pairs[0]
        
        # Create glowing effect by temporarily showing the cards
        buttons[card1_idx].config(image=card_images[card1_idx])
        buttons[card2_idx].config(image=card_images[card2_idx])
        
        # Schedule hiding the hint after a very quick flash (150ms - speed of light!)
        hint_timer = root.after(150, hide_hint)


def hide_hint():
    """Hide the hint by covering the cards again"""
    global hint_shown, hint_timer
    
    if not hint_shown:
        return
    
    hint_shown = False
    hint_timer = None
    
    # Cover all cards that aren't permanently flipped
    for i, btn in enumerate(buttons):
        if i not in flipped_cards:
            btn.config(image=back_image)


def on_card_click(idx):
    global first_card, second_card, flips
    if paused or not timer_running:
        return
    if idx in flipped_cards or idx == first_card:
        return

    buttons[idx].config(image=card_images[idx])
    buttons[idx].image = card_images[idx]

    if first_card is None:
        first_card = idx
    elif second_card is None:
        second_card = idx
        root.update()
        time.sleep(0.35)
        check_match()

    if flips >= flip_limit and len(flipped_cards) != len(card_images):
        game_over("Flip limit reached! You lose.")


def check_match():
    global first_card, second_card, score, flips, consecutive_failed_flips, points_per_match
    if card_images[first_card] == card_images[second_card]:
        flipped_cards.extend([first_card, second_card])
        score += points_per_match
        score_label.config(text=f"Score: {score}")
        consecutive_failed_flips = 0  # Reset failed flips counter on successful match
    else:
        flips += 1
        consecutive_failed_flips += 1  # Increment failed flips counter
        flips_label.config(text=f"Flips: {flips}/{flip_limit}")
        buttons[first_card].config(image=back_image)
        buttons[second_card].config(image=back_image)
        
        # Show hint after 5 consecutive failed flips
        if consecutive_failed_flips >= 5:
            root.after(500, show_hint)  # Show hint after a short delay
    
    first_card = None
    second_card = None
    if len(flipped_cards) == len(card_images):
        game_over("You win!")


def game_over(message):
    global timer_running
    timer_running = False
    cancel_timer()
    for b in buttons:
        b.config(state="disabled")
    stop_music()
    if "win" in message.lower():
        if clap_sound:
            clap_sound.play()
        win_stats.config(
            text=f"Score: {score}\nFlips: {flips}\nTime Left: {time_left}s"
        )
        win_overlay.lift()
    elif "flip" in message.lower():
        if lose_sound:
            lose_sound.play()
        flip_stats.config(
            text=f"Score: {score}\nFlips: {flips}/{flip_limit}\nTime Left: {time_left}s"
        )
        flip_overlay.lift()
    elif "time" in message.lower():
        if lose_sound:
            lose_sound.play()
        time_stats.config(text=f"Score: {score}\nFlips: {flips}\nTime Left: 0s")
        time_overlay.lift()
    else:
        if lose_sound:
            lose_sound.play()
        result_label.config(text=message, fg="red")
        result_label.lift()


def reset_game(size=4, theme="naruto"):
    global card_images, first_card, second_card, flipped_cards
    global score, flips, time_left, timer_running, buttons, grid_size, back_image, paused
    global consecutive_failed_flips, hint_shown, hint_timer
    global time_limit, flip_limit, points_per_match

    cancel_timer()
    cancel_hint_timer()
    if clap_sound:
        clap_sound.stop()
    if lose_sound:
        lose_sound.stop()
    play_music(theme)

    grid_size = size
    
    # Set game settings based on grid size
    if size == 4:
        time_limit = 60  # 1 minute
        flip_limit = 20
        points_per_match = 5
    elif size == 6:
        time_limit = 90  # 1 minute 30 seconds
        flip_limit = 40
        points_per_match = 10
    elif size == 8:
        time_limit = 120  # 2 minutes
        flip_limit = 50
        points_per_match = 15
    
    px = (120, 120) if size == 4 else (80, 80) if size == 6 else (60, 60)
    needed = 8 if size == 4 else 18 if size == 6 else 32

    # Load card back image with proper size
    back_image = load_back_image(px)

    for w in board_frame.winfo_children():
        w.destroy()
    buttons.clear()

    paths = theme_images.get(theme, {}).get(size, [])
    imgs = load_theme_images(paths, needed, px)
    card_images = imgs * 2
    random.shuffle(card_images)

    for i in range(size):
        for j in range(size):
            idx = i * size + j
            btn = tk.Button(
                board_frame,
                image=back_image,
                bd=0,
                command=lambda i=idx: on_card_click(i),
            )
            btn.grid(row=i, column=j, padx=6, pady=6)
            buttons.append(btn)

    first_card = None
    second_card = None
    flipped_cards.clear()
    score = 0
    flips = 0
    time_left = time_limit
    timer_running = True
    paused = False
    consecutive_failed_flips = 0  # Reset hint counter
    hint_shown = False  # Reset hint state

    score_label.config(text="Score: 0")
    flips_label.config(text=f"Flips: 0/{flip_limit}")
    # Format time display: show minutes and seconds for times >= 60 seconds
    if time_limit >= 60:
        minutes = time_limit // 60
        seconds = time_limit % 60
        if seconds > 0:
            timer_label.config(text=f"Time: {minutes}m {seconds}s")
        else:
            timer_label.config(text=f"Time: {minutes}m")
    else:
        timer_label.config(text=f"Time: {time_limit}s")
    result_label.config(text="")
    result_label.lower()
    win_overlay.lower()
    pause_menu_box.lower()
    update_timer()


# --- Hover helpers ---
def hover(btn, color):
    try:
        btn["bg"] = color
    except:
        pass


def nothover(btn):
    try:
        btn["bg"] = "gold"
    except:
        pass


# --- Home / Themes UI ---
start_btn = ctk.CTkButton(
    home_frame,
    text="START",
    font=(font_name, 24, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=200,
    height=50,
    corner_radius=20,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to(themes_frame),
)
pywinstyles.set_opacity(start_btn, color="#000001")
start_btn.place(relx=0.5, y=400, anchor="center")

howto_btn = ctk.CTkButton(
    home_frame,
    text="HOW TO PLAY",
    font=(font_name, 24, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=200,
    height=50,
    corner_radius=20,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to(howto_frame),
)
pywinstyles.set_opacity(howto_btn, color="#000001")
howto_btn.place(relx=0.5, y=490, anchor="center")

exit_btn = ctk.CTkButton(
    home_frame,
    text="EXIT",
    font=(font_name, 24, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=200,
    height=50,
    corner_radius=20,
    border_width=2,
    border_color="#FFFFFF",
    command=exit_app,
)
pywinstyles.set_opacity(exit_btn, color="#000001")
exit_btn.place(relx=0.5, y=580, anchor="center")

# Mute/Unmute button
mute_btn = ctk.CTkButton(
    home_frame,
    text="Mute",
    font=(font_name, 24, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=200,
    height=50,
    corner_radius=20,
    border_width=2,
    border_color="#FFFFFF",
    command=toggle_mute,
)
pywinstyles.set_opacity(mute_btn, color="#000001")
mute_btn.place(relx=0.5, y=680, anchor="center")


def make_theme_btn(parent, text, y, cmd):
    b = ctk.CTkButton(
        parent,
        text=text,
        font=(font_name, 19, "bold"),
        fg_color="#FF6B6B",
        bg_color="#000001",
        text_color="White",
        hover_color="#FF5252",
        width=13 * 10,
        height=3 * 20,
        corner_radius=18,
        border_width=2,
        border_color="#FFFFFF",
        command=cmd,
    )
    pywinstyles.set_opacity(b, color="#000001")
    b.place(y=y, anchor="center")
    return b


naruto_theme_btn = make_theme_btn(
    themes_frame, "Naruto", 180, lambda: go_to_naruto_with_auto_transitions()
)
naruto_theme_btn.place(x=130, y=490)
onepiece_theme_btn = make_theme_btn(
    themes_frame, "One Piece", 260, lambda: go_to(onepiece_frame)
)
onepiece_theme_btn.place(x=1000, y=490)
slamdunk_theme_btn = make_theme_btn(
    themes_frame, "Slam Dunk", 340, lambda: go_to(slamdunk_frame)
)
slamdunk_theme_btn.place(x=420, y=490)
db_theme_btn = make_theme_btn(
    themes_frame, "Dragon Ball", 420, lambda: go_to(dragonball_frame)
)
db_theme_btn.place(x=1275, y=490)
bleach_theme_btn = make_theme_btn(
    themes_frame, "Bleach", 500, lambda: go_to(bleach_frame)
)
bleach_theme_btn.place(x=700, y=490)

# --- HOW TO PLAY FRAME ---
howto_frame = tk.Frame(root, bg="#0d1117")  # GitHub dark background
set_bg(howto_frame, "howtoplaybg.png")  # optional anime-themed background
howto_frame.place(relwidth=1, relheight=1)
home_frame.lift()  # ensure home screen shows first

# --- MAIN CONTAINER ---
main_container = tk.Frame(howto_frame, bg="#161b22", relief="ridge", bd=4)
main_container.place(relx=0.5, rely=0.5, anchor="center", width=850, height=750)

# --- STYLED TITLE ---
title_label = tk.Label(
    main_container,
    text="HOW TO PLAY",
    font=(font_name, 32, "bold"),
    fg="#58a6ff",  # GitHub blue
    bg="#161b22",
)
title_label.pack(pady=(30, 25))

# --- INSTRUCTION SECTIONS ---
# Create a scrollable frame for instructions
instruction_frame = tk.Frame(main_container, bg="#161b22")
instruction_frame.pack(fill="both", expand=True, padx=35, pady=15)

# Theme Selection
theme_section = tk.Frame(instruction_frame, bg="#21262d", relief="raised", bd=2)
theme_section.pack(fill="x", pady=8)

theme_title = tk.Label(
    theme_section,
    text="🎮 Choose a Theme",
    font=(font_name, 18, "bold"),
    fg="#f85149",  # GitHub red
    bg="#21262d",
)
theme_title.pack(anchor="w", padx=20, pady=(15, 8))

theme_text = tk.Label(
    theme_section,
    text="Pick your favorite anime world — Naruto, One Piece, Slam Dunk, Dragon Ball, or Bleach.",
    font=(font_name, 13, "bold"),
    fg="#f0f6fc",  # GitHub light text
    bg="#21262d",
    wraplength=750,
    justify="left",
)
theme_text.pack(anchor="w", padx=20, pady=(0, 15))

# Difficulty Selection
diff_section = tk.Frame(instruction_frame, bg="#21262d", relief="raised", bd=2)
diff_section.pack(fill="x", pady=8)

diff_title = tk.Label(
    diff_section,
    text="⚡ Select a Difficulty",
    font=(font_name, 18, "bold"),
    fg="#a5d6ff",  # GitHub light blue
    bg="#21262d",
)
diff_title.pack(anchor="w", padx=20, pady=(15, 8))

diff_text = tk.Label(
    diff_section,
    text="Choose your board size:\n4x4 → Easy (8 pairs)\n6x6 → Medium (18 pairs)\n8x8 → Hard (32 pairs)",
    font=(font_name, 13, "bold"),
    fg="#f0f6fc",
    bg="#21262d",
    justify="left",
)
diff_text.pack(anchor="w", padx=20, pady=(0, 15))

# Gameplay
gameplay_section = tk.Frame(instruction_frame, bg="#21262d", relief="raised", bd=2)
gameplay_section.pack(fill="x", pady=8)

gameplay_title = tk.Label(
    gameplay_section,
    text="🎯 Start the Game",
    font=(font_name, 18, "bold"),
    fg="#ffa657",  # GitHub orange
    bg="#21262d",
)
gameplay_title.pack(anchor="w", padx=20, pady=(15, 8))

gameplay_text = tk.Label(
    gameplay_section,
    text="Flip two cards to reveal their pictures.\nMatch all pairs before time runs out!",
    font=(font_name, 13, "bold"),
    fg="#f0f6fc",
    bg="#21262d",
    justify="left",
)
gameplay_text.pack(anchor="w", padx=20, pady=(0, 15))

# Scoring
scoring_section = tk.Frame(instruction_frame, bg="#21262d", relief="raised", bd=2)
scoring_section.pack(fill="x", pady=8)

scoring_title = tk.Label(
    scoring_section,
    text="🏆 Scoring",
    font=(font_name, 18, "bold"),
    fg="#d2a8ff",  # GitHub purple
    bg="#21262d",
)
scoring_title.pack(anchor="w", padx=20, pady=(15, 8))

scoring_text = tk.Label(
    scoring_section,
    text="+5 points for every correct match.\nLimited flips — don't waste your turns!\nYou win when all pairs are matched!",
    font=(font_name, 13, "bold"),
    fg="#f0f6fc",
    bg="#21262d",
    justify="left",
)
scoring_text.pack(anchor="w", padx=20, pady=(0, 15))

# Controls
controls_section = tk.Frame(instruction_frame, bg="#21262d", relief="raised", bd=2)
controls_section.pack(fill="x", pady=8)

controls_title = tk.Label(
    controls_section,
    text="🎮 Controls",
    font=(font_name, 18, "bold"),
    fg="#79c0ff",  # GitHub blue
    bg="#21262d",
)
controls_title.pack(anchor="w", padx=20, pady=(15, 8))

controls_text = tk.Label(
    controls_section,
    text="Pause / Resume – Stop or continue the game.\nReset – Restart the current game.\nBack – Return to the theme menu.",
    font=(font_name, 13, "bold"),
    fg="#f0f6fc",
    bg="#21262d",
    justify="left",
)
controls_text.pack(anchor="w", padx=20, pady=(0, 15))

# Game Over
gameover_section = tk.Frame(instruction_frame, bg="#21262d", relief="raised", bd=2)
gameover_section.pack(fill="x", pady=8)

gameover_title = tk.Label(
    gameover_section,
    text="⚠️ Game Over Conditions",
    font=(font_name, 18, "bold"),
    fg="#ff7b72",  # GitHub red
    bg="#21262d",
)
gameover_title.pack(anchor="w", padx=20, pady=(15, 8))

gameover_text = tk.Label(
    gameover_section,
    text="Time's up!\nFlip limit reached!\nAll pairs matched = You Win!",
    font=(font_name, 13, "bold"),
    fg="#f0f6fc",
    bg="#21262d",
    justify="left",
)
gameover_text.pack(anchor="w", padx=20, pady=(0, 15))

# --- BACK BUTTON (top left corner) ---
howto_back_btn = ctk.CTkButton(
    howto_frame,
    text="Back",
    font=(font_name, 16, "bold"),
    fg_color="#FF6B6B",
    bg_color="#0d1117",
    text_color="white",
    hover_color="#FF5252",
    width=120,
    height=45,
    corner_radius=20,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to(home_frame),
)
pywinstyles.set_opacity(howto_back_btn, color="#0d1117")
howto_back_btn.place(x=20, y=20)


# --- UPDATE YOUR HOW TO PLAY BUTTON to go here ---
# Find this button in home_frame section and replace its command with this:
# command=lambda: go_to(howto_frame)


# --- Choose-tile UI for each theme (styled tiles + centered back) ---
def make_tile_btn(parent, text, x, y, cmd, bg, abg):
    btn = ctk.CTkButton(
        parent,
        text=text,
        font=(font_name, 18, "bold"),
        fg_color=bg,
        bg_color="#000001",
        text_color="white",
        hover_color=abg,
        width=100,
        height=50,
        corner_radius=15,
        border_width=2,
        border_color="#FFFFFF",
        command=cmd,
    )
    pywinstyles.set_opacity(btn, color="#000001")
    btn.place(x=x, y=y)
    return btn


def make_back_btn(parent, text, cmd, bg, abg):
    btn = ctk.CTkButton(
        parent,
        text=text,
        font=(font_name, 18, "bold"),
        fg_color=bg,
        bg_color="#000001",
        text_color="white",
        hover_color=abg,
        width=140,
        height=50,
        corner_radius=15,
        border_width=2,
        border_color="#FFFFFF",
        command=cmd,
    )
    pywinstyles.set_opacity(btn, color="#000001")
    btn.place(relx=0.5, rely=0.85, anchor="center")
    return btn


# Add GIF frame to the right side of naruto_frame (landscape orientation)
naruto_gif_frame = tk.Frame(naruto_frame, bg="#1A1A2E", relief="raised", bd=3)
naruto_gif_frame.place(x=400, y=200, width=800, height=400)

# Naruto choose tiles - arranged on left side with hover effects
# Create 4x4 button with hover effect
naruto_4x4_btn = ctk.CTkButton(
    naruto_frame,
    text="4x4",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_narutogame(4),
)
pywinstyles.set_opacity(naruto_4x4_btn, color="#000001")
naruto_4x4_btn.place(x=150, y=300)

# Add hover effects to 4x4 button
def on_4x4_enter(event):
    stop_auto_transitions()
    load_4x4_gif()

def on_4x4_leave(event):
    clear_gif()
    start_auto_transitions()

naruto_4x4_btn.bind("<Enter>", on_4x4_enter)
naruto_4x4_btn.bind("<Leave>", on_4x4_leave)
# Create 6x6 button with hover effect
naruto_6x6_btn = ctk.CTkButton(
    naruto_frame,
    text="6x6",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_narutogame(6),
)
pywinstyles.set_opacity(naruto_6x6_btn, color="#000001")
naruto_6x6_btn.place(x=150, y=400)

# Add hover effects to 6x6 button
def on_6x6_enter(event):
    stop_auto_transitions()
    load_6x6_gif()

def on_6x6_leave(event):
    clear_gif()
    start_auto_transitions()

naruto_6x6_btn.bind("<Enter>", on_6x6_enter)
naruto_6x6_btn.bind("<Leave>", on_6x6_leave)
# Create 8x8 button with hover effect
naruto_8x8_btn = ctk.CTkButton(
    naruto_frame,
    text="8x8",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_narutogame(8),
)
pywinstyles.set_opacity(naruto_8x8_btn, color="#000001")
naruto_8x8_btn.place(x=150, y=500)

# Add hover effects to 8x8 button
def on_8x8_enter(event):
    stop_auto_transitions()
    load_8x8_gif()

def on_8x8_leave(event):
    clear_gif()
    start_auto_transitions()

naruto_8x8_btn.bind("<Enter>", on_8x8_enter)
naruto_8x8_btn.bind("<Leave>", on_8x8_leave)
make_back_btn(naruto_frame, "Back", lambda: go_to(themes_frame), "#FF6B6B", "#FF5252")

# GIF frame with hover effects and smooth transitions
naruto_gif_images = []
naruto_gif_labels = []
current_gif_label = None
auto_transition_running = False
current_auto_gif = 0
transition_timer = None

def load_4x4_gif():
    global current_gif_label
    if os.path.exists("GIF-4x4.png"):
        try:
            # Clear previous GIF
            if current_gif_label:
                current_gif_label.destroy()
            
            # Load and resize image to fit frame without zooming
            from PIL import Image, ImageTk
            pil_img = Image.open("GIF-4x4.png")
            
            # Calculate scaling to fit within frame with padding to prevent overlap
            frame_width, frame_height = 760, 360  # Reduced size to prevent overlap
            img_width, img_height = pil_img.size
            
            # Calculate scale factor to fit image within frame with margin
            scale_w = frame_width / img_width
            scale_h = frame_height / img_height
            scale = min(scale_w, scale_h)  # Use smaller scale to fit entirely
            
            # Resize image maintaining aspect ratio
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            img = ImageTk.PhotoImage(pil_img)
            current_gif_label = tk.Label(naruto_gif_frame, image=img, bg="#1A1A2E")
            # Center the resized image in the frame
            current_gif_label.place(relx=0.5, rely=0.5, anchor="center")
            current_gif_label.image = img  # Keep reference
        except Exception:
            pass

def load_6x6_gif():
    global current_gif_label
    if os.path.exists("GIF-6x6.png"):
        try:
            # Clear previous GIF
            if current_gif_label:
                current_gif_label.destroy()
            
            # Load and resize image to fit frame without zooming
            from PIL import Image, ImageTk
            pil_img = Image.open("GIF-6x6.png")
            
            # Calculate scaling to fit within frame with padding to prevent overlap
            frame_width, frame_height = 760, 360  # Reduced size to prevent overlap
            img_width, img_height = pil_img.size
            
            # Calculate scale factor to fit image within frame with margin
            scale_w = frame_width / img_width
            scale_h = frame_height / img_height
            scale = min(scale_w, scale_h)  # Use smaller scale to fit entirely
            
            # Resize image maintaining aspect ratio
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            img = ImageTk.PhotoImage(pil_img)
            current_gif_label = tk.Label(naruto_gif_frame, image=img, bg="#1A1A2E")
            # Center the resized image in the frame
            current_gif_label.place(relx=0.5, rely=0.5, anchor="center")
            current_gif_label.image = img  # Keep reference
        except Exception:
            pass

def load_8x8_gif():
    global current_gif_label
    if os.path.exists("GIF-8x8.png"):
        try:
            # Clear previous GIF
            if current_gif_label:
                current_gif_label.destroy()
            
            # Load and resize image to fit frame without zooming
            from PIL import Image, ImageTk
            pil_img = Image.open("GIF-8x8.png")
            
            # Calculate scaling to fit within frame with padding to prevent overlap
            frame_width, frame_height = 760, 360  # Reduced size to prevent overlap
            img_width, img_height = pil_img.size
            
            # Calculate scale factor to fit image within frame with margin
            scale_w = frame_width / img_width
            scale_h = frame_height / img_height
            scale = min(scale_w, scale_h)  # Use smaller scale to fit entirely
            
            # Resize image maintaining aspect ratio
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            img = ImageTk.PhotoImage(pil_img)
            current_gif_label = tk.Label(naruto_gif_frame, image=img, bg="#1A1A2E")
            # Center the resized image in the frame
            current_gif_label.place(relx=0.5, rely=0.5, anchor="center")
            current_gif_label.image = img  # Keep reference
        except Exception:
            pass

def clear_gif():
    global current_gif_label
    if current_gif_label:
        current_gif_label.destroy()
        current_gif_label = None

def start_auto_transitions():
    global auto_transition_running, current_auto_gif, transition_timer
    auto_transition_running = True
    current_auto_gif = 0
    cycle_auto_gifs()

def stop_auto_transitions():
    global auto_transition_running, transition_timer
    auto_transition_running = False
    if transition_timer:
        root.after_cancel(transition_timer)
        transition_timer = None

def cycle_auto_gifs():
    global current_auto_gif, auto_transition_running, transition_timer
    if not auto_transition_running:
        return
    
    # Load current auto GIF
    gif_files = ["GIF-4x4.png", "GIF-6x6.png", "GIF-8x8.png"]
    if current_auto_gif < len(gif_files):
        load_auto_gif(gif_files[current_auto_gif])
        current_auto_gif = (current_auto_gif + 1) % len(gif_files)
    
    # Schedule next transition
    transition_timer = root.after(3000, cycle_auto_gifs)  # 3 second intervals

def load_auto_gif(gif_file):
    global current_gif_label
    if os.path.exists(gif_file):
        try:
            # Clear previous GIF
            if current_gif_label:
                current_gif_label.destroy()
            
            # Load and resize image to fit frame without zooming
            from PIL import Image, ImageTk
            pil_img = Image.open(gif_file)
            
            # Calculate scaling to fit within frame with padding to prevent overlap
            frame_width, frame_height = 760, 360  # Reduced size to prevent overlap
            img_width, img_height = pil_img.size
            
            # Calculate scale factor to fit image within frame with margin
            scale_w = frame_width / img_width
            scale_h = frame_height / img_height
            scale = min(scale_w, scale_h)  # Use smaller scale to fit entirely
            
            # Resize image maintaining aspect ratio
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            img = ImageTk.PhotoImage(pil_img)
            current_gif_label = tk.Label(naruto_gif_frame, image=img, bg="#1A1A2E")
            # Center the resized image in the frame
            current_gif_label.place(relx=0.5, rely=0.5, anchor="center")
            current_gif_label.image = img  # Keep reference
        except Exception:
            pass

# Generic loader to display a GIF/image into a specific frame
def load_gif_into(target_frame, gif_file):
    global current_gif_label
    if os.path.exists(gif_file):
        try:
            if current_gif_label:
                current_gif_label.destroy()
            from PIL import Image, ImageTk
            pil_img = Image.open(gif_file)
            frame_width, frame_height = 760, 360
            img_width, img_height = pil_img.size
            scale_w = frame_width / img_width
            scale_h = frame_height / img_height
            scale = min(scale_w, scale_h)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(pil_img)
            current_gif_label = tk.Label(target_frame, image=img, bg="#1A1A2E")
            current_gif_label.place(relx=0.5, rely=0.5, anchor="center")
            current_gif_label.image = img
        except Exception:
            pass

# One Piece hover loaders
def load_op_4x4_gif():
    load_gif_into(onepiece_gif_frame, "GIF-4x4.png")

def load_op_6x6_gif():
    load_gif_into(onepiece_gif_frame, "GIF-6x6.png")

def load_op_8x8_gif():
    load_gif_into(onepiece_gif_frame, "GIF-8x8.png")

# Slam Dunk hover loaders
def load_slam_4x4_gif():
    load_gif_into(slamdunk_gif_frame, "GIF-4x4.png")

def load_slam_6x6_gif():
    load_gif_into(slamdunk_gif_frame, "GIF-6x6.png")

def load_slam_8x8_gif():
    load_gif_into(slamdunk_gif_frame, "GIF-8x8.png")

# Dragon Ball hover loaders
def load_db_4x4_gif():
    load_gif_into(dragonball_gif_frame, "GIF-4x4.png")

def load_db_6x6_gif():
    load_gif_into(dragonball_gif_frame, "GIF-6x6.png")

def load_db_8x8_gif():
    load_gif_into(dragonball_gif_frame, "GIF-8x8.png")

# Bleach hover loaders
def load_bleach_4x4_gif():
    load_gif_into(bleach_gif_frame, "GIF-4x4.png")

def load_bleach_6x6_gif():
    load_gif_into(bleach_gif_frame, "GIF-6x6.png")

def load_bleach_8x8_gif():
    load_gif_into(bleach_gif_frame, "GIF-8x8.png")

# Start auto transitions when naruto frame is shown
def go_to_naruto_with_auto_transitions():
    go_to(naruto_frame)
    start_auto_transitions()

# GIF frame is ready for hover effects

# One Piece choose tiles - copy naruto layout
# Add GIF frame to the right side of onepiece_frame (landscape orientation)
onepiece_gif_frame = tk.Frame(onepiece_frame, bg="#1A1A2E", relief="raised", bd=3)
onepiece_gif_frame.place(x=400, y=200, width=800, height=400)

# Create 4x4 button with hover effect
onepiece_4x4_btn = ctk.CTkButton(
    onepiece_frame,
    text="4x4",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_opgame(4),
)
pywinstyles.set_opacity(onepiece_4x4_btn, color="#000001")
onepiece_4x4_btn.place(x=150, y=300)

# Add hover effects to 4x4 button
def on_op_4x4_enter(event):
    stop_auto_transitions()
    load_op_4x4_gif()

def on_op_4x4_leave(event):
    clear_gif()
    start_auto_transitions()

onepiece_4x4_btn.bind("<Enter>", on_op_4x4_enter)
onepiece_4x4_btn.bind("<Leave>", on_op_4x4_leave)

# Create 6x6 button with hover effect
onepiece_6x6_btn = ctk.CTkButton(
    onepiece_frame,
    text="6x6",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_opgame(6),
)
pywinstyles.set_opacity(onepiece_6x6_btn, color="#000001")
onepiece_6x6_btn.place(x=150, y=400)

# Add hover effects to 6x6 button
def on_op_6x6_enter(event):
    stop_auto_transitions()
    load_op_6x6_gif()

def on_op_6x6_leave(event):
    clear_gif()
    start_auto_transitions()

onepiece_6x6_btn.bind("<Enter>", on_op_6x6_enter)
onepiece_6x6_btn.bind("<Leave>", on_op_6x6_leave)

# Create 8x8 button with hover effect
onepiece_8x8_btn = ctk.CTkButton(
    onepiece_frame,
    text="8x8",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_opgame(8),
)
pywinstyles.set_opacity(onepiece_8x8_btn, color="#000001")
onepiece_8x8_btn.place(x=150, y=500)

# Add hover effects to 8x8 button
def on_op_8x8_enter(event):
    stop_auto_transitions()
    load_op_8x8_gif()

def on_op_8x8_leave(event):
    clear_gif()
    start_auto_transitions()

onepiece_8x8_btn.bind("<Enter>", on_op_8x8_enter)
onepiece_8x8_btn.bind("<Leave>", on_op_8x8_leave)

make_back_btn(onepiece_frame, "Back", lambda: go_to(themes_frame), "#FF6B6B", "#FF5252")

# Slam Dunk choose tiles - copy naruto layout
# Add GIF frame to the right side of slamdunk_frame (landscape orientation)
slamdunk_gif_frame = tk.Frame(slamdunk_frame, bg="#1A1A2E", relief="raised", bd=3)
slamdunk_gif_frame.place(x=400, y=200, width=800, height=400)

# Create 4x4 button with hover effect
slamdunk_4x4_btn = ctk.CTkButton(
    slamdunk_frame,
    text="4x4",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_slamgame(4),
)
pywinstyles.set_opacity(slamdunk_4x4_btn, color="#000001")
slamdunk_4x4_btn.place(x=150, y=300)

# Add hover effects to 4x4 button
def on_slam_4x4_enter(event):
    stop_auto_transitions()
    load_slam_4x4_gif()

def on_slam_4x4_leave(event):
    clear_gif()
    start_auto_transitions()

slamdunk_4x4_btn.bind("<Enter>", on_slam_4x4_enter)
slamdunk_4x4_btn.bind("<Leave>", on_slam_4x4_leave)

# Create 6x6 button with hover effect
slamdunk_6x6_btn = ctk.CTkButton(
    slamdunk_frame,
    text="6x6",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_slamgame(6),
)
pywinstyles.set_opacity(slamdunk_6x6_btn, color="#000001")
slamdunk_6x6_btn.place(x=150, y=400)

# Add hover effects to 6x6 button
def on_slam_6x6_enter(event):
    stop_auto_transitions()
    load_slam_6x6_gif()

def on_slam_6x6_leave(event):
    clear_gif()
    start_auto_transitions()

slamdunk_6x6_btn.bind("<Enter>", on_slam_6x6_enter)
slamdunk_6x6_btn.bind("<Leave>", on_slam_6x6_leave)

# Create 8x8 button with hover effect
slamdunk_8x8_btn = ctk.CTkButton(
    slamdunk_frame,
    text="8x8",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_slamgame(8),
)
pywinstyles.set_opacity(slamdunk_8x8_btn, color="#000001")
slamdunk_8x8_btn.place(x=150, y=500)

# Add hover effects to 8x8 button
def on_slam_8x8_enter(event):
    stop_auto_transitions()
    load_slam_8x8_gif()

def on_slam_8x8_leave(event):
    clear_gif()
    start_auto_transitions()

slamdunk_8x8_btn.bind("<Enter>", on_slam_8x8_enter)
slamdunk_8x8_btn.bind("<Leave>", on_slam_8x8_leave)

make_back_btn(slamdunk_frame, "Back", lambda: go_to(themes_frame), "#FF6B6B", "#FF5252")

# Dragon Ball choose tiles - copy naruto layout
# Add GIF frame to the right side of dragonball_frame (landscape orientation)
dragonball_gif_frame = tk.Frame(dragonball_frame, bg="#1A1A2E", relief="raised", bd=3)
dragonball_gif_frame.place(x=400, y=200, width=800, height=400)

# Create 4x4 button with hover effect
dragonball_4x4_btn = ctk.CTkButton(
    dragonball_frame,
    text="4x4",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_dbgame(4),
)
pywinstyles.set_opacity(dragonball_4x4_btn, color="#000001")
dragonball_4x4_btn.place(x=150, y=300)

# Add hover effects to 4x4 button
def on_db_4x4_enter(event):
    stop_auto_transitions()
    load_db_4x4_gif()

def on_db_4x4_leave(event):
    clear_gif()
    start_auto_transitions()

dragonball_4x4_btn.bind("<Enter>", on_db_4x4_enter)
dragonball_4x4_btn.bind("<Leave>", on_db_4x4_leave)

# Create 6x6 button with hover effect
dragonball_6x6_btn = ctk.CTkButton(
    dragonball_frame,
    text="6x6",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_dbgame(6),
)
pywinstyles.set_opacity(dragonball_6x6_btn, color="#000001")
dragonball_6x6_btn.place(x=150, y=400)

# Add hover effects to 6x6 button
def on_db_6x6_enter(event):
    stop_auto_transitions()
    load_db_6x6_gif()

def on_db_6x6_leave(event):
    clear_gif()
    start_auto_transitions()

dragonball_6x6_btn.bind("<Enter>", on_db_6x6_enter)
dragonball_6x6_btn.bind("<Leave>", on_db_6x6_leave)

# Create 8x8 button with hover effect
dragonball_8x8_btn = ctk.CTkButton(
    dragonball_frame,
    text="8x8",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_dbgame(8),
)
pywinstyles.set_opacity(dragonball_8x8_btn, color="#000001")
dragonball_8x8_btn.place(x=150, y=500)

# Add hover effects to 8x8 button
def on_db_8x8_enter(event):
    stop_auto_transitions()
    load_db_8x8_gif()

def on_db_8x8_leave(event):
    clear_gif()
    start_auto_transitions()

dragonball_8x8_btn.bind("<Enter>", on_db_8x8_enter)
dragonball_8x8_btn.bind("<Leave>", on_db_8x8_leave)

make_back_btn(dragonball_frame, "Back", lambda: go_to(themes_frame), "#FF6B6B", "#FF5252")

# Bleach choose tiles - copy naruto layout
# Add GIF frame to the right side of bleach_frame (landscape orientation)
bleach_gif_frame = tk.Frame(bleach_frame, bg="#1A1A2E", relief="raised", bd=3)
bleach_gif_frame.place(x=400, y=200, width=800, height=400)

# Create 4x4 button with hover effect
bleach_4x4_btn = ctk.CTkButton(
    bleach_frame,
    text="4x4",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_bleachgame(4),
)
pywinstyles.set_opacity(bleach_4x4_btn, color="#000001")
bleach_4x4_btn.place(x=150, y=300)

# Add hover effects to 4x4 button
def on_bleach_4x4_enter(event):
    stop_auto_transitions()
    load_bleach_4x4_gif()

def on_bleach_4x4_leave(event):
    clear_gif()
    start_auto_transitions()

bleach_4x4_btn.bind("<Enter>", on_bleach_4x4_enter)
bleach_4x4_btn.bind("<Leave>", on_bleach_4x4_leave)

# Create 6x6 button with hover effect
bleach_6x6_btn = ctk.CTkButton(
    bleach_frame,
    text="6x6",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_bleachgame(6),
)
pywinstyles.set_opacity(bleach_6x6_btn, color="#000001")
bleach_6x6_btn.place(x=150, y=400)

# Add hover effects to 6x6 button
def on_bleach_6x6_enter(event):
    stop_auto_transitions()
    load_bleach_6x6_gif()

def on_bleach_6x6_leave(event):
    clear_gif()
    start_auto_transitions()

bleach_6x6_btn.bind("<Enter>", on_bleach_6x6_enter)
bleach_6x6_btn.bind("<Leave>", on_bleach_6x6_leave)

# Create 8x8 button with hover effect
bleach_8x8_btn = ctk.CTkButton(
    bleach_frame,
    text="8x8",
    font=(font_name, 18, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    width=100,
    height=50,
    corner_radius=15,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to_bleachgame(8),
)
pywinstyles.set_opacity(bleach_8x8_btn, color="#000001")
bleach_8x8_btn.place(x=150, y=500)

# Add hover effects to 8x8 button
def on_bleach_8x8_enter(event):
    stop_auto_transitions()
    load_bleach_8x8_gif()

def on_bleach_8x8_leave(event):
    clear_gif()
    start_auto_transitions()

bleach_8x8_btn.bind("<Enter>", on_bleach_8x8_enter)
bleach_8x8_btn.bind("<Leave>", on_bleach_8x8_leave)

make_back_btn(bleach_frame, "Back", lambda: go_to(themes_frame), "#FF6B6B", "#FF5252")

# --- Ensure theme selection also has a visible Back to Themes button on each theme main (optional) ---
themes_home_btn = ctk.CTkButton(
    themes_frame,
    text="Home",
    font=(font_name, 14, "bold"),
    fg_color="#FF6B6B",
    bg_color="#000001",
    text_color="white",
    hover_color="#FF5252",
    corner_radius=12,
    width=80,
    height=35,
    border_width=2,
    border_color="#FFFFFF",
    command=lambda: go_to(home_frame),
)
pywinstyles.set_opacity(themes_home_btn, color="#000001")
themes_home_btn.place(relx=0.02, rely=0.02, anchor="nw")

# --- Start the app ---
root.mainloop()
