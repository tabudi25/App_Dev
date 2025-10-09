import tkinter as tk

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

    # Add text
    button_text = canvas.create_text(width/2, height/2, text=text, fill="white", font=("Arial", 20, "bold"))

    # ✅ Bind click to both shape & text
    def on_click(event=None):
        if command:
            command()

    canvas.tag_bind(button_shape, "<Button-1>", on_click)
    canvas.tag_bind(button_text, "<Button-1>", on_click)
    canvas.bind("<Button-1>", on_click)  # whole canvas clickable

    return canvas
