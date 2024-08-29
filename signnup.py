from tkinter import Tk, Label, Entry, Frame, Canvas, messagebox
from PIL import Image, ImageTk
from tkinter import *
import subprocess
import sys
import sqlite3

conn = sqlite3.connect('C:/Users/a/stock_master.db')  # Adjust the path as necessary
cursor = conn.cursor()


def leave ():
    sign_up_window.destroy()
    subprocess.Popen([sys.executable, "main.py"])

def clear_entries():
    email_entry.delete(0, END)
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    confirm_password_entry.delete(0, END)

def sign_up():
    email = email_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Check if all fields are filled
    if email and username and password and confirm_password:
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")

            return
        else:
            try:
                cursor.execute("INSERT INTO users (email, user_name, password) VALUES (?, ?, ?)",
                               (email, username, password))
                conn.commit()
                messagebox.showinfo("Success", "User registered successfully!")
                clear_entries()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username or email already exists.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

    # Check if passwords match
     # Exit the function if validation fails

    # If all validations pass, you can now proceed with the sign-up process
    print("Add Member successful!")  # Placeholder for actual sign-up logic

def create_rounded_button(frame, text, command):
# Other parts of the code remain unchanged...def create_rounded_button(frame, text, command):
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

sign_up_window = Tk()
sign_up_window.title("Add Member")

    # Set window size and position
window_width = 1200
window_height = 700
screen_width = sign_up_window.winfo_screenwidth()
screen_height = sign_up_window.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
sign_up_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
sign_up_window.configure(bg="white")
sign_up_window.iconbitmap('images/add-user_1177577.ico')
frame = Frame(sign_up_window, bg="white")
frame.place(relx=0.5, rely=0.5, anchor="center")

sign_up_label = Label(frame, text="Add Member", font=("Arial", 36, "bold"), bg="white", fg="#04364A")
sign_up_label.grid(row=0, column=1, columnspan=2, pady=(0, 40))

    # Add email entry with placeholder
email_entry = Entry(frame, font=("Arial", 20), width=25, bd=0)
set_placeholder(email_entry, "Email", "grey")
email_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, "Email", "black"))
email_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, "Email", "grey"))
email_entry.grid(row=1, column=2, padx=20, pady=(10, 0), sticky='w')

canvas_email = Canvas(frame, width=350, height=2, bg="white", highlightthickness=0)
canvas_email.create_line(0, 0, 350, 0, fill="#04364A", width=2)
canvas_email.grid(row=2, column=2, padx=20, pady=(0, 20), sticky='w')

    # Add username entry with placeholder
username_entry = Entry(frame, font=("Arial", 20), width=25, bd=0)
set_placeholder(username_entry, "Username", "grey")
username_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, "Username", "black"))
username_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, "Username", "grey"))
username_entry.grid(row=4, column=2, padx=20, pady=(10, 0), sticky='w')

canvas_username = Canvas(frame, width=350, height=2, bg="white", highlightthickness=0)
canvas_username.create_line(0, 0, 350, 0, fill="#04364A", width=2)
canvas_username.grid(row=5, column=2, padx=20, pady=(0, 20), sticky='w')

    # Add password entry with placeholder
password_entry = Entry(frame, font=("Arial", 20), width=25, bd=0, show='*')
set_placeholder(password_entry, "Password", "grey")
password_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, "Password", "black"))
password_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, "Password", "grey"))
password_entry.grid(row=6, column=2, padx=20, pady=(10, 0), sticky='w')

canvas_password = Canvas(frame, width=350, height=2, bg="white", highlightthickness=0)
canvas_password.create_line(0, 0, 350, 0, fill="black", width=2)
canvas_password.grid(row=7, column=2, padx=20, pady=(0, 30), sticky='w')

    # Add confirm password entry with placeholder
confirm_password_entry = Entry(frame, font=("Arial", 20), width=25, bd=0, show='*')
set_placeholder(confirm_password_entry, "Confirm Password", "grey")
confirm_password_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, "Confirm Password", "black"))
confirm_password_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, "Confirm Password", "grey"))
confirm_password_entry.grid(row=8, column=2, padx=20, pady=(10, 0), sticky='w')

canvas_confirm_password = Canvas(frame, width=350, height=2, bg="white", highlightthickness=0)
canvas_confirm_password.create_line(0, 0, 350, 0, fill="black", width=2)
canvas_confirm_password.grid(row=9, column=2, padx=20, pady=(0, 30), sticky='w')

sign_up_button = create_rounded_button(frame, "Add Member", sign_up)
sign_up_button.grid(row=10, column=1, columnspan=2, pady=30)

frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=0)
frame.grid_columnconfigure(2, weight=1)
frame.grid_rowconfigure(0, weight=1)

button_leave = Button(sign_up_window, text="⬅️", font=("Helvetica", 20, "bold"), command=leave, bg="white",relief= "flat",

                       fg="#04364A")
button_leave.place(x=0, y=0)

sign_up_window.mainloop()

# Run the sign-up window
#create_sign_up_window()
conn.close()