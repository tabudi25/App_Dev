# Main application file for Multi-theme Flip Memory     ame
import tkinter as tk
import customtkinter as ctk
import pywinstyles

# Import modules
from constants import COLOR_BG_PANEL, COLOR_PANEL_ACCENT, COLOR_BTN_TEXT, FONT_NAMES
from font_loader import load_custom_font, verify_font
from audio import play_intro, toggle_mute, load_sound_effects
from game_logic import (
    initialize_game_state, register_game_frame, reset_game, update_timer, cancel_timer,
    paused, timer_running, grid_size
)
from navigation import (
    go_to, exit_app, go_to_narutogame, go_to_opgame, go_to_slamgame,
    go_to_dbgame, go_to_bleachgame, back_to_themes, get_current_theme
)
from ui_components import (
    set_bg, make_theme_btn, make_tile_btn, make_back_btn
)
from theme_handlers import (
    set_root_reference, load_4x4_gif, load_6x6_gif, load_8x8_gif,
    clear_gif, start_auto_transitions, stop_auto_transitions,
    load_op_4x4_gif, load_op_6x6_gif, load_op_8x8_gif,
    load_slam_4x4_gif, load_slam_6x6_gif, load_slam_8x8_gif,
    load_db_4x4_gif, load_db_6x6_gif, load_db_8x8_gif,
    load_bleach_4x4_gif, load_bleach_6x6_gif, load_bleach_8x8_gif
)
from game_frames import create_game_frame

# Load font
font_name = load_custom_font()
verify_font(FONT_NAMES)

# Initialize window
root = tk.Tk()
root.geometry("1920x1090")
root.title("Flip Memory Game")

# Set root reference for theme handlers
set_root_reference(root)

# Create frames
home_frame = tk.Frame(root)
themes_frame = tk.Frame(root)
naruto_frame = tk.Frame(root)
onepiece_frame = tk.Frame(root)
slamdunk_frame = tk.Frame(root)
dragonball_frame = tk.Frame(root)
bleach_frame = tk.Frame(root)
howto_frame = tk.Frame(root, bg="#1A3D64")

# Create separate game frames for each theme
naruto_game = create_game_frame(root, FONT_NAMES, "naruto")
op_game = create_game_frame(root, FONT_NAMES, "op")
slam_game = create_game_frame(root, FONT_NAMES, "slam")
db_game = create_game_frame(root, FONT_NAMES, "db")
bleach_game = create_game_frame(root, FONT_NAMES, "bleach")

# Extract game frames
naruto_game_frame = naruto_game['game_frame']
op_game_frame = op_game['game_frame']
slam_game_frame = slam_game['game_frame']
db_game_frame = db_game['game_frame']
bleach_game_frame = bleach_game['game_frame']

ALL_FRAMES = [
    home_frame, themes_frame, naruto_frame, onepiece_frame,
    slamdunk_frame, dragonball_frame, bleach_frame,
    naruto_game_frame, op_game_frame, slam_game_frame,
    db_game_frame, bleach_game_frame, howto_frame
]

for f in ALL_FRAMES:
    f.place(relwidth=1, relheight=1)
home_frame.lift()

# Set backgrounds
set_bg(home_frame, "homep1.PNG")
set_bg(themes_frame, "themes.PNG")
set_bg(naruto_frame, "narutobg.png")
set_bg(onepiece_frame, "onepiecebg.png")
set_bg(slamdunk_frame, "slamD.png")
set_bg(dragonball_frame, "dragonballbg.png")
set_bg(bleach_frame, "bleachbg.png")
set_bg(howto_frame, "homep1.png")

# Set themes frame reference in navigation
from navigation import set_themes_frame
set_themes_frame(themes_frame)

# Initialize game state and register all game frames
initialize_game_state(naruto_game, root)

# Register all game frames
register_game_frame("naruto", naruto_game)
register_game_frame("op", op_game)
register_game_frame("slam", slam_game)
register_game_frame("db", db_game)
register_game_frame("bleach", bleach_game)

# === HOME FRAME UI ===
start_btn = ctk.CTkButton(
    home_frame, text="START", font=(FONT_NAMES, 24, "bold"),
    fg_color="#787c82", bg_color="#000001", text_color="black",
    hover_color="#FF5252", width=242, height=50, corner_radius=20,
    border_width=2, border_color="white",
    command=lambda: go_to(themes_frame, home_frame)
)

