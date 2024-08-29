from tkinter import *
from tkinter import font
from PIL import Image, ImageTk

class Dashboard(Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)

        # Use controller to reference the main Tk instance if needed
        self.controller = controller

        # Set the window to full-screen mode
        self.controller.state("zoomed")

        # Create custom fonts
        self.custom_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.title_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.content_font = font.Font(family="Arial", size=14)

        # Initialize UI
        self.create_top_bar()
        self.create_main_content()
        self.create_sections()

    def load_image(self, path, size):
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def create_top_bar(self):
        # Create the top frame with a border
        top_frame = Frame(self, bg="#64CCC5", height=40, bd=2, relief='solid', highlightbackground="#176B87", highlightcolor="#176B87")
        top_frame.pack(side="top", fill="x")

        # Create and pack the label inside the top frame
        top_label = Label(top_frame, text="Dashboard", font=("Helvetica", 16, "bold"), bg="#64CCC5", fg='#04364A')
        top_label.pack(pady=10)

    def create_main_content(self):
        self.main_content = Frame(self, bg="white", width=1000, height=800)
        self.main_content.pack(side="right", fill="both", expand=True)

        for i in range(4):
            self.main_content.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.main_content.grid_columnconfigure(i, weight=1)

    def create_section(self, title, icon, content, row, column, rowspan=1, colspan=1):
        section = LabelFrame(self.main_content, text=title, padx=10, pady=10, bg='white', font=self.title_font, fg='#176B87')
        section.grid(row=row, column=column, padx=10, pady=10, sticky="nsew", rowspan=rowspan, columnspan=colspan)
        
        if isinstance(icon, str):
            icon_label = Label(section, text=icon, font=font.Font(family="Arial", size=50), bg='white', fg='#176B87', width=3)
        else:
            icon_label = Label(section, image=icon, bg='white')
            icon_label.image = icon

        icon_label.pack(side="left")
        
        text_label = Label(section, text=content, anchor="w", bg='white', font=self.content_font, fg='#176B87')
        text_label.pack(side="left", fill="both", expand=True)

    def create_sections(self):
        sales_icon = self.load_image("images/Untitled.png", (80, 80))
        purchase_icon = self.load_image("images/purches.jpg", (80, 80))
        summary_icon = self.load_image("images/summary.png", (80, 80))
        topselling_icon = self.load_image("images/fire.png", (80, 80))
        sales_purchase_icon = self.load_image("images/chart1.jpg", (300, 150))
        order_summary_icon = self.load_image("images/chart2.jpg", (300, 150))

        self.create_section("Sales Overview", sales_icon, "Sales: ₹832\n\nRevenue: ₹18,300\n\nProfit: ₹868\n\nCost: ₹17,432", 0, 0)
        self.create_section("Purchase Overview", purchase_icon, "Purchase: 82\n\nCancel: 5\n\nCost: ₹15,320\n\nReturn: 3", 0, 1)
        self.create_section("Inventory Summary", summary_icon, "Quantity in Hand: 868\n\nTo be received: 200", 1, 0)
        self.create_section("Product Summary", summary_icon, "Suppliers: 30\n\nCategories: 14", 1, 1)
        self.create_section("Top Selling Stock", topselling_icon, "Surf Excel: 30\n\nRin: 21\n\nParle G: 19", 3, 0, colspan=1)
        self.create_section("Sales & Purchase", sales_purchase_icon, "", 2, 0)
        self.create_section("Order Summary", order_summary_icon, "", 2, 1)
