import subprocess
from tkinter import Tk, Label, Entry, Frame, Canvas, Toplevel, messagebox
from PIL import Image, ImageTk
import sqlite3

conn = sqlite3.connect('C:/Users/a/stock_master.db')
cursor = conn.cursor()



# Example: Fetch users from the 'users' table
def fetch_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Close the connection when done
def close_connection():
    conn.close()


def open_main_application():
    username = username_entry.get()
    password = password_entry.get()
    cursor.execute("SELECT * FROM users WHERE user_name = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        root.destroy()  # Close the current Sign In window
        subprocess.Popen(["python", "main.py"])  # Execute the main.py script

    else:
        messagebox.showerror("Error", "Invalid username or password")


def create_rounded_button(frame, text, command):
    canvas = Canvas(frame, width=220, height=60, bg="white", highlightthickness=0)
    canvas.create_oval(2, 2, 60, 60, fill="#64CCC5", outline="#64CCC5")
    canvas.create_oval(160, 2, 218, 60, fill="#64CCC5", outline="#64CCC5")
    canvas.create_rectangle(30, 2, 190, 60, fill="#64CCC5", outline="#64CCC5")
    canvas.create_text(110, 32, text=text, fill="#04364A", font=("Arial", 20, "bold"))
    canvas.bind("<Button-1>", lambda e: command())
    return canvas

def set_placeholder(entry, placeholder, color):
    entry.insert(0, placeholder)
    entry.config(fg=color)

def clear_placeholder(event, placeholder, color):
    entry = event.widget
    if entry.get() == placeholder:
        entry.delete(0, 'end')
        entry.config(fg=color)

def restore_placeholder(event, placeholder, color):
    entry = event.widget
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg=color)

root = Tk()
root.title("Sign In")
root.iconbitmap('images/user_2.ico')
# Set window size
window_width = 1200
window_height = 700

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate x and y coordinates for the window to be centered
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Set the dimensions of the window and position it
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg="white")

frame = Frame(root, bg="white")
frame.place(relx=0.5, rely=0.5, anchor="center")

image = Image.open("images/pic.jpg")  # Changed to use forward slashes
image = image.resize((300, 300), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

canvas = Canvas(frame, width=300, height=300, bg="white", highlightthickness=0)
canvas.create_image(150, 150, image=photo)
canvas.grid(row=0, column=0, rowspan=5, padx=50, pady=20)

sign_in_label = Label(frame, text="Sign in", font=("Arial", 36, "bold"), bg="white", fg="#04364A")
sign_in_label.grid(row=0, column=1, columnspan=2, pady=(0, 40))

# Add username entry with placeholder
username_entry = Entry(frame, font=("Arial", 20), width=25, bd=0)
set_placeholder(username_entry, "Username", "grey")
username_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, "Username", "black"))
username_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, "Username", "grey"))
username_entry.grid(row=1, column=2, padx=20, pady=(10, 0), sticky='w')

canvas_username = Canvas(frame, width=350, height=2, bg="white", highlightthickness=0)
canvas_username.create_line(0, 0, 350, 0, fill="#04364A", width=2)
canvas_username.grid(row=2, column=2, padx=20, pady=(0, 20), sticky='w')

# Add password entry with placeholder
password_entry = Entry(frame, font=("Arial", 20), width=25, bd=0, show='*')
set_placeholder(password_entry, "Password", "grey")
password_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, "Password", "black"))
password_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, "Password", "grey"))
password_entry.grid(row=3, column=2, padx=20, pady=(10, 0), sticky='w')

canvas_password = Canvas(frame, width=350, height=2, bg="white", highlightthickness=0)
canvas_password.create_line(0, 0, 350, 0, fill="black", width=2)
canvas_password.grid(row=4, column=2, padx=20, pady=(0, 30), sticky='w')

sign_in_button = create_rounded_button(frame, "Sign In", open_main_application)
sign_in_button.grid(row=5, column=1, columnspan=2, pady=30)

sign_up_frame = Frame(frame, bg="white")
sign_up_frame.grid(row=6, column=1, columnspan=2, pady=(0, 20))

frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=0)
frame.grid_columnconfigure(2, weight=1)
frame.grid_rowconfigure(0, weight=1)

root.mainloop()
