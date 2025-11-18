# Core game logic for the memory game
import random
import os
from PIL import Image, ImageTk
import tkinter as tk

# Game state variables (will be initialized in main)
card_size = (120, 120)
time_limit = 60
flip_limit = 20
points_per_match = 5
first_card = None
second_card = None
buttons = []
flipped_cards = []
card_images = []
card_pil_images = []
card_pair_ids = []
score = 0
flips = 0
time_left = 60
timer_running = True
timer_id = None
grid_size = 4
paused = False
consecutive_failed_flips = 0
hint_shown = False
hint_timer = None

# UI references (will be set from main)
score_label = None
flips_label = None
timer_label = None
result_label = None
win_overlay = None
flip_overlay = None
time_overlay = None
win_stats = None
flip_stats = None
time_stats = None
board_frame = None
root = None
back_image = None
back_pil_image = None
clap_sound = None
lose_sound = None

# Store all game frame references
game_frames_dict = {}


def initialize_game_state(ui_refs, game_root):
    """Initialize game state with UI references"""
    global score_label, flips_label, timer_label, result_label
    global win_overlay, flip_overlay, time_overlay
    global win_stats, flip_stats, time_stats, board_frame, root
    global clap_sound, lose_sound, game_frames_dict
    
    score_label = ui_refs.get('score_label')
    flips_label = ui_refs.get('flips_label')
    timer_label = ui_refs.get('timer_label')
    result_label = ui_refs.get('result_label')
    win_overlay = ui_refs.get('win_overlay')
    flip_overlay = ui_refs.get('flip_overlay')
    time_overlay = ui_refs.get('time_overlay')
    win_stats = ui_refs.get('win_stats')
    flip_stats = ui_refs.get('flip_stats')
    time_stats = ui_refs.get('time_stats')
    board_frame = ui_refs.get('board_frame')
    root = game_root
    clap_sound = ui_refs.get('clap_sound')
    lose_sound = ui_refs.get('lose_sound')


def register_game_frame(theme, ui_refs):
    """Register a game frame for a specific theme"""
    global game_frames_dict
    game_frames_dict[theme] = ui_refs


def switch_game_frame(theme):
    """Switch to a different game frame based on theme"""
    global score_label, flips_label, timer_label, result_label
    global win_overlay, flip_overlay, time_overlay
    global win_stats, flip_stats, time_stats, board_frame
    global clap_sound, lose_sound
    
    if theme in game_frames_dict:
        ui_refs = game_frames_dict[theme]
        score_label = ui_refs.get('score_label')
        flips_label = ui_refs.get('flips_label')
        timer_label = ui_refs.get('timer_label')
        result_label = ui_refs.get('result_label')
        win_overlay = ui_refs.get('win_overlay')
        flip_overlay = ui_refs.get('flip_overlay')
        time_overlay = ui_refs.get('time_overlay')
        win_stats = ui_refs.get('win_stats')
        flip_stats = ui_refs.get('flip_stats')
        time_stats = ui_refs.get('time_stats')
        board_frame = ui_refs.get('board_frame')
        clap_sound = ui_refs.get('clap_sound')
        lose_sound = ui_refs.get('lose_sound')


def load_back_image(size=(120, 120), theme="naruto"):
    """Load card back image based on theme, or create gray placeholder if not found"""
    global back_image, back_pil_image
    
    # Map theme names to cover image filenames
    theme_cover_map = {
        "naruto": "narutocover.jpeg",
        "op": "onepiececover.jpeg",
        "slam": "slamdunkcover.jpeg",
        "db": "dragonballcover.jpeg",
        "bleach": "bleachcover.jpeg"
    }
    
    cover_filename = theme_cover_map.get(theme, "narutocover.jpeg")
    
    if os.path.exists(cover_filename):
        try:
            pil_img = Image.open(cover_filename).resize(size, Image.Resampling.LANCZOS)
            back_image = ImageTk.PhotoImage(pil_img)
            back_pil_image = pil_img.copy()
            return back_image, back_pil_image
        except Exception:
            pass
    
    # Fallback to gray placeholder if image not found
    pil_img = Image.new("RGB", size, color="gray")
    back_image = ImageTk.PhotoImage(pil_img)
    back_pil_image = pil_img.copy()
    return back_image, back_pil_image


