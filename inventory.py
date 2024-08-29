import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

# Connect to the SQLite database

conn = sqlite3.connect('C:/Users/a/stock_master.db')
cursor = conn.cursor()

# Define the inventory table structure in the database
def create_inventory_table():
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS inventory (  
            id INTEGER PRIMARY KEY,  
            product_name TEXT NOT NULL,  
            category TEXT NOT NULL,  
            stock INTEGER NOT NULL,  
            price REAL NOT NULL  
        )  
    ''')
    conn.commit()

create_inventory_table()  # Create the table if it does not exist

class RoundedButton(Canvas):
    def __init__(self, parent, text, command=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.command = command
        self.text = text
        self.configure(bg="#64CCC5", highlightthickness=0)
        self.create_rounded_button()
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def create_rounded_button(self):
        self.delete("all")
        self.create_rounded_rectangle(10, 10, 180, 50, fill="#04364A", outline="#04364A")
        self.create_text(95, 30, text=self.text, fill="white", font=("Helvetica", 12))

    def create_rounded_rectangle(self, x1, y1, x2, y2, **kwargs):
        r = (y2 - y1) // 2
        self.create_arc(x1, y1, x1 + 2 * r, y2, start=90, extent=180, style=PIESLICE, outline=kwargs['fill'], fill=kwargs['fill'])
        self.create_arc(x2 - 2 * r, y1, x2, y2, start=270, extent=180, style=PIESLICE, outline=kwargs['fill'], fill=kwargs['fill'])
        self.create_rectangle(x1 + r, y1, x2 - r, y2, outline=kwargs['fill'], fill=kwargs['fill'])

    def on_click(self, event):
        if self.command:
            self.command()

    def on_hover(self, event):
        self.delete("all")
        self.create_rounded_rectangle(10, 10, 180, 50, fill="#0A4B57", outline="#0A4B57")
        self.create_text(95, 30, text=self.text, fill="white", font=("Helvetica", 12))

    def on_leave(self, event):
        self.delete("all")
        self.create_rounded_rectangle(10, 10, 180, 50, fill="#04364A", outline="#04364A")
        self.create_text(95, 30, text=self.text, fill="white", font=("Helvetica", 12))


class InventoryManagementApp(Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        self.create_top_frame()
        self.create_table()
        self.create_side_frame()

    def create_top_frame(self):
        self.top_frame = Frame(self, bg="#64CCC5", height=50, padx=10, pady=10, highlightbackground="#176B87", highlightthickness=2)
        self.top_frame.pack(side=TOP, fill=X)

        header = Label(self.top_frame, text="Inventory Management", font=("Arial", 18, "bold"), bg="#64CCC5", fg="#04364A")
        header.pack(anchor=CENTER)

        # Add Product Button
        add_product_button = RoundedButton(self.top_frame, text="Add Product", command=self.open_side_frame, width=200, height=60)
        add_product_button.pack(side=RIGHT, padx=10)

        # Delete Product Button
        delete_product_button = RoundedButton(self.top_frame, text="Delete Product", command=self.delete_selected_item, width=200, height=60)
        delete_product_button.pack(side=RIGHT, padx=10)

        # Info Button
        info_button = RoundedButton(self.top_frame, text="Info", command=self.show_info, width=200, height=60)
        info_button.pack(side=RIGHT, padx=10)

    def create_table(self):
        self.main_frame = Frame(self, bg="white", highlightbackground="#176B87", highlightthickness=2)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.product_tree = ttk.Treeview(self.main_frame, columns=("Product Name", "Category", "Stock", "Price"), show='headings')

        for col in ("Product Name", "Category", "Stock", "Price"):
            self.product_tree.heading(col, text=col)

        self.product_tree.pack(fill=BOTH, expand=True)

        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="#04364A", rowheight=25, font=("Helvetica", 10))
        style.map('Treeview', background=[('selected', '#176B87')], foreground=[('selected', 'white')])
        style.configure("Treeview.Heading", background="#64CCC5", foreground="#04364A", font=("Arial", 10, "bold"))

        self.load_inventory()

        scrollbar = ttk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.product_tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.product_tree.configure(yscroll=scrollbar.set)

    def load_inventory(self):
        for row in self.product_tree.get_children():  # Clear existing entries
            self.product_tree.delete(row)

        cursor.execute("SELECT product_name, category, stock, price FROM inventory")
        for product in cursor.fetchall():
            self.product_tree.insert("", "end", values=product)

    def create_side_frame(self):
        self.side_frame = None

    def delete_selected_item(self):
        selected_item = self.product_tree.focus()
        if selected_item:
            product_name = self.product_tree.item(selected_item, "values")[0]
            cursor.execute("DELETE FROM inventory WHERE product_name=?", (product_name,))
            conn.commit()
            self.product_tree.delete(selected_item)

    def open_side_frame(self):
        if self.side_frame is None:
            self.side_frame = Frame(self.main_frame, width=300, bg="#64CCC5", highlightbackground="#176B87", highlightthickness=2)
            self.side_frame.pack(side=RIGHT, fill=Y)

            title_label = Label(self.side_frame, text="New Product", font=("Arial", 16), bg="#64CCC5", fg="#04364A")
            title_label.pack(pady=10)

            add_product_list = ["Product Name", "Category", "Stock", "Price"]
            self.entries = {}

            for field in add_product_list:
                frame = Frame(self.side_frame, bg="#64CCC5")
                frame.pack(pady=10, padx=5, fill=X)

                Label(frame, text=field, bg="#64CCC5", font=("Arial", 12)).pack(anchor=W)

                entry = Entry(frame, font=("Arial", 12))
                entry.pack(fill=X, padx=10)

                self.entries[field] = entry

            save_button = RoundedButton(self.side_frame, text="Save", command=self.save_product, width=200, height=50)
            save_button.pack(pady=20)

            close_button = RoundedButton(self.side_frame, text="Close", command=self.close_side_frame, width=200, height=50)
            close_button.pack()

    def save_product(self):
        product_data = {
            "product_name": self.entries["Product Name"].get(),
            "category": self.entries["Category"].get(),
            "stock": self.entries["Stock"].get(),
            "price": self.entries["Price"].get(),
        }

        # Input validation
        if all(product_data.values()):
            try:
                stock = int(product_data["stock"])
                price = float(product_data["price"])

                cursor.execute("INSERT INTO inventory (product_name, category, stock, price) VALUES (?, ?, ?, ?)",
                               (product_data["product_name"], product_data["category"], stock, price))
                conn.commit()

                self.product_tree.insert("", "end", values=(product_data["product_name"], product_data["category"], stock, price))
                messagebox.showinfo("Product Added", "New product has been added successfully.")
                self.close_side_frame()
            except ValueError:
                messagebox.showwarning("Input Error", "Stock must be an integer and Price must be a number.")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def close_side_frame(self):
        if self.side_frame is not None:
            self.side_frame.destroy()
            self.side_frame = None

    def show_info(self):
        selected_item = self.product_tree.focus()
        if selected_item:
            item_values = self.product_tree.item(selected_item, "values")
            info_message = f"Product Name: {item_values[0]}\nCategory: {item_values[1]}\nStock: {item_values[2]}\nPrice: ${item_values[3]}"
            messagebox.showinfo("Product Information", info_message)
        else:
            messagebox.showwarning("No Selection", "Please select an item to view its information.")

if __name__ == "__main__":
    root = Tk()
    root.title("Inventory Management System")
    root.geometry("1000x600")
    app = InventoryManagementApp(root)
    app.pack(fill=BOTH, expand=True)
    root.mainloop()

    # Close the database connection when the application exits
    conn.close()