import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Button Image Example")

# Load image using Pillow
image = Image.open('images/log-out_4562493.png')  # Change to the path of your image
photo = ImageTk.PhotoImage(image)

# Create button with image
button = tk.Button(root, image=photo, command=lambda: print("Button Clicked"))
button.pack(pady=20)

root.mainloop()