def on_start_enter(event):
    start_btn.configure(text_color="white")
    start_btn.configure(fg_color="black")
    start_btn.configure(border_color="white")

def on_start_leave(event):
    start_btn.configure(text_color="black")
    start_btn.configure(fg_color="#787c82")
    start_btn.configure(border_color="white")

start_btn.bind("<Enter>", on_start_enter)
start_btn.bind("<Leave>", on_start_leave)

pywinstyles.set_opacity(start_btn, color="#000001")
start_btn.place(x=732, y=400, anchor="center")

howto_btn = ctk.CTkButton(
    home_frame, text="HOW TO PLAY", font=(FONT_NAMES, 24, "bold"),
    fg_color="#787c82", bg_color="#000001", text_color="black",
    hover_color="#FF5252", width=242, height=50, corner_radius=20,
    border_width=2, border_color="white",
    command=lambda: go_to(howto_frame, home_frame)
)
pywinstyles.set_opacity(howto_btn, color="#000001")
howto_btn.place(relx=0.5, y=490, anchor="center")

def on_howto_enter(event):
    howto_btn.configure(text_color="white")
    howto_btn.configure(fg_color="black")
    howto_btn.configure(border_color="white")

def on_howto_leave(event):
    howto_btn.configure(text_color="black")
    howto_btn.configure(fg_color="#787c82")
    howto_btn.configure(border_color="white") 

howto_btn.bind("<Enter>", on_howto_enter)
howto_btn.bind("<Leave>", on_howto_leave)

exit_btn = ctk.CTkButton(
    home_frame, text="EXIT", font=(FONT_NAMES, 24, "bold"),
    fg_color="#787c82", bg_color="#000001", text_color="black",
    hover_color="#FF5252", width=242, height=50, corner_radius=20,
    border_width=2, border_color="white", command=lambda: exit_app(root)
)
pywinstyles.set_opacity(exit_btn, color="#000001")
exit_btn.place(relx=0.5, y=585, anchor="center")

def on_exit_enter(event):
    exit_btn.configure(text_color="white")
    exit_btn.configure(fg_color="black")
    exit_btn.configure(border_color="white")

def on_exit_leave(event):
    exit_btn.configure(text_color="black")
    exit_btn.configure(fg_color="#787c82")
    exit_btn.configure(border_color="white")

exit_btn.bind("<Enter>", on_exit_enter)
exit_btn.bind("<Leave>", on_exit_leave)


mute_btn = ctk.CTkButton(
    home_frame, text="🔊", font=(FONT_NAMES, 24, "bold"),
    fg_color="#787c82", bg_color="#000001", text_color="black",
    hover_color="#FF5252", width=40, height=50, corner_radius=20,
    border_width=2, border_color="white",
    command=lambda: toggle_mute(mute_btn)
)
pywinstyles.set_opacity(mute_btn, color="#000001")
mute_btn.place(x=1400, y=35, anchor="center")

def on_mute_enter(event):
    mute_btn.configure(text_color="white")
    mute_btn.configure(fg_color="black")
    mute_btn.configure(border_color="white")

def on_mute_leave(event):
    mute_btn.configure(text_color="black")
    mute_btn.configure(fg_color="#787c82")
    mute_btn.configure(border_color="white")

mute_btn.bind("<Enter>", on_mute_enter)
mute_btn.bind("<Leave>", on_mute_leave)

# === THEMES FRAME UI ===
naruto_theme_btn = make_theme_btn(
    themes_frame, "Naruto", 180,
    lambda: go_to_naruto_with_auto_transitions(), FONT_NAMES
)
naruto_theme_btn.place(x=130, y=490)

onepiece_theme_btn = make_theme_btn(
    themes_frame, "One Piece", 260,
    lambda: go_to_onepiece_with_auto_transitions(), FONT_NAMES
)
onepiece_theme_btn.place(x=1030, y=490)

slamdunk_theme_btn = make_theme_btn(
    themes_frame, "Slam Dunk", 340,
    lambda: go_to_slamdunk_with_auto_transitions(), FONT_NAMES
)
slamdunk_theme_btn.place(x=420, y=490)