def load_theme_images(paths, needed, size):
    """Load theme images safely"""
    from constants import THEME_IMAGES
    imgs = []
    pil_imgs = []
    for p in paths:
        if os.path.exists(p):
            try:
                pil_img = Image.open(p).resize(size, Image.Resampling.LANCZOS)
                pil_imgs.append(pil_img.copy())
                imgs.append(ImageTk.PhotoImage(pil_img))
            except Exception:
                pass
    while len(imgs) < needed:
        k = len(imgs)
        r, g, b = (k * 73) % 256, (k * 37) % 256, (k * 151) % 256
        pil_img = Image.new("RGB", size, (r, g, b))
        pil_imgs.append(pil_img.copy())
        imgs.append(ImageTk.PhotoImage(pil_img))
    return imgs[:needed], pil_imgs[:needed]


def update_timer():
    """Update the game timer"""
    global time_left, timer_id, timer_running, paused, timer_label
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
    """Cancel the timer"""
    global timer_id
    if timer_id:
        try:
            root.after_cancel(timer_id)
        except Exception:
            pass
        timer_id = None


def cancel_hint_timer():
    """Cancel the hint timer"""
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
        else:
            # Ensure matched cards stay showing their images
            btn.config(image=card_images[i])
            btn.image = card_images[i]


def create_squished_image(pil_image, scale_factor):
    """Create a horizontally squished version of a PIL image to simulate 3D flip"""
    try:
        orig_width, orig_height = pil_image.size
        new_width = max(1, int(orig_width * scale_factor))
        new_height = orig_height
        
        # Resize the image horizontally to create squish effect
        squished = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(squished)
    except Exception:
        # Fallback: return original image converted to PhotoImage
        return ImageTk.PhotoImage(pil_image)


