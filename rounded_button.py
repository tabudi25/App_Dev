import tkinter as tk
import os

def get_arcade_font():
    """Get arcade-style font name - just return the font name string"""
    # Check if font file exists
    font_files = ["Arcade Classic.ttf", "ARCADECLASSIC.TTF", "ArcadeClassic.ttf"]
    
    for font_file in font_files:
        if os.path.exists(font_file):
            # Font file exists, return the expected font family name
            return "Arcade Classic"
    
    # Try system-installed arcade fonts (just return the name, don't test)
    arcade_fonts = [
        "Arcade Classic", "ArcadeClassic", "ARCADECLASSIC",
        "Press Start 2P", "PressStart2P",
        "Arcade", "Arcade Interlaced", "Arcade Rounded",
        "Courier New", "Lucida Console", "Consolas"
    ]
    
    # Return the first one as default (will fallback if not available)
    return arcade_fonts[0] if arcade_fonts else "Courier New"

_arcade_font_name = get_arcade_font()

def create_rounded_button(parent, x, y, width, height, radius, bg, text, command):
    canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0, bg=parent["bg"])
    canvas.place(x=x, y=y)

    def round_rect(x0, y0, x1, y1, r, **kwargs):
        points = [
            x0+r, y0,
            x1-r, y0,
            x1, y0,
            x1, y0+r,
            x1, y1-r,
            x1, y1,
            x1-r, y1,
            x0+r, y1,
            x0, y1,
            x0, y1-r,
            x0, y0+r,
            x0, y0
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    # Draw rounded rectangle (button background)
    button_shape = round_rect(5, 5, width-5, height-5, radius, fill=bg, outline="")

    # Add text with arcade font
    button_text = canvas.create_text(width/2, height/2, text=text, fill="white", font=(_arcade_font_name, 20, "bold"))

    # ✅ Bind click to both shape & text
    def on_click(event=None):
        if command:
            command()

    canvas.tag_bind(button_shape, "<Button-1>", on_click)
    canvas.tag_bind(button_text, "<Button-1>", on_click)
    canvas.bind("<Button-1>", on_click)  # whole canvas clickable

    return canvas