db_theme_btn = make_theme_btn(
    themes_frame, "Dragon Ball", 420,
    lambda: go_to_dragonball_with_auto_transitions(), FONT_NAMES
)
db_theme_btn.place(x=1350, y=490)

bleach_theme_btn = make_theme_btn(
    themes_frame, "Bleach", 500,
    lambda: go_to_bleach_with_auto_transitions(), FONT_NAMES
)
bleach_theme_btn.place(x=720, y=490)

themes_home_btn = ctk.CTkButton(
    themes_frame, text="Home", font=(FONT_NAMES, 14, "bold"),
    fg_color="#787c82", bg_color="#000001", text_color="black",
    hover_color="white", corner_radius=12, width=85, height=45,
    border_width=2, border_color="white",
    command=lambda: go_to(home_frame, home_frame)
)

def on_themes_home_enter(event):
    themes_home_btn.configure(text_color="white")
    themes_home_btn.configure(fg_color="black")
    themes_home_btn.configure(border_color="white")

def on_themes_home_leave(event):
    themes_home_btn.configure(text_color="black")
    themes_home_btn.configure(fg_color="#787c82")
    themes_home_btn.configure(border_color="white")

themes_home_btn.bind("<Enter>", on_themes_home_enter)
themes_home_btn.bind("<Leave>", on_themes_home_leave)

pywinstyles.set_opacity(themes_home_btn, color="#000001")
themes_home_btn.place(relx=0.02, rely=0.02, anchor="nw")

# === HOW TO PLAY FRAME ===
main_container = tk.Frame(howto_frame, bg="black", relief="raised", bd=10)
main_container.place(relx=0.5, rely=0.5, anchor="center", width=1090, height=750)

title_label = tk.Label(
    main_container, text="------------------------------------------ HOW TO PLAY -----------------------------------------", font=(FONT_NAMES, 15, "bold"),
    fg="white", bg="black"
)
title_label.pack(pady=(30, 15))

# Create a canvas with scrollbar for scrollable content
canvas = tk.Canvas(main_container, bg="black", highlightthickness=0)
scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
instruction_frame = tk.Frame(canvas, bg="black")

# Store reference to the canvas window
canvas_window = canvas.create_window((0, 0), window=instruction_frame, anchor="nw")

# Update scroll region and canvas window width
def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    # Update canvas window width to match canvas width
    canvas_width = canvas.winfo_width()
    if canvas_width > 1:  # Only update if canvas has been rendered
        canvas.itemconfig(canvas_window, width=canvas_width)

instruction_frame.bind("<Configure>", update_scroll_region)
canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

canvas.configure(yscrollcommand=scrollbar.set)

# Enable mouse wheel scrolling
def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

canvas.pack(side="left", fill="both", expand=True, padx=(35, 0), pady=15)
scrollbar.pack(side="right", fill="y", padx=(0, 35), pady=15)

# Theme Selection
theme_section = tk.Frame(instruction_frame, bg="black", relief="raised", bd=0)
theme_section.pack(fill="x", pady=4)

theme_title = tk.Label(
    theme_section, 
    text="🎮 Choose a Theme", font=(FONT_NAMES, 12, "bold"),
    fg="White", bg="black"
)
theme_title.pack(anchor="w", padx=20, pady=(0, 0))

theme_text = tk.Label(
    theme_section,
    text="Pick your favorite anime world — Naruto, One Piece, Slam Dunk, Dragon Ball, or Bleach.",
    font=(FONT_NAMES, 12, "bold"), fg="White", bg="black",
    wraplength=750, justify="left"
)
theme_text.pack(anchor="w", padx=20, pady=(0, 15))

# Difficulty Selection
diff_section = tk.Frame(instruction_frame, bg="black", bd=0)
diff_section.pack(fill="x", pady=8)

diff_title = tk.Label(
    diff_section, text="⚡ Select a Difficulty", font=(FONT_NAMES, 12, "bold"),
    fg="White", bg="black"
)
diff_title.pack(anchor="w", padx=20, pady=(15, 8))

diff_text = tk.Label(
    diff_section,
    text="Choose your board size:\n4x4 → Easy (8 pairs)\n6x6 → Medium (18 pairs)\n8x8 → Hard (32 pairs)",
    font=(FONT_NAMES, 12, "bold"), fg="White", bg="black", justify="left"
)
diff_text.pack(anchor="w", padx=20, pady=(0, 15))

