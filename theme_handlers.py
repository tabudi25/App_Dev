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
    if os.path.exists("GIF-4x4.png"):
        try:
            if current_gif_label:
                current_gif_label.destroy()
            pil_img = Image.open("GIF-4x4.png")
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
    if os.path.exists("GIF-6x6.png"):
        try:
            if current_gif_label:
                current_gif_label.destroy()
            pil_img = Image.open("GIF-6x6.png")
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
    if os.path.exists("GIF-8x8.png"):
        try:
            if current_gif_label:
                current_gif_label.destroy()
            pil_img = Image.open("GIF-8x8.png")
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


def start_auto_transitions(naruto_gif_frame):
    """Start auto transitions for GIFs"""
    global auto_transition_running, current_auto_gif, transition_timer
    auto_transition_running = True
    current_auto_gif = 0
    cycle_auto_gifs(naruto_gif_frame)


def stop_auto_transitions():
    """Stop auto transitions"""
    global auto_transition_running, transition_timer
    auto_transition_running = False
    if transition_timer and root_ref:
        root_ref.after_cancel(transition_timer)
        transition_timer = None


def cycle_auto_gifs(naruto_gif_frame):
    """Cycle through auto GIFs"""
    global current_auto_gif, auto_transition_running, transition_timer
    if not auto_transition_running:
        return
    
    # Load current auto GIF
    gif_files = ["GIF-4x4.png", "GIF-6x6.png", "GIF-8x8.png"]
    if current_auto_gif < len(gif_files):
        load_auto_gif(naruto_gif_frame, gif_files[current_auto_gif])
        current_auto_gif = (current_auto_gif + 1) % len(gif_files)
    
    # Schedule next transition
    if root_ref:
        transition_timer = root_ref.after(3000, lambda: cycle_auto_gifs(naruto_gif_frame))


def load_auto_gif(naruto_gif_frame, gif_file):
    """Load auto GIF"""
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
            current_gif_label = tk.Label(naruto_gif_frame, image=img, bg="#1A1A2E")
            current_gif_label.place(relx=0.5, rely=0.5, anchor="center")
            current_gif_label.image = img
        except Exception:
            pass


# Theme-specific GIF loaders
def load_op_4x4_gif(onepiece_gif_frame):
    load_gif_into(onepiece_gif_frame, "GIF-4x4.png")


def load_op_6x6_gif(onepiece_gif_frame):
    load_gif_into(onepiece_gif_frame, "GIF-6x6.png")


def load_op_8x8_gif(onepiece_gif_frame):
    load_gif_into(onepiece_gif_frame, "GIF-8x8.png")


def load_slam_4x4_gif(slamdunk_gif_frame):
    load_gif_into(slamdunk_gif_frame, "GIF-4x4.png")


def load_slam_6x6_gif(slamdunk_gif_frame):
    load_gif_into(slamdunk_gif_frame, "GIF-6x6.png")


def load_slam_8x8_gif(slamdunk_gif_frame):
    load_gif_into(slamdunk_gif_frame, "GIF-8x8.png")


def load_db_4x4_gif(dragonball_gif_frame):
    load_gif_into(dragonball_gif_frame, "GIF-4x4.png")


def load_db_6x6_gif(dragonball_gif_frame):
    load_gif_into(dragonball_gif_frame, "GIF-6x6.png")


def load_db_8x8_gif(dragonball_gif_frame):
    load_gif_into(dragonball_gif_frame, "GIF-8x8.png")


def load_bleach_4x4_gif(bleach_gif_frame):
    load_gif_into(bleach_gif_frame, "GIF-4x4.png")


def load_bleach_6x6_gif(bleach_gif_frame):
    load_gif_into(bleach_gif_frame, "GIF-6x6.png")


def load_bleach_8x8_gif(bleach_gif_frame):
    load_gif_into(bleach_gif_frame, "GIF-8x8.png")

