# UI component creation functions
import tkinter as tk
import customtkinter as ctk
import pywinstyles
from tkinter import PhotoImage
import os
from constants import COLOR_BG_PANEL, COLOR_PANEL_ACCENT, COLOR_BTN_TEXT, FONT_NAMES


def set_bg(frame, path):
    """Set background image for a frame"""
    if os.path.exists(path):
        try:
            img = PhotoImage(file=path)
            tk.Label(frame, image=img).place(x=0, y=0, relwidth=1, relheight=1)
            frame.bg_img = img
        except Exception:
            pass


def make_theme_btn(parent, text, y, cmd, font_name):
    """Create a theme button"""
    b = ctk.CTkButton(
        parent,
        text=text,
        font=(font_name, 19, "bold"),
        fg_color="#787c82",
        bg_color="#000001",
        text_color="black",
        hover_color="#FF5252",
        width=13 * 10,
        height=3 * 20,
        corner_radius=18,
        border_width=2,
        border_color="#8CE4FF",
        command=cmd,
    )
    
    def on_theme_enter(event):
        b.configure(text_color="white")
        b.configure(fg_color="black")
        b.configure(border_color="white")
    
    def on_theme_leave(event):
        b.configure(text_color="black")
        b.configure(fg_color="#787c82")
        b.configure(border_color="white")
    
    b.bind("<Enter>", on_theme_enter)
    b.bind("<Leave>", on_theme_leave)
    
    pywinstyles.set_opacity(b, color="#000001")
    b.place(y=y, anchor="center")
    return b


def make_tile_btn(parent, text, x, y, cmd, bg, abg, font_name):
    """Create a tile button for difficulty selection"""
    btn = ctk.CTkButton(
        parent,
        text=text,
        font=(font_name, 18, "bold"),
        fg_color="#787c82",
        bg_color="#000001",
        text_color="black",
        hover_color=abg,
        width=100,
        height=50,
        corner_radius=15,
        border_width=2,
        border_color="#FFFFFF",
        command=cmd,
    )
    
    def on_tile_enter(event):
        btn.configure(text_color="white")
        btn.configure(fg_color="black")
        btn.configure(border_color="white")
    
    def on_tile_leave(event):
        btn.configure(text_color="black")
        btn.configure(fg_color="#787c82")
        btn.configure(border_color="white")
    
    btn.bind("<Enter>", on_tile_enter)
    btn.bind("<Leave>", on_tile_leave)
    
    pywinstyles.set_opacity(btn, color="#000001")
    btn.place(x=x, y=y)
    return btn


def make_back_btn(parent, text, cmd, bg, abg, font_name):
    """Create a back button"""
    btn = ctk.CTkButton(
        parent,
        text=text,
        font=(font_name, 18, "bold"),
        fg_color="#787c82",
        bg_color="#000001",
        text_color="black",
        hover_color=abg,
        width=85,
        height=45,
        corner_radius=15,
        border_width=2,
        border_color="#FFFFFF",
        command=cmd,
    )
    
    def on_back_enter(event):
        btn.configure(text_color="white")
        btn.configure(fg_color="black")
        btn.configure(border_color="white")
    
    def on_back_leave(event):
        btn.configure(text_color="black")
        btn.configure(fg_color="#787c82")
        btn.configure(border_color="white")
    
    btn.bind("<Enter>", on_back_enter)
    btn.bind("<Leave>", on_back_leave)
    
    pywinstyles.set_opacity(btn, color="#000001")
    btn.place(relx=0.02, rely=0.02, anchor="nw")
    return btn


def hover(btn, color):
    """Hover effect for buttons"""
    try:
        btn["bg"] = color
    except:
        pass


def nothover(btn):
    """Remove hover effect"""
    try:
        btn["bg"] = "gold"
    except:
        pass