# Gameplay
gameplay_section = tk.Frame(instruction_frame, bg="black", relief="raised", bd=0)
gameplay_section.pack(fill="x", pady=4)

gameplay_title = tk.Label(
    gameplay_section, text="🎯 Start the Game", font=(FONT_NAMES, 12, "bold"),
    fg="White", bg="black"
)
gameplay_title.pack(anchor="w", padx=20, pady=(15, 8))

gameplay_text = tk.Label(
    gameplay_section,
    text="Flip two cards to reveal their pictures.\nMatch all pairs before time runs out!",
    font=(FONT_NAMES, 12, "bold"), fg="White", bg="black", justify="left"
)
gameplay_text.pack(anchor="w", padx=20, pady=(0, 15))

# Scoring
scoring_section = tk.Frame(instruction_frame, bg="black", relief="raised", bd=0)
scoring_section.pack(fill="x", pady=8)

scoring_title = tk.Label(
    scoring_section, text="🏆 Scoring", font=(FONT_NAMES, 12, "bold"),
    fg="White", bg="black"
)
scoring_title.pack(anchor="w", padx=20, pady=(15, 8))

scoring_text = tk.Label(
    scoring_section,
    text="+5 points for every correct match.\nLimited flips — don't waste your turns!\nYou win when all pairs are matched!",
    font=(FONT_NAMES, 12, "bold"), fg="White", bg="black", justify="left"
)
scoring_text.pack(anchor="w", padx=20, pady=(0, 15))

# Controls
controls_section = tk.Frame(instruction_frame, bg="black", relief="raised", bd=0)
controls_section.pack(fill="x", pady=8)

controls_title = tk.Label(
    controls_section, text="🎮 Controls", font=(FONT_NAMES, 12, "bold"),
    fg="White", bg="black"
)
controls_title.pack(anchor="w", padx=20, pady=(15, 8))

controls_text = tk.Label(
    controls_section,
    text="Pause / Resume – Stop or continue the game.\nReset – Restart the current game.\nBack – Return to the theme menu.",
    font=(FONT_NAMES, 12, "bold"), fg="White", bg="black", justify="left"
)
controls_text.pack(anchor="w", padx=20, pady=(0, 15))

# Game Over
gameover_section = tk.Frame(instruction_frame, bg="black", relief="raised", bd=0)
gameover_section.pack(fill="x", pady=8)

gameover_title = tk.Label(
    gameover_section, text="⚠️ Game Over Conditions", font=(FONT_NAMES, 12, "bold"),
    fg="white", bg="black"
)
gameover_title.pack(anchor="w", padx=20, pady=(15, 8))

gameover_text = tk.Label(
    gameover_section,
    text="Time's up!\nFlip limit reached!\nAll pairs matched = You Win!",
    font=(FONT_NAMES, 12, "bold"), fg="white", bg="black", justify="left"
)
gameover_text.pack(anchor="w", padx=20, pady=(0, 15))

howto_back_btn = ctk.CTkButton(
    howto_frame, text="Back", font=(FONT_NAMES, 16, "bold"),
    fg_color="#787c82", bg_color="#0d1117", text_color="black",
    hover_color="#FF5252", width=120, height=45, corner_radius=20,
    border_width=2, border_color="white",
    command=lambda: go_to(home_frame, home_frame)
)

def on_howto_back_enter(event):
    howto_back_btn.configure(text_color="white")
    howto_back_btn.configure(fg_color="black")
    howto_back_btn.configure(border_color="white")

def on_howto_back_leave(event):
    howto_back_btn.configure(text_color="black")
    howto_back_btn.configure(fg_color="#787c82")
    howto_back_btn.configure(border_color="white")

howto_back_btn.bind("<Enter>", on_howto_back_enter)
howto_back_btn.bind("<Leave>", on_howto_back_leave)

pywinstyles.set_opacity(howto_back_btn, color="#0d1117")
howto_back_btn.place(x=20, y=20)

# === NARUTO FRAME UI ===
naruto_gif_frame = tk.Frame(naruto_frame, bg="white", relief="raised", bd=5)
naruto_gif_frame.place(x=400, y=200, width=715, height=376)


