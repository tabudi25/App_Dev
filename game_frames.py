# Game frame setup for each theme
import tkinter as tk
import customtkinter as ctk
import pywinstyles
from constants import COLOR_BG_PANEL, COLOR_PANEL_ACCENT, COLOR_SCORE_BORDER, COLOR_FLIPS_BORDER, COLOR_TIME_BORDER
from audio import load_sound_effects

FONT_NAMES = "Arial"

def create_game_frame(parent, font_name, theme_name):
    """Create a game frame for a specific theme"""
    game_frame = tk.Frame(parent, bg=COLOR_BG_PANEL)
    game_frame.place(relwidth=0, relheight=0)
    game_frame.lower()
    
    # Set background based on theme
    from ui_components import set_bg
    bg_images = {
        "naruto": "narutogamebg.png",
        "op": "opgamebg1.png",
        "slam": "slamdunkgamebg.png",
        "db": "dbgamebg.png",
        "bleach": "bleachgamebg.png"
    }
    bg_image = bg_images.get(theme_name, "narutogamebg.png")
    set_bg(game_frame, bg_image)
    
    # === GAME FRAME LAYOUT ===
    game_frame.grid_rowconfigure(1, weight=1)
    game_frame.grid_columnconfigure(0, weight=1)
    
    
    # === SCORE PANEL ===
    score_panel = tk.Frame(
        game_frame, bg=COLOR_BG_PANEL, relief="ridge", bd=5,
        highlightbackground=COLOR_SCORE_BORDER, highlightthickness=3
    )
    score_panel.place(x=990, y=10)
    score_label = tk.Label(
        score_panel, text="Score: 0", font=(FONT_NAMES, 18, "bold"),
        fg="white", bg=COLOR_BG_PANEL
    )
    score_label.pack(side="left", padx=(6, 12))
    
    # === FLIPS & TIMER LABELS ===
    flips_panel = tk.Frame(
        game_frame, bg=COLOR_BG_PANEL, relief="ridge", bd=5,
        highlightbackground=COLOR_FLIPS_BORDER, highlightthickness=3
    )
    flips_panel.place(x=1130, y=10)
    flips_label = tk.Label(
        flips_panel, text="Flips: 0/20", font=(FONT_NAMES, 18, "bold"),
        fg="white", bg=COLOR_BG_PANEL
    )
    flips_label.pack(side="left", padx=(6, 12))
    
    timer_panel = tk.Frame(
        game_frame, bg=COLOR_BG_PANEL, relief="ridge", bd=5,
        highlightbackground=COLOR_TIME_BORDER, highlightthickness=3
    )
    timer_panel.place(x=1295, y=10)
    timer_label = tk.Label(
        timer_panel, text="Time: 60s", font=(FONT_NAMES, 18, "bold"),
        fg="white", bg=COLOR_BG_PANEL
    )
    timer_label.pack(side="left", padx=(6, 12))
    
    # === PAUSE MENU BOX ===
    pause_menu_box = tk.Frame(game_frame, bg="black", bd=4, relief="ridge")
    pause_menu_box.place(relx=0.5, rely=0.5, anchor="center", width=450, height=500)
    pause_menu_box.lower()
    
    pause_menu_title = tk.Label(
        pause_menu_box, text="Game Paused", font=(FONT_NAMES, 32, "bold"),
        fg="white", bg="black"
    )
    pause_menu_title.pack(pady=(30, 20))
    
    pause_menu_buttons = tk.Frame(pause_menu_box, bg="black")
    pause_menu_buttons.pack(pady=20)
    
    # === MENU ICON BUTTON ===
    menu_icon_btn = ctk.CTkButton(
        game_frame, text="☰", fg_color="#787c82", bg_color="transparent",
        hover_color="#3c434a", text_color="white", font=(FONT_NAMES, 32, "bold"),
        width=60, height=60, corner_radius=15, border_width=2,
        border_color="white", command=lambda: on_menu_click(pause_menu_box, game_frame)
    )
    pywinstyles.set_opacity(menu_icon_btn, color=COLOR_BG_PANEL)
    menu_icon_btn.place(relx=0.01, rely=0.01, anchor="nw")
    
    def on_menu_icon_enter(event):
        menu_icon_btn.configure(text_color="white")
        menu_icon_btn.configure(fg_color="#3c434a")
        menu_icon_btn.configure(border_color="white")
    
    def on_menu_icon_leave(event):
        menu_icon_btn.configure(text_color="white")
        menu_icon_btn.configure(fg_color="#787c82")
        menu_icon_btn.configure(border_color="white")
    
    menu_icon_btn.bind("<Enter>", on_menu_icon_enter)
    menu_icon_btn.bind("<Leave>", on_menu_icon_leave)
    
    # === BOARD FRAME ===
    board_frame = tk.Frame(game_frame, bg=COLOR_BG_PANEL)
    board_frame.place(relx=0.5, rely=0.45, anchor="center")
    pywinstyles.set_opacity(board_frame, color=COLOR_BG_PANEL)
    
    # === RESULT LABEL ===
    result_label = tk.Label(
        game_frame, text="", font=(FONT_NAMES, 40, "bold"),
        fg="yellow", bg="black"
    )
    result_label.place(relx=0.5, rely=0.5, anchor="center")
    result_label.lower()
    
    # === WIN OVERLAY BOX ===
    win_overlay = tk.Frame(game_frame, bg="black", bd=4, relief="ridge")
    win_overlay.place(relx=0.5, rely=0.5, anchor="center", width=400, height=250)
    win_overlay.lower()
    
    win_msg = tk.Label(
        win_overlay, text="You Win!", font=(FONT_NAMES, 28, "bold"),
        fg="lime", bg="black"
    )
    win_msg.pack(pady=(15, 5))
    win_stats = tk.Label(
        win_overlay, text="", font=(FONT_NAMES, 16, "bold"),
        fg="white", bg="black"
    )
    win_stats.pack(pady=10)
    
    # === FLIP OVERLAY BOX ===
    flip_overlay = tk.Frame(game_frame, bg="black", bd=4, relief="ridge")
    flip_overlay.place(relx=0.5, rely=0.5, anchor="center", width=400, height=250)
    flip_overlay.lower()
    
    flip_msg = tk.Label(
        flip_overlay, text="Flip Limit Reached!", font=(FONT_NAMES, 24, "bold"),
        fg="red", bg="black"
    )
    flip_msg.pack(pady=(15, 5))
    flip_stats = tk.Label(
        flip_overlay, text="", font=(FONT_NAMES, 16, "bold"),
        fg="white", bg="black"
    )
    flip_stats.pack(pady=10)
    
    # === TIME OVERLAY BOX ===
    time_overlay = tk.Frame(game_frame, bg="black", bd=4, relief="ridge")
    time_overlay.place(relx=0.5, rely=0.5, anchor="center", width=400, height=250)
    time_overlay.lower()
    
    time_msg = tk.Label(
        time_overlay, text="Time's Up!", font=(FONT_NAMES, 24, "bold"),
        fg="red", bg="black"
    )
    time_msg.pack(pady=(15, 5))
    time_stats = tk.Label(
        time_overlay, text="", font=(FONT_NAMES, 16, "bold"),
        fg="white", bg="black"
    )
    time_stats.pack(pady=10)
    
    # Load sound effects
    clap_sound, lose_sound = load_sound_effects()
    
    # Create pause menu buttons
    from navigation import get_current_theme
    from game_logic import reset_game, update_timer, grid_size
    from audio import play_music, stop_music
    from audio import stop_music as stop_music_func
    
    def on_menu_resume():
        """Resume the game from menu"""
        import game_logic
        game_logic.paused = False
        game_logic.timer_running = True
        pause_menu_box.lower()
        play_music(get_current_theme())
        update_timer()
    
    def on_menu_reset():
        """Reset game from menu"""
        pause_menu_box.lower()
        reset_game(grid_size, theme=get_current_theme())
    
    def on_menu_back():
        """Go back to themes from menu"""
        pause_menu_box.lower()
        from navigation import back_to_themes, get_themes_frame
        themes_frame = get_themes_frame()
        back_to_themes(
            game_frame=game_frame, themes_frame=themes_frame,
            result_label=result_label, win_overlay=win_overlay,
            flip_overlay=flip_overlay, time_overlay=time_overlay,
            pause_menu_box=pause_menu_box, clap_sound=clap_sound, lose_sound=lose_sound
        )
    
    def on_menu_change_grid():
        """Navigate back to theme selection to choose a different grid size"""
        from navigation import go_to_theme_selection
        from game_logic import cancel_timer
        import game_logic
        
        pause_menu_box.lower()
        cancel_timer()
        game_logic.paused = False
        game_logic.timer_running = False
        
        # Lower the game frame
        game_frame.lower()
        
        # Navigate to theme selection screen
        go_to_theme_selection()
    
    menu_resume_btn = ctk.CTkButton(
        pause_menu_buttons, text="Resume", font=(FONT_NAMES, 18, "bold"),
        fg_color="#787c82", bg_color="black", hover_color="#FF5252",
        text_color="black", width=180, height=60, corner_radius=15,
        border_width=2, border_color="white", command=on_menu_resume
    )
    
    def on_menu_resume_enter(event):
        menu_resume_btn.configure(text_color="white")
        menu_resume_btn.configure(fg_color="black")
        menu_resume_btn.configure(border_color="white")
    
    def on_menu_resume_leave(event):
        menu_resume_btn.configure(text_color="black")
        menu_resume_btn.configure(fg_color="#787c82")
        menu_resume_btn.configure(border_color="white")
    
    menu_resume_btn.bind("<Enter>", on_menu_resume_enter)
    menu_resume_btn.bind("<Leave>", on_menu_resume_leave)
    menu_resume_btn.pack(pady=10)
    
    menu_reset_btn = ctk.CTkButton(
        pause_menu_buttons, text="Reset", font=(FONT_NAMES, 18, "bold"),
        fg_color="#787c82", bg_color="black", hover_color="#FF5252",
        text_color="black", width=180, height=60, corner_radius=15,
        border_width=2, border_color="white", command=on_menu_reset
    )
    
    def on_menu_reset_enter(event):
        menu_reset_btn.configure(text_color="white")
        menu_reset_btn.configure(fg_color="black")
        menu_reset_btn.configure(border_color="white")
    
    def on_menu_reset_leave(event):
        menu_reset_btn.configure(text_color="black")
        menu_reset_btn.configure(fg_color="#787c82")
        menu_reset_btn.configure(border_color="white")
    
    menu_reset_btn.bind("<Enter>", on_menu_reset_enter)
    menu_reset_btn.bind("<Leave>", on_menu_reset_leave)
    menu_reset_btn.pack(pady=10)
    
    menu_back_btn = ctk.CTkButton(
        pause_menu_buttons, text="Back", font=(FONT_NAMES, 18, "bold"),
        fg_color="#787c82", bg_color="black", hover_color="#FF5252",
        text_color="black", width=180, height=60, corner_radius=15,
        border_width=2, border_color="white", command=on_menu_back
    )
    
    def on_menu_back_enter(event):
        menu_back_btn.configure(text_color="white")
        menu_back_btn.configure(fg_color="black")
        menu_back_btn.configure(border_color="white")
    
    def on_menu_back_leave(event):
        menu_back_btn.configure(text_color="black")
        menu_back_btn.configure(fg_color="#787c82")
        menu_back_btn.configure(border_color="white")
    
    menu_back_btn.bind("<Enter>", on_menu_back_enter)
    menu_back_btn.bind("<Leave>", on_menu_back_leave)
    menu_back_btn.pack(pady=10)
    
    menu_change_grid_btn = ctk.CTkButton(
        pause_menu_buttons, text="Change grid", font=(FONT_NAMES, 18, "bold"),
        fg_color="#787c82", bg_color="black", hover_color="#FF5252",
        text_color="black", width=180, height=60, corner_radius=15,
        border_width=2, border_color="white", command=on_menu_change_grid
    )
    
    def on_menu_change_grid_enter(event):
        menu_change_grid_btn.configure(text_color="white")
        menu_change_grid_btn.configure(fg_color="black")
        menu_change_grid_btn.configure(border_color="white")
    
    def on_menu_change_grid_leave(event):
        menu_change_grid_btn.configure(text_color="black")
        menu_change_grid_btn.configure(fg_color="#787c82")
        menu_change_grid_btn.configure(border_color="white")
    
    menu_change_grid_btn.bind("<Enter>", on_menu_change_grid_enter)
    menu_change_grid_btn.bind("<Leave>", on_menu_change_grid_leave)
    menu_change_grid_btn.pack(pady=10)
    
    # Create overlay buttons
    def on_win_reset():
        win_overlay.lower()
        reset_game(grid_size, theme=get_current_theme())
    
    def on_win_back():
        win_overlay.lower()
        from navigation import back_to_themes, get_themes_frame
        themes_frame = get_themes_frame()
        back_to_themes(
            game_frame=game_frame, themes_frame=themes_frame,
            result_label=result_label, win_overlay=win_overlay,
            flip_overlay=flip_overlay, time_overlay=time_overlay,
            pause_menu_box=pause_menu_box, clap_sound=clap_sound, lose_sound=lose_sound
        )
    
    def on_flip_reset():
        flip_overlay.lower()
        reset_game(grid_size, theme=get_current_theme())
    
    def on_flip_back():
        flip_overlay.lower()
        from navigation import back_to_themes, get_themes_frame
        themes_frame = get_themes_frame()
        back_to_themes(
            game_frame=game_frame, themes_frame=themes_frame,
            result_label=result_label, win_overlay=win_overlay,
            flip_overlay=flip_overlay, time_overlay=time_overlay,
            pause_menu_box=pause_menu_box, clap_sound=clap_sound, lose_sound=lose_sound
        )
    
    def on_time_reset():
        time_overlay.lower()
        reset_game(grid_size, theme=get_current_theme())
    
    def on_time_back():
        time_overlay.lower()
        from navigation import back_to_themes, get_themes_frame
        themes_frame = get_themes_frame()
        back_to_themes(
            game_frame=game_frame, themes_frame=themes_frame,
            result_label=result_label, win_overlay=win_overlay,
            flip_overlay=flip_overlay, time_overlay=time_overlay,
            pause_menu_box=pause_menu_box, clap_sound=clap_sound, lose_sound=lose_sound
        )
    
    win_btns = tk.Frame(win_overlay, bg="black")
    win_btns.pack(side="bottom", pady=15)
    
    win_reset_btn = ctk.CTkButton(
        win_btns, text="Reset", font=(FONT_NAMES, 14, "bold"),
        fg_color="#787c82", bg_color="#000001", hover_color="#FF5252",
        text_color="black", width=100, corner_radius=12, border_width=2,
        border_color="white", command=on_win_reset
    )
    
    def on_win_reset_enter(event):
        win_reset_btn.configure(text_color="white")
        win_reset_btn.configure(fg_color="black")
        win_reset_btn.configure(border_color="white")
    
    def on_win_reset_leave(event):
        win_reset_btn.configure(text_color="black")
        win_reset_btn.configure(fg_color="#787c82")
        win_reset_btn.configure(border_color="white")
    
    win_reset_btn.bind("<Enter>", on_win_reset_enter)
    win_reset_btn.bind("<Leave>", on_win_reset_leave)
    pywinstyles.set_opacity(win_reset_btn, color="#000001")
    win_reset_btn.pack(side="left", padx=10)
    
    win_back_btn = ctk.CTkButton(
        win_btns, text="Back", font=(FONT_NAMES, 14, "bold"),
        fg_color="#787c82", bg_color="#000001", hover_color="#FF5252",
        text_color="black", width=100, corner_radius=12, border_width=2,
        border_color="white", command=on_win_back
    )
    
    def on_win_back_enter(event):
        win_back_btn.configure(text_color="white")
        win_back_btn.configure(fg_color="black")
        win_back_btn.configure(border_color="white")
    
    def on_win_back_leave(event):
        win_back_btn.configure(text_color="black")
        win_back_btn.configure(fg_color="#787c82")
        win_back_btn.configure(border_color="white")
    
    win_back_btn.bind("<Enter>", on_win_back_enter)
    win_back_btn.bind("<Leave>", on_win_back_leave)
    pywinstyles.set_opacity(win_back_btn, color="#000001")
    win_back_btn.pack(side="right", padx=10)
    
    flip_reset_btn = ctk.CTkButton(
        flip_overlay, text="⟳ Reset", font=(FONT_NAMES, 14, "bold"),
        fg_color="#787c82", bg_color="#000001", hover_color="#FF5252",
        text_color="black", width=100, corner_radius=12, border_width=2,
        border_color="white", command=on_flip_reset
    )
    
    def on_flip_reset_enter(event):
        flip_reset_btn.configure(text_color="white")
        flip_reset_btn.configure(fg_color="black")
        flip_reset_btn.configure(border_color="white")
    
    def on_flip_reset_leave(event):
        flip_reset_btn.configure(text_color="black")
        flip_reset_btn.configure(fg_color="#787c82")
        flip_reset_btn.configure(border_color="white")
    
    flip_reset_btn.bind("<Enter>", on_flip_reset_enter)
    flip_reset_btn.bind("<Leave>", on_flip_reset_leave)
    pywinstyles.set_opacity(flip_reset_btn, color="#000001")
    flip_reset_btn.pack(side="left", padx=10)
    
    flip_back_btn = ctk.CTkButton(
        flip_overlay, text="Back", font=(FONT_NAMES, 14, "bold"),
        fg_color="#787c82", bg_color="#000001", hover_color="#FF5252",
        text_color="black", width=100, corner_radius=12, border_width=2,
        border_color="white", command=on_flip_back
    )
    
    def on_flip_back_enter(event):
        flip_back_btn.configure(text_color="white")
        flip_back_btn.configure(fg_color="black")
        flip_back_btn.configure(border_color="white")
    
    def on_flip_back_leave(event):
        flip_back_btn.configure(text_color="black")
        flip_back_btn.configure(fg_color="#787c82")
        flip_back_btn.configure(border_color="white")
    
    flip_back_btn.bind("<Enter>", on_flip_back_enter)
    flip_back_btn.bind("<Leave>", on_flip_back_leave)
    pywinstyles.set_opacity(flip_back_btn, color="#000001")
    flip_back_btn.pack(side="right", padx=10)
    
    time_reset_btn = ctk.CTkButton(
        time_overlay, text="⟳ Reset", font=(FONT_NAMES, 14, "bold"),
        fg_color="#787c82", bg_color="#000001", hover_color="#FF5252",
        text_color="black", width=100, corner_radius=12, border_width=2,
        border_color="white", command=on_time_reset
    )
    
    def on_time_reset_enter(event):
        time_reset_btn.configure(text_color="white")
        time_reset_btn.configure(fg_color="black")
        time_reset_btn.configure(border_color="white")
    
    def on_time_reset_leave(event):
        time_reset_btn.configure(text_color="black")
        time_reset_btn.configure(fg_color="#787c82")
        time_reset_btn.configure(border_color="white")
    
    time_reset_btn.bind("<Enter>", on_time_reset_enter)
    time_reset_btn.bind("<Leave>", on_time_reset_leave)
    pywinstyles.set_opacity(time_reset_btn, color="#000001")
    time_reset_btn.pack(side="left", padx=10)
    
    time_back_btn = ctk.CTkButton(
        time_overlay, text="Back", font=(FONT_NAMES, 14, "bold"),
        fg_color="#787c82", bg_color="#000001", hover_color="#FF5252",
        text_color="black", width=100, corner_radius=12, border_width=2,
        border_color="white", command=on_time_back
    )
    
    def on_time_back_enter(event):
        time_back_btn.configure(text_color="white")
        time_back_btn.configure(fg_color="black")
        time_back_btn.configure(border_color="white")
    
    def on_time_back_leave(event):
        time_back_btn.configure(text_color="black")
        time_back_btn.configure(fg_color="#787c82")
        time_back_btn.configure(border_color="white")
    
    time_back_btn.bind("<Enter>", on_time_back_enter)
    time_back_btn.bind("<Leave>", on_time_back_leave)
    pywinstyles.set_opacity(time_back_btn, color="#000001")
    time_back_btn.pack(side="right", padx=10)
    
    # Return the game frame and all its components
    return {
        'game_frame': game_frame,
        'score_label': score_label,
        'flips_label': flips_label,
        'timer_label': timer_label,
        'result_label': result_label,
        'win_overlay': win_overlay,
        'flip_overlay': flip_overlay,
        'time_overlay': time_overlay,
        'win_stats': win_stats,
        'flip_stats': flip_stats,
        'time_stats': time_stats,
        'board_frame': board_frame,
        'pause_menu_box': pause_menu_box,
        'clap_sound': clap_sound,
        'lose_sound': lose_sound
    }


def on_menu_click(pause_menu_box, game_frame):
    """Open pause menu and pause the game"""
    import game_logic
    from audio import stop_music
    if not game_logic.paused:
        game_logic.paused = True
        game_logic.timer_running = False
        stop_music()
        pause_menu_box.lift()

