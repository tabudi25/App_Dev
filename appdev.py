# FULL CODE: Multi-theme Flip Memory Game (shared game frame; different image sets per theme)
# Save as e.g. memory_game.py and run with Python 3 (Pillow & pygame required).
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import customtkinter as ctk
import random, time, pygame, os

import pywinstyles


# --- Initialize music ---
pygame.mixer.init()

# --- Colors / constants ---
COLOR_BG_PANEL = "#000000"
COLOR_PANEL_ACCENT = "#34495e"
COLOR_BTN_TEXT = "white"


# --- Music / SFX helpers ---
def play_music():
    if os.path.exists("narutomusic.mp3"):
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

# --- Frames (screens) ---
home_frame = tk.Frame(root)
themes_frame = tk.Frame(root)
naruto_frame = tk.Frame(root)
onepiece_frame = tk.Frame(root)
slamdunk_frame = tk.Frame(root)
dragonball_frame = tk.Frame(root)
bleach_frame = tk.Frame(root)
game_frame = tk.Frame(root, bg="#000001")
pywinstyles.set_opacity(game_frame, color="#000001")

ALL_FRAMES = [
    home_frame,
    themes_frame,
    naruto_frame,
    onepiece_frame,
    slamdunk_frame,
    dragonball_frame,
    bleach_frame,
    game_frame,
]

for f in ALL_FRAMES:
    f.place(relwidth=1, relheight=1)
home_frame.lift()


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
set_bg(slamdunk_frame, "slamdunkbg.png")
set_bg(dragonball_frame, "dragonballbg.png")
set_bg(bleach_frame, "bleachbg.png")
set_bg(game_frame, "narutogamebg.png")


# --- Navigation helpers ---
def go_to(frame):
    frame.lift()


current_theme = "naruto"


def exit_app():
    root.destroy()


def go_to_narutogame(size=4):
    global current_theme
    current_theme = "naruto"
    naruto_frame.lower()
    game_frame.lift()
    play_music()
    reset_game(size, theme=current_theme)


def go_to_opgame(size=4):
    global current_theme
    current_theme = "op"
    onepiece_frame.lower()
    game_frame.lift()
    play_music()
    reset_game(size, theme=current_theme)


def go_to_slamgame(size=4):
    global current_theme
    current_theme = "slam"
    slamdunk_frame.lower()
    game_frame.lift()
    play_music()
    reset_game(size, theme=current_theme)


def go_to_dbgame(size=4):
    global current_theme
    current_theme = "db"
    dragonball_frame.lower()
    game_frame.lift()
    play_music()
    reset_game(size, theme=current_theme)


def go_to_bleachgame(size=4):
    global current_theme
    current_theme = "bleach"
    bleach_frame.lower()
    game_frame.lift()
    play_music()
    reset_game(size, theme=current_theme)


# --- Game settings & globals ---
card_size = (120, 120)
time_limit = 60
flip_limit = 20

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
    score_panel, text="Score: 0", font=("Arial", 18), fg="white", bg=COLOR_PANEL_ACCENT
)  # Label para score
score_label.pack(side="left", padx=(6, 12))  # Gibutang left sa sulod sa panel

# === FLIPS & TIMER LABELS (top center & right) ===
flips_label = tk.Label(
    game_frame,
    text=f"Flips: 0/{flip_limit}",
    font=("Arial", 18),
    fg="white",
    bg=COLOR_PANEL_ACCENT,
)  # Label para flips count
flips_label.grid(row=0, column=1, padx=20)  # Gibutang sa row=0 col=1

timer_label = tk.Label(
    game_frame,
    text=f"Time: {time_limit}s",
    font=("Arial", 18),
    fg="white",
    bg=COLOR_PANEL_ACCENT,
)  # Label para countdown timer
timer_label.grid(row=0, column=2, padx=20)  # Gibutang sa row=0 col=2

