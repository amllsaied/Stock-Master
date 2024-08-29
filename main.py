from tkinter import *

from tkinter import messagebox
from dashboard import Dashboard
from inventory import InventoryManagementApp
from report import Report
from suppliers_page import Suppliers
import subprocess
import sys
from PIL import Image, ImageTk




def load_image(path, size):
    img = Image.open(path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)


class Application(Tk):
    def __init__(self):
        super().__init__()
        self.title("StockMaster")
        self.iconbitmap('images/inventory-management_12440902.ico')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f"{width}x{height}")

        # Create a container for the frames
        self.container = Frame(self)
        self.container.pack(fill="both", expand=True, side=RIGHT)

        # Configure the grid for the container so it expands properly
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Left sidebar with borders
        self.sidebar = Frame(self, width=200, bg="#64CCC5", bd=2, relief='solid', highlightbackground="#176B87", highlightcolor="#176B87")
        self.sidebar.pack(side=LEFT, fill=Y)

        self.create_sidebar_items()

        # Create frames for each section
        self.frames = {}
        for F in (Dashboard, InventoryManagementApp, Report, Suppliers):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Dashboard")  # Show the dashboard by default


    def create_sidebar_items(self):
        buttons = [
            ("Dashboard", "Dashboard", "🏠"),
            ("Inventory", "InventoryManagementApp", "📦"),
            ("Report", "Report", "📊"),
            ("Suppliers", "Suppliers", "👥")
        ]

        for (text, frame_name, icon) in buttons:
            button = Button(self.sidebar, text=f"{icon} {text}", relief="flat", font=(10),
                            anchor="w", bg="#64CCC5", bd=0, fg="#04364A",
                            command=lambda name=frame_name: self.show_frame(name))
            button.pack(fill="x", padx=10, pady=(20))

        log_out_button = Button(self.sidebar, text="⟶Log Out", relief="flat", font=(10),
                                anchor="w", bg="#64CCC5", bd=0, fg="#04364A", command=self.logOut)
        add_member_button = Button(self.sidebar, text="👤Add Member", relief="flat", font=(10),
                                   anchor="w", bg="#64CCC5", bd=0, fg="#04364A", command=self.signup_page)
        add_member_button.pack(fill="x", padx=10, pady=(20))

        log_out_button.pack(fill="x", padx=10, pady=(50), side=BOTTOM)

    def show_frame(self, page_name):
        frame = self.frames[page_name]

        frame.tkraise()  # Raise the selected frame to the top

    def logOut(self):
        # Create a confirmation dialog
        result = messagebox.askokcancel("Log Out", "Are you sure you want to log out?")
        if result:
            self.destroy()
            subprocess.Popen([sys.executable, "login.py"])

    def signup_page(self):
        self.destroy()
        subprocess.Popen([sys.executable, "signnup.py"])

if __name__ == "__main__":
    app = Application()
    app.mainloop()