def animate_card_flip(button, target_pil_image, target_photo_image, source_pil_image=None, callback=None):
    """Animate a card flip by creating intermediate squished images"""
    steps = 10
    current_step = [0]
    
    # Determine current PIL image
    if source_pil_image is not None:
        current_pil = source_pil_image
    else:
        current_pil = back_pil_image
    
    def flip_step():
        step = current_step[0]
        progress = step / steps
        
        if step < steps // 2:
            # First half: shrink width (flip away)
            scale = 1.0 - (progress * 2)
            squished = create_squished_image(current_pil, scale)
            button.config(image=squished)
            button.image = squished
            current_step[0] += 1
            root.after(20, flip_step)
        elif step == steps // 2:
            # At midpoint, show narrowest and switch to target image
            scale = 0.0
            squished = create_squished_image(target_pil_image, scale)
            button.config(image=squished)
            button.image = squished
            current_step[0] += 1
            root.after(20, flip_step)
        else:
            # Second half: expand width (flip in)
            scale = ((step - steps // 2) / (steps - steps // 2))
            squished = create_squished_image(target_pil_image, scale)
            button.config(image=squished)
            button.image = squished
            current_step[0] += 1
            if step < steps - 1:
                root.after(20, flip_step)
            else:
                # Final state: show full target image
                button.config(image=target_photo_image)
                button.image = target_photo_image
                if callback:
                    callback()
    
    flip_step()


def on_card_click(idx):
    """Handle card click event"""
    global first_card, second_card, flips
    if paused or not timer_running:
        return
    if idx in flipped_cards or idx == first_card:
        return

    # Animate the flip
    def after_flip():
        global first_card, second_card
        if first_card is None:
            first_card = idx
        elif second_card is None:
            second_card = idx
            # Wait a bit then check match
            root.after(350, check_match)

    # Start the flip animation
    animate_card_flip(buttons[idx], card_pil_images[idx], card_images[idx], callback=after_flip)


def check_match():
    """Check if two flipped cards match. Add points if match, flip back if no match."""
    global first_card, second_card, score, flips, consecutive_failed_flips, points_per_match
    
    # Safety check - ensure both cards are selected
    if first_card is None or second_card is None:
        return
    
    # Store card indices
    card1_idx = first_card
    card2_idx = second_card
    
    # Check if cards match by comparing the actual images
    if card_images[card1_idx] == card_images[card2_idx]:
        # CARDS MATCH - Keep flipped, add points
        flipped_cards.extend([card1_idx, card2_idx])
        score += points_per_match
        score_label.config(text=f"Score: {score}")
        consecutive_failed_flips = 0
        
        # Ensure cards stay showing their images
        buttons[card1_idx].config(image=card_images[card1_idx])
        buttons[card1_idx].image = card_images[card1_idx]
        buttons[card2_idx].config(image=card_images[card2_idx])
        buttons[card2_idx].image = card_images[card2_idx]
        
        # Reset selection variables
        first_card = None
        second_card = None
        
        # Check if game is won
        if len(flipped_cards) == len(card_images):
            game_over("You win!")
    else:
        # CARDS DON'T MATCH - Flip back, count flip
        flips += 1
        consecutive_failed_flips += 1
        flips_label.config(text=f"Flips: {flips}/{flip_limit}")
        
        # Check if flip limit reached
        if flips >= flip_limit and len(flipped_cards) != len(card_images):
            game_over("Flip limit reached! You lose.")
            return
        
        # Animate flipping cards back to back image
        def flip_back_complete():
            global first_card, second_card
            first_card = None
            second_card = None
            
            # Show hint after 5 consecutive failed flips
            if consecutive_failed_flips >= 5:
                root.after(500, show_hint)
        
        # Track when both cards finish flipping back
        cards_flipped_back = [False, False]
        
        def check_both_flipped_back():
            if all(cards_flipped_back):
                flip_back_complete()
        
        def card1_flipped_back():
            cards_flipped_back[0] = True
            check_both_flipped_back()
        
        def card2_flipped_back():
            cards_flipped_back[1] = True
            check_both_flipped_back()
        
        # Animate both cards flipping back
        animate_card_flip(buttons[card1_idx], back_pil_image, back_image, 
                         source_pil_image=card_pil_images[card1_idx], callback=card1_flipped_back)
        animate_card_flip(buttons[card2_idx], back_pil_image, back_image, 
                         source_pil_image=card_pil_images[card2_idx], callback=card2_flipped_back)


def game_over(message):
    """Handle game over state"""
    global timer_running
    from audio import stop_music
    
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
    """Reset the game with new size and theme"""
    global card_images, card_pil_images, card_pair_ids, first_card, second_card, flipped_cards
    global score, flips, time_left, timer_running, buttons, grid_size, back_image, back_pil_image, paused
    global consecutive_failed_flips, hint_shown, hint_timer
    global time_limit, flip_limit, points_per_match
    from constants import THEME_IMAGES
    from audio import play_music, stop_music
    
    # Switch to the correct game frame for this theme
    switch_game_frame(theme)
    
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
        time_limit = 60
        flip_limit = 20
        points_per_match = 5
    elif size == 6:
        time_limit = 90
        flip_limit = 40
        points_per_match = 10
    elif size == 8:
        time_limit = 120
        flip_limit = 50
        points_per_match = 15
    
    px = (120, 120) if size == 4 else (80, 80) if size == 6 else (60, 60)
    needed = 8 if size == 4 else 18 if size == 6 else 32

    # Load card back image with proper size and theme
    back_image, back_pil_image = load_back_image(px, theme)

    for w in board_frame.winfo_children():
        w.destroy()
    buttons.clear()

    paths = THEME_IMAGES.get(theme, {}).get(size, [])
    imgs, pil_imgs = load_theme_images(paths, needed, px)
    card_images = imgs * 2
    card_pil_images = pil_imgs * 2
    # Create pair IDs: each pair of cards gets the same ID (0, 0, 1, 1, 2, 2, ...)
    card_pair_ids = [i // 2 for i in range(len(card_images))]
    
    # Shuffle all three lists together in the same way
    combined = list(zip(card_images, card_pil_images, card_pair_ids))
    random.shuffle(combined)
    card_images, card_pil_images, card_pair_ids = zip(*combined)
    card_images = list(card_images)
    card_pil_images = list(card_pil_images)
    card_pair_ids = list(card_pair_ids)

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
    consecutive_failed_flips = 0
    hint_shown = False

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
    update_timer()

