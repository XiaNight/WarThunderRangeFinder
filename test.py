import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import ctypes

def make_window_click_through(hwnd):
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x00080000
    WS_EX_TRANSPARENT = 0x00000020
    LWA_COLORKEY = 0x00000001
    LWA_ALPHA = 0x00000002

    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 255, LWA_ALPHA)

def on_key(event):
    if event.keysym == 'Escape':
        root.quit()

def create_text_image(text, font, text_color, width, height):
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((width // 2, height // 2), text, font=font, fill=text_color, anchor="mm")
    return image

root = tk.Tk()
root.geometry("300x100+0+0")
root.attributes("-topmost", True)
root.overrideredirect(True)

root.update_idletasks()
root.after(0, make_window_click_through, root.winfo_id())

width, height = 300, 100
text = "Hello, World!"
font = ImageFont.truetype("arial.ttf", 20)
text_color = (255, 255, 255)

text_image = create_text_image(text, font, text_color, width, height)
photo = ImageTk.PhotoImage(text_image)

label = tk.Label(root, image=photo, bg=None)
label.pack(fill=tk.BOTH, expand=True)

root.bind("<Key>", on_key)

root.mainloop()