# === PAUSE OVERLAY (large text overlay center) ===
pause_overlay = tk.Label(
    game_frame,
    text="The Game Paused",
    font=("Arial", 48, "bold"),
    fg="yellow",
    bg="black",
)  # Overlay text "paused"
pause_overlay.place(relx=0.5, rely=0.5, anchor="center")  # Center overlay
pause_overlay.lower()  # By default nakatago

# === SIDE PANEL (right control buttons) ===
side_panel = tk.Frame(game_frame, bg=COLOR_BG_PANEL)  # Container sa right side
side_panel.place(relx=0.95, rely=0.5, anchor="e")  # Placed near right edge

# === BUTTON CONFIGURATION (shared style) ===
btn_cfg = {
    "font": ("Arial", 14, "bold"),
    "fg": COLOR_BTN_TEXT,
    "width": 12,
    "height": 2,
    "cursor": "hand2",
    "bd": 0,
    "relief": "flat",
}


# === PAUSE TOGGLE HANDLER ===
def on_pause_toggle():
    """Toggle between pause and resume state"""
    global paused, timer_running
    if paused:  # If currently paused → resume
        paused = False
        timer_running = True
        pause_btn.configure(
            text="⏸ Pause", fg_color="#3498db", hover_color="#2980b9"
        )  # Change button look
        pause_overlay.lower()  # Hide overlay
        play_music()  # Resume bg music
        update_timer()  # Resume timer
    else:  # If currently running → pause
        paused = True
        timer_running = False
        pause_btn.configure(
            text="▶ Resume", fg_color="#27ae60", hover_color="#1e8449"
        )  # Change button look
        stop_music()  # Stop bg music
        pause_overlay.lift()  # Show overlay


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
    pause_overlay.lower()  # Hide pause overlay
    game_frame.lower()  # Hide game frame
    themes_frame.lift()  # Show themes menu


# === CONTROL BUTTONS (in side_panel) ===
reset_btn = ctk.CTkButton(
    side_panel,
    text="⟳ Reset",
    fg_color="#e74c3c",
    bg_color="#000001",
    hover_color="#c0392b",
    text_color=COLOR_BTN_TEXT,
    font=("Arial", 14, "bold"),
    width=12 * 10,
    height=2 * 20,
    corner_radius=15,
    command=lambda: reset_game(grid_size, theme=current_theme),
)  # Reset board
pywinstyles.set_opacity(reset_btn, color="#000001")
reset_btn.pack(pady=12, fill="x")  # Add spacing, full width

back_btn = ctk.CTkButton(
    side_panel,
    text="← Back",
    fg_color="#e67e22",
    bg_color="#000001",
    hover_color="#d35400",
    text_color=COLOR_BTN_TEXT,
    font=("Arial", 14, "bold"),
    width=12 * 10,
    height=2 * 20,
    corner_radius=15,
    command=back_to_themes,
)  # Back to theme menu
pywinstyles.set_opacity(back_btn, color="#000001")
back_btn.pack(pady=12, fill="x")

pause_btn = ctk.CTkButton(
    side_panel,
    text="⏸ Pause",
    fg_color="#3498db",
    bg_color="#000001",
    hover_color="#2980b9",
    text_color=COLOR_BTN_TEXT,
    font=("Arial", 14, "bold"),
    width=12 * 10,
    height=2 * 20,
    corner_radius=15,
    command=on_pause_toggle,
)  # Pause/Resume toggle
pywinstyles.set_opacity(pause_btn, color="#000001")
pause_btn.pack(pady=12, fill="x")

# === BOARD FRAME (main card grid area) ===
board_frame = tk.Frame(game_frame, bg=COLOR_BG_PANEL)  # Board container for cards
board_frame.place(relx=0.5, rely=0.45, anchor="center")  # Positioned center

# === RESULT LABEL (for overlay messages like win/lose) ===
result_label = tk.Label(
    game_frame, text="", font=("Arial", 40, "bold"), fg="yellow", bg="black"
)  # Big text for result
result_label.place(relx=0.5, rely=0.5, anchor="center")  # Center screen
result_label.lower()  # Hide by default


