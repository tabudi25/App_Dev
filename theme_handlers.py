# Theme-specific handlers and GIF loading functions
import os
import tkinter as tk
from PIL import Image, ImageTk

# Global state for GIF transitions
current_gif_label = None
auto_transition_running = False
current_auto_gif = 0
transition_timer = None
root_ref = None


def set_root_reference(root):
    """Set the root window reference for timers"""
    global root_ref
    root_ref = root


def load_gif_into(target_frame, gif_file):
    """Generic loader to display a GIF/image into a specific frame"""
    global current_gif_label
    if os.path.exists(gif_file):
        try:
            if current_gif_label:
                current_gif_label.destroy()
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


def load_4x4_gif(naruto_gif_frame):
    """Load 4x4 GIF for Naruto theme"""
    global current_gif_label
    if os.path.exists("GIF-4x4-naruto.png"):
        try:
            if current_gif_label:
                current_gif_label.destroy()
            pil_img = Image.open("GIF-4x4-naruto.png")
            frame_width, frame_height = 710, 360
            img_width, img_height = pil_img.size
            scale_w = frame_width / img_width
            scale_h = frame_height / img_height
            scale = min(scale_w, scale_h)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(pil_img)
            current_gif_label = tk.Label(naruto_gif_frame, image=img, bg="#8CE4FF")
            current_gif_label.place(relx=0.5, rely=0.5, anchor="center")
            current_gif_label.image = img
        except Exception:
            pass


def load_6x6_gif(naruto_gif_frame):
    """Load 6x6 GIF for Naruto theme"""
    global current_gif_label
    if os.path.exists("GIF-6x6-naruto.png"):
        try:
            if current_gif_label:
                current_gif_label.destroy()
            pil_img = Image.open("GIF-6x6-naruto.png")
            frame_width, frame_height = 760, 360
            img_width, img_height = pil_img.size
            scale_w = frame_width / img_width
            scale_h = frame_height / img_height
            scale = min(scale_w, scale_h)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(pil_img)
            current_gif_label = tk.Label(naruto_gif_frame, image=img, bg="#1A1A2E")
            current_gif_label.place(relx=0.5, rely=0.5, anchor="center")
            current_gif_label.image = img
        except Exception:
            pass


def load_8x8_gif(naruto_gif_frame):
    """Load 8x8 GIF for Naruto theme"""
    global current_gif_label
    if os.path.exists("GIF-8x8-naruto.png"):
        try:
            if current_gif_label:
                current_gif_label.destroy()
            pil_img = Image.open("GIF-8x8-naruto.png")
            frame_width, frame_height = 760, 360
            img_width, img_height = pil_img.size
            scale_w = frame_width / img_width
            scale_h = frame_height / img_height
            scale = min(scale_w, scale_h)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(pil_img)
            current_gif_label = tk.Label(naruto_gif_frame, image=img, bg="#1A1A2E")
            current_gif_label.place(relx=0.5, rely=0.5, anchor="center")
            current_gif_label.image = img
        except Exception:
            pass


def clear_gif():
    """Clear the current GIF"""
    global current_gif_label
    if current_gif_label:
        current_gif_label.destroy()
        current_gif_label = None


# Store current frame and theme for auto transitions
current_auto_frame = None
current_theme_prefix = None
current_bg_color = None

def start_auto_transitions(gif_frame, theme_prefix="naruto", bg_color="#1A1A2E"):
    """Start auto transitions for GIFs - generic version"""
    global auto_transition_running, current_auto_gif, transition_timer, current_auto_frame, current_theme_prefix, current_bg_color
    auto_transition_running = True
    current_auto_gif = 0
    current_auto_frame = gif_frame
    current_theme_prefix = theme_prefix
    current_bg_color = bg_color
    cycle_auto_gifs()


def stop_auto_transitions():
    """Stop auto transitions"""
    global auto_transition_running, transition_timer
    auto_transition_running = False
    if transition_timer and root_ref:
        root_ref.after_cancel(transition_timer)
        transition_timer = None


def cycle_auto_gifs():
    """Cycle through auto GIFs - generic version"""
    global current_auto_gif, auto_transition_running, transition_timer, current_auto_frame, current_theme_prefix, current_bg_color
    if not auto_transition_running or not current_auto_frame:
        return
    
    # Load current auto GIF based on theme prefix
    gif_files = [
        f"GIF-4x4-{current_theme_prefix}.png",
        f"GIF-6x6-{current_theme_prefix}.png",
        f"GIF-8x8-{current_theme_prefix}.png"
    ]
    if current_auto_gif < len(gif_files):
        load_auto_gif(gif_files[current_auto_gif])
        current_auto_gif = (current_auto_gif + 1) % len(gif_files)
    
    # Schedule next transition
    if root_ref:
        transition_timer = root_ref.after(3000, cycle_auto_gifs)


def load_auto_gif(gif_file):
    """Load auto GIF - generic version"""
    global current_gif_label, current_auto_frame, current_bg_color
    if os.path.exists(gif_file) and current_auto_frame:
        try:
            if current_gif_label:
                current_gif_label.destroy()
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
            current_gif_label = tk.Label(current_auto_frame, image=img, bg=current_bg_color)
            current_gif_label.place(relx=0.5, rely=0.5, anchor="center")
            current_gif_label.image = img
        except Exception:
            pass


# Theme-specific GIF loaders
def load_op_4x4_gif(onepiece_gif_frame):
    load_gif_into(onepiece_gif_frame, "GIF-4x4-op.png")


def load_op_6x6_gif(onepiece_gif_frame):
    load_gif_into(onepiece_gif_frame, "GIF-6x6-op.png")


def load_op_8x8_gif(onepiece_gif_frame):
    load_gif_into(onepiece_gif_frame, "GIF-8x8-op.png")


def load_slam_4x4_gif(slamdunk_gif_frame):
    load_gif_into(slamdunk_gif_frame, "GIF-4x4-slamdunk.png")


def load_slam_6x6_gif(slamdunk_gif_frame):
    load_gif_into(slamdunk_gif_frame, "GIF-6x6-slamdunk.png")


def load_slam_8x8_gif(slamdunk_gif_frame):
    load_gif_into(slamdunk_gif_frame, "GIF-8x8-slamdunk.png")


def load_db_4x4_gif(dragonball_gif_frame):
    load_gif_into(dragonball_gif_frame, "GIF-4x4-db.png")


def load_db_6x6_gif(dragonball_gif_frame):
    load_gif_into(dragonball_gif_frame, "GIF-6x6-db.png")


def load_db_8x8_gif(dragonball_gif_frame):
    load_gif_into(dragonball_gif_frame, "GIF-8x8-db.png")


def load_bleach_4x4_gif(bleach_gif_frame):
    load_gif_into(bleach_gif_frame, "GIF-4x4-bleach.png")


def load_bleach_6x6_gif(bleach_gif_frame):
    load_gif_into(bleach_gif_frame, "GIF-6x6-bleach.png")


def load_bleach_8x8_gif(bleach_gif_frame):
    load_gif_into(bleach_gif_frame, "GIF-8x8-bleach.png")