def go_to_naruto_with_auto_transitions():
    go_to(naruto_frame, home_frame)
    start_auto_transitions(naruto_gif_frame, "naruto", "#1A1A2E")


naruto_4x4_btn = make_tile_btn(
    naruto_frame, "4x4", 150, 300,
    lambda: go_to_narutogame(4, naruto_frame, naruto_game_frame),
    "#BF1A1A", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(naruto_4x4_btn, color="#000001")


def on_4x4_enter(event):    
    stop_auto_transitions()
    load_4x4_gif(naruto_gif_frame)


def on_4x4_leave(event):
    clear_gif()
    start_auto_transitions(naruto_gif_frame, "naruto", "#1A1A2E")


naruto_4x4_btn.bind("<Enter>", on_4x4_enter)
naruto_4x4_btn.bind("<Leave>", on_4x4_leave)

naruto_6x6_btn = make_tile_btn(
    naruto_frame, "6x6", 150, 400,
    lambda: go_to_narutogame(6, naruto_frame, naruto_game_frame),
    "#BF1A1A", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(naruto_6x6_btn, color="#000001")


def on_6x6_enter(event):
    stop_auto_transitions()
    load_6x6_gif(naruto_gif_frame)


def on_6x6_leave(event):
    clear_gif()
    start_auto_transitions(naruto_gif_frame, "naruto", "#1A1A2E")


naruto_6x6_btn.bind("<Enter>", on_6x6_enter)
naruto_6x6_btn.bind("<Leave>", on_6x6_leave)

naruto_8x8_btn = make_tile_btn(
    naruto_frame, "8x8", 150, 500,
    lambda: go_to_narutogame(8, naruto_frame, naruto_game_frame),
    "#BF1A1A", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(naruto_8x8_btn, color="#000001")


def on_8x8_enter(event):
    stop_auto_transitions()
    load_8x8_gif(naruto_gif_frame)


def on_8x8_leave(event):
    clear_gif()
    start_auto_transitions(naruto_gif_frame, "naruto", "#1A1A2E")


naruto_8x8_btn.bind("<Enter>", on_8x8_enter)
naruto_8x8_btn.bind("<Leave>", on_8x8_leave)

make_back_btn(
    naruto_frame, "Back", lambda: go_to(themes_frame, home_frame),
    "#BF1A1A", "#8CE4FF", FONT_NAMES
)

# === ONE PIECE FRAME UI ===
onepiece_gif_frame = tk.Frame(onepiece_frame, bg="white", relief="raised", bd=3)
onepiece_gif_frame.place(x=400, y=200, width=715, height=376)


def go_to_onepiece_with_auto_transitions():
    go_to(onepiece_frame, home_frame)
    start_auto_transitions(onepiece_gif_frame, "op", "#F8F4EC")

onepiece_4x4_btn = make_tile_btn(
    onepiece_frame, "4x4", 150, 300,
    lambda: go_to_opgame(4, onepiece_frame, op_game_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(onepiece_4x4_btn, color="#000001")


def on_op_4x4_enter(event):
    stop_auto_transitions()
    load_op_4x4_gif(onepiece_gif_frame)


def on_op_4x4_leave(event):
    clear_gif()
    start_auto_transitions(onepiece_gif_frame, "op", "#F8F4EC")


onepiece_4x4_btn.bind("<Enter>", on_op_4x4_enter)
onepiece_4x4_btn.bind("<Leave>", on_op_4x4_leave)

onepiece_6x6_btn = make_tile_btn(
    onepiece_frame, "6x6", 150, 400,
    lambda: go_to_opgame(6, onepiece_frame, op_game_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(onepiece_6x6_btn, color="#000001")


def on_op_6x6_enter(event):
    stop_auto_transitions()
    load_op_6x6_gif(onepiece_gif_frame)


def on_op_6x6_leave(event):
    clear_gif()
    start_auto_transitions(onepiece_gif_frame, "op", "#F8F4EC")


onepiece_6x6_btn.bind("<Enter>", on_op_6x6_enter)
onepiece_6x6_btn.bind("<Leave>", on_op_6x6_leave)

onepiece_8x8_btn = make_tile_btn(
    onepiece_frame, "8x8", 150, 500,
    lambda: go_to_opgame(8, onepiece_frame, op_game_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(onepiece_8x8_btn, color="#000001")


def on_op_8x8_enter(event):
    stop_auto_transitions()
    load_op_8x8_gif(onepiece_gif_frame)


def on_op_8x8_leave(event):
    clear_gif()
    start_auto_transitions(onepiece_gif_frame, "op", "#F8F4EC")


onepiece_8x8_btn.bind("<Enter>", on_op_8x8_enter)
onepiece_8x8_btn.bind("<Leave>", on_op_8x8_leave)

make_back_btn(
    onepiece_frame, "Back", lambda: go_to(themes_frame, home_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)

# === SLAM DUNK FRAME UI ===
slamdunk_gif_frame = tk.Frame(slamdunk_frame, bg="white", relief="raised", bd=3)
slamdunk_gif_frame.place(x=400, y=200, width=715, height=376)


def go_to_slamdunk_with_auto_transitions():
    go_to(slamdunk_frame, home_frame)
    start_auto_transitions(slamdunk_gif_frame, "slamdunk", "#1A1A2E")

slamdunk_4x4_btn = make_tile_btn(
    slamdunk_frame, "4x4", 150, 300,
    lambda: go_to_slamgame(4, slamdunk_frame, slam_game_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(slamdunk_4x4_btn, color="#000001")


def on_slam_4x4_enter(event):
    stop_auto_transitions()
    load_slam_4x4_gif(slamdunk_gif_frame)


def on_slam_4x4_leave(event):
    clear_gif()
    start_auto_transitions(slamdunk_gif_frame, "slamdunk", "#1A1A2E")


slamdunk_4x4_btn.bind("<Enter>", on_slam_4x4_enter)
slamdunk_4x4_btn.bind("<Leave>", on_slam_4x4_leave)

slamdunk_6x6_btn = make_tile_btn(
    slamdunk_frame, "6x6", 150, 400,
    lambda: go_to_slamgame(6, slamdunk_frame, slam_game_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(slamdunk_6x6_btn, color="#000001")


def on_slam_6x6_enter(event):
    stop_auto_transitions()
    load_slam_6x6_gif(slamdunk_gif_frame)


def on_slam_6x6_leave(event):
    clear_gif()
    start_auto_transitions(slamdunk_gif_frame, "slamdunk", "#1A1A2E")


slamdunk_6x6_btn.bind("<Enter>", on_slam_6x6_enter)
slamdunk_6x6_btn.bind("<Leave>", on_slam_6x6_leave)

slamdunk_8x8_btn = make_tile_btn(
    slamdunk_frame, "8x8", 150, 500,
    lambda: go_to_slamgame(8, slamdunk_frame, slam_game_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(slamdunk_8x8_btn, color="#000001")


def on_slam_8x8_enter(event):
    stop_auto_transitions()
    load_slam_8x8_gif(slamdunk_gif_frame)


def on_slam_8x8_leave(event):
    clear_gif()
    start_auto_transitions(slamdunk_gif_frame, "slamdunk", "#1A1A2E")


slamdunk_8x8_btn.bind("<Enter>", on_slam_8x8_enter)
slamdunk_8x8_btn.bind("<Leave>", on_slam_8x8_leave)

make_back_btn(
    slamdunk_frame, "Back", lambda: go_to(themes_frame, home_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)

# === DRAGON BALL FRAME UI ===
dragonball_gif_frame = tk.Frame(dragonball_frame, bg="white", relief="raised", bd=3)
dragonball_gif_frame.place(x=400, y=200, width=715, height=376)


def go_to_dragonball_with_auto_transitions():
    go_to(dragonball_frame, home_frame)
    start_auto_transitions(dragonball_gif_frame, "db", "#1A1A2E")

dragonball_4x4_btn = make_tile_btn(
    dragonball_frame, "4x4", 150, 300,
    lambda: go_to_dbgame(4, dragonball_frame, db_game_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(dragonball_4x4_btn, color="#000001")


def on_db_4x4_enter(event):
    stop_auto_transitions()
    load_db_4x4_gif(dragonball_gif_frame)


def on_db_4x4_leave(event):
    clear_gif()
    start_auto_transitions(dragonball_gif_frame, "db", "#1A1A2E")


dragonball_4x4_btn.bind("<Enter>", on_db_4x4_enter)
dragonball_4x4_btn.bind("<Leave>", on_db_4x4_leave)

dragonball_6x6_btn = make_tile_btn(
    dragonball_frame, "6x6", 150, 400,
    lambda: go_to_dbgame(6, dragonball_frame, db_game_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(dragonball_6x6_btn, color="#000001")


def on_db_6x6_enter(event):
    stop_auto_transitions()
    load_db_6x6_gif(dragonball_gif_frame)


def on_db_6x6_leave(event):
    clear_gif()
    start_auto_transitions(dragonball_gif_frame, "db", "#1A1A2E")


dragonball_6x6_btn.bind("<Enter>", on_db_6x6_enter)
dragonball_6x6_btn.bind("<Leave>", on_db_6x6_leave)

dragonball_8x8_btn = make_tile_btn(
    dragonball_frame, "8x8", 150, 500,
    lambda: go_to_dbgame(8, dragonball_frame, db_game_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(dragonball_8x8_btn, color="#000001")


def on_db_8x8_enter(event):
    stop_auto_transitions()
    load_db_8x8_gif(dragonball_gif_frame)


def on_db_8x8_leave(event):
    clear_gif()
    start_auto_transitions(dragonball_gif_frame, "db", "#1A1A2E")


dragonball_8x8_btn.bind("<Enter>", on_db_8x8_enter)
dragonball_8x8_btn.bind("<Leave>", on_db_8x8_leave)

make_back_btn(
    dragonball_frame, "Back", lambda: go_to(themes_frame, home_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)

# === BLEACH FRAME UI ===
bleach_gif_frame = tk.Frame(bleach_frame, bg="white", relief="raised", bd=3)
bleach_gif_frame.place(x=400, y=200, width=715, height=376)


def go_to_bleach_with_auto_transitions():
    go_to(bleach_frame, home_frame)
    start_auto_transitions(bleach_gif_frame, "bleach", "#1A1A2E")

bleach_4x4_btn = make_tile_btn(
    bleach_frame, "4x4", 150, 300,
    lambda: go_to_bleachgame(4, bleach_frame, bleach_game_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(bleach_4x4_btn, color="#000001")


def on_bleach_4x4_enter(event):
    stop_auto_transitions()
    load_bleach_4x4_gif(bleach_gif_frame)


def on_bleach_4x4_leave(event):
    clear_gif()
    start_auto_transitions(bleach_gif_frame, "bleach", "#1A1A2E")


bleach_4x4_btn.bind("<Enter>", on_bleach_4x4_enter)
bleach_4x4_btn.bind("<Leave>", on_bleach_4x4_leave)

bleach_6x6_btn = make_tile_btn(
    bleach_frame, "6x6", 150, 400,
    lambda: go_to_bleachgame(6, bleach_frame, bleach_game_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(bleach_6x6_btn, color="#000001")


def on_bleach_6x6_enter(event):
    stop_auto_transitions()
    load_bleach_6x6_gif(bleach_gif_frame)


def on_bleach_6x6_leave(event):
    clear_gif()
    start_auto_transitions(bleach_gif_frame, "bleach", "#1A1A2E")


bleach_6x6_btn.bind("<Enter>", on_bleach_6x6_enter)
bleach_6x6_btn.bind("<Leave>", on_bleach_6x6_leave)

bleach_8x8_btn = make_tile_btn(
    bleach_frame, "8x8", 150, 500,
    lambda: go_to_bleachgame(8, bleach_frame, bleach_game_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)
pywinstyles.set_opacity(bleach_8x8_btn, color="#000001")


def on_bleach_8x8_enter(event):
    stop_auto_transitions()
    load_bleach_8x8_gif(bleach_gif_frame)


def on_bleach_8x8_leave(event):
    clear_gif()
    start_auto_transitions(bleach_gif_frame, "bleach", "#1A1A2E")


bleach_8x8_btn.bind("<Enter>", on_bleach_8x8_enter)
bleach_8x8_btn.bind("<Leave>", on_bleach_8x8_leave)

make_back_btn(
    bleach_frame, "Back", lambda: go_to(themes_frame, home_frame),
    "#FF6B6B", "#FF5252", FONT_NAMES
)

# Start intro music
play_intro()

# Start the app
root.mainloop()