# --- WIN OVERLAY BOX ---
win_overlay = tk.Frame(game_frame, bg="black", bd=4, relief="ridge")
win_overlay.place(relx=0.5, rely=0.5, anchor="center", width=400, height=250)
win_overlay.lower()

win_msg = tk.Label(
    win_overlay, text="You Win!", font=("Arial", 28, "bold"), fg="lime", bg="black"
)
win_msg.pack(pady=(15, 5))
win_stats = tk.Label(win_overlay, text="", font=("Arial", 16), fg="white", bg="black")
win_stats.pack(pady=10)


def on_win_reset():
    win_overlay.lower()
    reset_game(grid_size, theme=current_theme)


def on_win_back():
    win_overlay.lower()
    back_to_themes()


win_btns = tk.Frame(win_overlay, bg="black")
win_btns.pack(side="bottom", pady=15)

win_reset_btn = ctk.CTkButton(
    win_btns,
    text="⟳ Reset",
    font=("Arial", 14, "bold"),
    fg_color="#e74c3c",
    bg_color="#000001",
    hover_color="#c0392b",
    text_color="white",
    width=100,
    corner_radius=12,
    command=on_win_reset,
)
pywinstyles.set_opacity(win_reset_btn, color="#000001")
win_reset_btn.pack(side="left", padx=10)

win_back_btn = ctk.CTkButton(
    win_btns,
    text="← Back",
    font=("Arial", 14, "bold"),
    fg_color="#e67e22",
    bg_color="#000001",
    hover_color="#d35400",
    text_color="white",
    width=100,
    corner_radius=12,
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
    font=("Arial", 24, "bold"),
    fg="red",
    bg="black",
)
flip_msg.pack(pady=(15, 5))
flip_stats = tk.Label(flip_overlay, text="", font=("Arial", 16), fg="white", bg="black")
flip_stats.pack(pady=10)

flip_reset_btn = ctk.CTkButton(
    flip_overlay,
    text="⟳ Reset",
    font=("Arial", 14, "bold"),
    fg_color="#e74c3c",
    bg_color="#000001",
    hover_color="#c0392b",
    text_color="white",
    width=100,
    corner_radius=12,
    command=on_win_reset,
)
pywinstyles.set_opacity(flip_reset_btn, color="#000001")
flip_reset_btn.pack(side="left", padx=10)

flip_back_btn = ctk.CTkButton(
    flip_overlay,
    text="← Back",
    font=("Arial", 14, "bold"),
    fg_color="#e67e22",
    bg_color="#000001",
    hover_color="#d35400",
    text_color="white",
    width=100,
    corner_radius=12,
    command=on_win_back,
)
pywinstyles.set_opacity(flip_back_btn, color="#000001")
flip_back_btn.pack(side="right", padx=10)

# --- TIME OVERLAY BOX ---
time_overlay = tk.Frame(game_frame, bg="black", bd=4, relief="ridge")
time_overlay.place(relx=0.5, rely=0.5, anchor="center", width=400, height=250)
time_overlay.lower()

time_msg = tk.Label(
    time_overlay, text="Time's Up!", font=("Arial", 24, "bold"), fg="red", bg="black"
)
time_msg.pack(pady=(15, 5))
time_stats = tk.Label(time_overlay, text="", font=("Arial", 16), fg="white", bg="black")
time_stats.pack(pady=10)

time_reset_btn = ctk.CTkButton(
    time_overlay,
    text="⟳ Reset",
    font=("Arial", 14, "bold"),
    fg_color="#e74c3c",
    bg_color="#000001",
    hover_color="#c0392b",
    text_color="white",
    width=100,
    corner_radius=12,
    command=on_win_reset,
)
pywinstyles.set_opacity(time_reset_btn, color="#000001")
time_reset_btn.pack(side="left", padx=10)

