import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

conn = sqlite3.connect('C:/Users/a/stock_master.db')

# Create the suppliers table if it does not exist
def create_suppliers_table():
    with conn:
        conn.execute('''  
        CREATE TABLE IF NOT EXISTS suppliers (  
            supplier_name TEXT,  
            product_name TEXT,  
            contact_number TEXT,  
            sup_email TEXT  
        )  
        ''')

    # Call to create table


create_suppliers_table()


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
        self.create_arc(x1, y1, x1 + 2 * r, y2, start=90, extent=180, style=PIESLICE, outline=kwargs['fill'],
                        fill=kwargs['fill'])
        self.create_arc(x2 - 2 * r, y1, x2, y2, start=270, extent=180, style=PIESLICE, outline=kwargs['fill'],
                        fill=kwargs['fill'])
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


class Suppliers(Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)

        # Top frame            (self, bg="#64CCC5", height=50, padx=10, pady=10, highlightbackground="#176B87", highlightthickness=2)
        self.top_frame = Frame(self, bg="#64CCC5", height=50, padx=10, pady=10, highlightbackground="#176B87",
                               highlightthickness=2)
        self.top_frame.pack(side=TOP, fill=X)
        self.create_top_frame()

        # Main frame
        self.main_frame = Frame(self, bg="white", highlightbackground="#176B87", highlightthickness=2)
        self.main_frame.pack(fill=BOTH, expand=True)
        self.create_supplier_table()

        # Side frame
        self.side_frame = None

        # Load suppliers from database
        self.load_suppliers()

    def load_suppliers(self):
        cursor = conn.cursor()
        cursor.execute("SELECT supplier_name, product_name, contact_number, sup_email FROM suppliers")
        suppliers_data = cursor.fetchall()
        for value in suppliers_data:
            self.supplier_tree.insert("", "end", values=value)

    def delete_selected_item(self):
        selected_item = self.supplier_tree.focus()
        if selected_item:
            supplier_name = self.supplier_tree.item(selected_item)['values'][0]
            with conn:
                conn.execute("DELETE FROM suppliers WHERE supplier_name = ?", (supplier_name,))
            self.supplier_tree.delete(selected_item)

    def create_top_frame(self):
        header = Label(self.top_frame, text="Suppliers", font=("Arial", 18, "bold"), bg="#64CCC5", fg="#04364A")
        header.pack(anchor=CENTER)

        # Buttons for adding and deleting suppliers
        add_supplier_button = RoundedButton(self.top_frame, text="Add Supplier", command=self.open_side_frame, width=200, height=60)
        add_supplier_button.pack(side=RIGHT, padx=10)

        delete_supplier_button = RoundedButton(self.top_frame, text="Delete Supplier",
                                               command=self.delete_selected_item, width=200, height=60)
        delete_supplier_button.pack(side=RIGHT, padx=10)

    def create_supplier_table(self):
        # Frame for the table
        table_frame = Frame(self.main_frame, bg="white", padx=5, pady=10, highlightbackground="#176B87",
                            highlightthickness=2)
        table_frame.pack(side=RIGHT,fill=BOTH, expand=True)

        # Treeview for displaying suppliers
        self.supplier_tree = ttk.Treeview(table_frame, columns=("Supplier Name", "Product", "Contact Number", "Email"),
                                          show='headings')

        for col in self.supplier_tree["columns"]:
            self.supplier_tree.heading(col, text=col)

        self.supplier_tree.pack(fill=BOTH, expand=True)

        # Apply styles to the Treeview
        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="#04364A", rowheight=25, font=("Helvetica", 10))
        style.map('Treeview', background=[('selected', '#176B87')], foreground=[('selected', 'white')])
        style.configure("Treeview.Heading", background="#64CCC5", foreground="#04364A", font=("Arial", 10, "bold"))

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.supplier_tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.supplier_tree.configure(yscroll=scrollbar.set)

    def open_side_frame(self):
        if self.side_frame is None:
            self.side_frame = Frame(self.main_frame, width=300, bg="#64CCC5", highlightbackground="#176B87",
                                    highlightthickness=2)
            self.side_frame.pack(side=RIGHT, fill=Y)

            # Title
            title_label = Label(self.side_frame, text="New Supplier", font=("Arial", 16), bg="#64CCC5", fg="#04364A")
            title_label.pack(pady=10)

            add_supplier_list = ["Supplier Name", "Product", "Contact Number", "Mail ID"]
            self.entries = {}  # To store references to entry fields

            for field in add_supplier_list:
                frame = Frame(self.side_frame, bg="#64CCC5")
                frame.pack(pady=10, padx=5, fill=X)

                Label(frame, text=field, bg="#64CCC5", font=("Arial", 12)).pack(anchor=W)

                entry = Entry(frame, font=("Arial", 12))
                entry.pack(fill=X, padx=10)

                self.entries[field] = entry  # Store entry reference in the dictionary

            save_button = RoundedButton(self.side_frame, text="Save", command=self.save_supplier, width=200, height=50)
            save_button.pack(pady=20)

            close_button = RoundedButton(self.side_frame, text="Close", command=self.close_side_frame, width=200,
                                         height=50)
            close_button.pack()

    def save_supplier(self):
        supplier_data = []
        for field, entry in self.entries.items():
            value = entry.get()
            supplier_data.append(value)

        if len(supplier_data) == 4:  # Ensure all fields are filled
            # Insert new supplier into the database
            with conn:
                conn.execute(
                    "INSERT INTO suppliers (supplier_name, product_name, contact_number, sup_email) VALUES (?, ?, ?, ?)",
                    (supplier_data[0], supplier_data[1], supplier_data[2], supplier_data[3]))
            self.supplier_tree.insert("", "end", values=supplier_data)
            messagebox.showinfo("Supplier Added", "New supplier has been added successfully.")
            self.close_side_frame()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def close_side_frame(self):
        if self.side_frame is not None:
            self.side_frame.destroy()
            self.side_frame = None


if __name__ == "__main__":
    root = Tk()
    root.geometry("1000x600")
    root.title("Supplier Management System")

    app = Suppliers(root)
    app.pack(fill=BOTH, expand=True)

    root.mainloop()

    # Close the database connection when the application exits
    conn.close()