time_back_btn = ctk.CTkButton(
    time_overlay,
    text="← Back",
    font=("Arial", 14, "bold"),
    fg_color="#e67e22",
    bg_color="#000001",
    hover_color="#d35400",
    text_color="white",
    width=100,
    corner_radius=12,
    command=on_win_back,
)
pywinstyles.set_opacity(time_back_btn, color="#000001")
time_back_btn.pack(side="right", padx=10)

# --- Placeholder back image ---
back_image = ImageTk.PhotoImage(Image.new("RGB", (120, 120), color="gray"))

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
    global first_card, second_card, score, flips
    if card_images[first_card] == card_images[second_card]:
        flipped_cards.extend([first_card, second_card])
        score += 5
        score_label.config(text=f"Score: {score}")
    else:
        flips += 1
        flips_label.config(text=f"Flips: {flips}/{flip_limit}")
        buttons[first_card].config(image=back_image)
        buttons[second_card].config(image=back_image)
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

    cancel_timer()
    if clap_sound:
        clap_sound.stop()
    if lose_sound:
        lose_sound.stop()
    play_music()

    grid_size = size
    px = (120, 120) if size == 4 else (80, 80) if size == 6 else (60, 60)
    needed = 8 if size == 4 else 18 if size == 6 else 32

    back_image = ImageTk.PhotoImage(Image.new("RGB", px, color="gray"))

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

    score_label.config(text="Score: 0")
    flips_label.config(text=f"Flips: 0/{flip_limit}")
    timer_label.config(text=f"Time: {time_limit}s")
    result_label.config(text="")
    result_label.lower()
    win_overlay.lower()
    pause_overlay.lower()
    pause_btn.configure(text="⏸ Pause", fg_color="#3498db")
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
    font=("Comic Sans MS", 24, "bold"),
    fg_color="#FF7F7F",
    bg_color="#000001",
    text_color="white",
    hover_color="#28a75a",
    width=13 * 11,
    height=50,
    corner_radius=20,
    command=lambda: go_to(themes_frame),
)
pywinstyles.set_opacity(start_btn, color="#000001")
start_btn.place(x=600, y=400)

howto_btn = ctk.CTkButton(
    home_frame,
    text="HOW TO PLAY",
    font=("Comic Sans MS", 24, "bold"),
    fg_color="#FF7F7F",
    bg_color="#000001",
    text_color="white",
    hover_color="#28a75a",
    width=13 * 11,
    height=50,
    corner_radius=20,
    command=lambda: go_to(howto_frame),
)
pywinstyles.set_opacity(howto_btn, color="#000001")
howto_btn.place(x=600, y=490)

exit_btn = ctk.CTkButton(
    home_frame,
    text="EXIT",
    font=("Comic Sans MS", 24, "bold"),
    fg_color="#FF7F7F",
    bg_color="#000001",
    text_color="white",
    hover_color="#28a75a",
    width=13 * 11,
    height=50,
    corner_radius=20,
    command=lambda: go_to(exit_app()),
)
pywinstyles.set_opacity(exit_btn, color="#000001")
exit_btn.place(x=600, y=580)


def make_theme_btn(parent, text, y, cmd):
    b = ctk.CTkButton(
        parent,
        text=text,
        font=("Arial", 19, "bold"),
        fg_color="#FF7F7F",
        bg_color="#000001",
        text_color="White",
        hover_color="darkorange1",
        width=13 * 10,
        height=3 * 20,
        corner_radius=18,
        command=cmd,
    )
    pywinstyles.set_opacity(b, color="#000001")
    b.place(y=y, anchor="center")
    return b


naruto_theme_btn = make_theme_btn(
    themes_frame, "Naruto", 180, lambda: go_to(naruto_frame)
)
naruto_theme_btn.place(x=130, y=330)
onepiece_theme_btn = make_theme_btn(
    themes_frame, "One Piece", 260, lambda: go_to(onepiece_frame)
)
onepiece_theme_btn.place(x=980, y=330)
slamdunk_theme_btn = make_theme_btn(
    themes_frame, "Slam Dunk", 340, lambda: go_to(slamdunk_frame)
)
slamdunk_theme_btn.place(x=400, y=330)
db_theme_btn = make_theme_btn(
    themes_frame, "Dragon Ball", 420, lambda: go_to(dragonball_frame)
)
db_theme_btn.place(x=1250, y=330)
bleach_theme_btn = make_theme_btn(
    themes_frame, "Bleach", 500, lambda: go_to(bleach_frame)
)
bleach_theme_btn.place(x=690, y=330)

# --- HOW TO PLAY FRAME ---
# --- HOW TO PLAY FRAME ---
howto_frame = tk.Frame(root, bg="black")
set_bg(howto_frame, "howtoplaybg.png")  # optional anime-themed background
howto_frame.place(relwidth=1, relheight=1)
home_frame.lift()  # ensure home screen shows first

# --- STYLED TITLE ---
title_label = tk.Label(
    howto_frame,
    text="HOW TO PLAY",
    font=("Impact", 17, "bold"),  # anime-style bold font
    fg="#FFD700",  # gold color
    bg="black",
)
title_label.pack(pady=(60, 5))  # spacing at top

# --- HOW TO PLAY TEXT ---
howto_text = """
Choose a Theme
Pick your favorite anime world — Naruto, One Piece, Slam Dunk, Dragon Ball, or Bleach.
Select a Difficulty
Choose your board size:
4x4 → Easy
6x6 → Medium
8x8 → Hard
Start the Game
Flip two cards to reveal their pictures.
Match all pairs before time runs out!
Scoring
+5 points for every correct match.
Limited flips — don’t waste your turns!
You win when all pairs are matched!
Controls
Pause / Resume – Stop or continue the game.
Reset – Restart the current game.
Back – Return to the theme menu.
Game Over Conditions
Time’s up!
Flip limit reached!
All pairs matched = You Win!
"""

howto_label = tk.Label(
    howto_frame,
    text=howto_text,
    font=("Comic Sans MS", 12, "bold"),  # playful anime-like font
    fg="white",
    bg="black",
    justify="center",
    padx=60,
    pady=20,
)
howto_label.pack(fill="both", expand=False)

# --- BACK BUTTON (styled anime look) ---
howto_back_btn = ctk.CTkButton(
    howto_frame,
    text="← Back",
    font=("Comic Sans MS", 14, "bold"),
    fg_color="#e67e22",
    bg_color="#000001",
    text_color="white",
    hover_color="#ff9f43",
    width=120,
    height=50,
    corner_radius=15,
    command=lambda: go_to(home_frame),
)
pywinstyles.set_opacity(howto_back_btn, color="#000001")
howto_back_btn.place(relx=0.5, rely=0.9, anchor="center")


# --- UPDATE YOUR HOW TO PLAY BUTTON to go here ---
# Find this button in home_frame section and replace its command with this:
# command=lambda: go_to(howto_frame)


# --- Choose-tile UI for each theme (styled tiles + centered back) ---
def make_tile_btn(parent, text, x, y, cmd, bg, abg):
    btn = ctk.CTkButton(
        parent,
        text=text,
        font=("Arial", 18, "bold"),
        fg_color=bg,
        bg_color="#000001",
        text_color="white",
        hover_color=abg,
        width=100,
        height=50,
        corner_radius=15,
        command=cmd,
    )
    pywinstyles.set_opacity(btn, color="#000001")
    btn.place(x=x, y=y)
    return btn


def make_back_btn(parent, text, cmd, bg, abg):
    btn = ctk.CTkButton(
        parent,
        text=text,
        font=("Arial", 18, "bold"),
        fg_color=bg,
        bg_color="#000001",
        text_color="white",
        hover_color=abg,
        width=140,
        height=50,
        corner_radius=15,
        command=cmd,
    )
    pywinstyles.set_opacity(btn, color="#000001")
    btn.place(relx=0.5, rely=0.85, anchor="center")
    return btn


# Naruto choose tiles
make_tile_btn(
    naruto_frame, "4x4", 200, 345, lambda: go_to_narutogame(4), "#2ecc71", "#27ae60"
)
make_tile_btn(
    naruto_frame, "6x6", 600, 345, lambda: go_to_narutogame(6), "#f1c40f", "#d4ac0d"
)
make_tile_btn(
    naruto_frame, "8x8", 1000, 345, lambda: go_to_narutogame(8), "#9b59b6", "#8e44ad"
)
make_back_btn(naruto_frame, "← Back", lambda: go_to(themes_frame), "#e67e22", "#d35400")

# One Piece choose tiles
make_tile_btn(
    onepiece_frame, "4x4", 200, 345, lambda: go_to_opgame(4), "#2ecc71", "#27ae60"
)
make_tile_btn(
    onepiece_frame, "6x6", 600, 345, lambda: go_to_opgame(6), "#f1c40f", "#d4ac0d"
)
make_tile_btn(
    onepiece_frame, "8x8", 1000, 345, lambda: go_to_opgame(8), "#9b59b6", "#8e44ad"
)
make_back_btn(
    onepiece_frame, "← Back", lambda: go_to(themes_frame), "#e67e22", "#d35400"
)

# Slam Dunk choose tiles
make_tile_btn(
    slamdunk_frame, "4x4", 200, 345, lambda: go_to_slamgame(4), "#2ecc71", "#27ae60"
)
make_tile_btn(
    slamdunk_frame, "6x6", 600, 345, lambda: go_to_slamgame(6), "#f1c40f", "#d4ac0d"
)
make_tile_btn(
    slamdunk_frame, "8x8", 1000, 345, lambda: go_to_slamgame(8), "#9b59b6", "#8e44ad"
)
make_back_btn(
    slamdunk_frame, "← Back", lambda: go_to(themes_frame), "#e67e22", "#d35400"
)

# Dragon Ball choose tiles
make_tile_btn(
    dragonball_frame, "4x4", 200, 345, lambda: go_to_dbgame(4), "#2ecc71", "#27ae60"
)
make_tile_btn(
    dragonball_frame, "6x6", 600, 345, lambda: go_to_dbgame(6), "#f1c40f", "#d4ac0d"
)
make_tile_btn(
    dragonball_frame, "8x8", 1000, 345, lambda: go_to_dbgame(8), "#9b59b6", "#8e44ad"
)
make_back_btn(
    dragonball_frame, "← Back", lambda: go_to(themes_frame), "#e67e22", "#d35400"
)

# Bleach choose tiles
make_tile_btn(
    bleach_frame, "4x4", 200, 345, lambda: go_to_bleachgame(4), "#2ecc71", "#27ae60"
)
make_tile_btn(
    bleach_frame, "6x6", 600, 345, lambda: go_to_bleachgame(6), "#f1c40f", "#d4ac0d"
)
make_tile_btn(
    bleach_frame, "8x8", 1000, 345, lambda: go_to_bleachgame(8), "#9b59b6", "#8e44ad"
)
make_back_btn(bleach_frame, "← Back", lambda: go_to(themes_frame), "#e67e22", "#d35400")

# --- Ensure theme selection also has a visible Back to Themes button on each theme main (optional) ---
themes_home_btn = ctk.CTkButton(
    themes_frame,
    text="Home",
    font=("Arial", 14),
    fg_color="#FF7F7F",
    bg_color="#000001",
    text_color="white",
    hover_color="#ff6060",
    corner_radius=12,
    width=80,
    height=35,
    command=lambda: go_to(home_frame),
)
pywinstyles.set_opacity(themes_home_btn, color="#000001")
themes_home_btn.place(relx=0.02, rely=0.02, anchor="nw")

# --- Start the app ---
root.mainloop()
