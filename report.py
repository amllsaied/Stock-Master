import sqlite3
import tkinter as tk
from tkinter import font
from tkinter import ttk

# Connect to the SQLite database

conn = sqlite3.connect('C:/Users/a/stock_master.db')
# Function to fetch data from database
def fetch_best_selling_products():
    cursor = conn.cursor()
    cursor.execute("SELECT Product, ID, Qty, Turnover FROM BestSellingProducts")
    return cursor.fetchall()

def fetch_inventory_levels():
    cursor = conn.cursor()
    cursor.execute("SELECT Item, Qty, Min, Max, Reorder FROM InventoryLevels")
    return cursor.fetchall()

def fetch_overview():
    cursor = conn.cursor()
    cursor.execute("SELECT Metric, Value FROM Overview")
    return cursor.fetchall()

def fetch_stock_movement():
    cursor = conn.cursor()
    cursor.execute("SELECT Month, Inbound FROM StockMovement")
    return cursor.fetchall()

# Define the Report class
class Report(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)

        # Function to create a section with a table
        def create_section(frame, title, columns, data, row, column, rowspan=1, colspan=1):
            # Define custom fonts
            title_font = font.Font(family="Helvetica", size=10, weight="bold")

            # Create the section frame
            section = tk.LabelFrame(frame, text=title, padx=5, pady=5, bg='#64CCC5', font=title_font, fg='#176B87', bd=2, relief='solid')
            section.grid(row=row, column=column, padx=5, pady=5, sticky="nsew", rowspan=rowspan, columnspan=colspan)

            # Create the Treeview widget
            tree = ttk.Treeview(section, columns=columns, show='headings', height=4)
            tree.pack(fill="both", expand=True)

            # Define the columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor='center', width=50)

            # Insert data into the table
            for data_row in data:
                tree.insert('', 'end', values=data_row)

            # Apply styles to the Treeview
            style = ttk.Style()
            style.configure("Treeview", background="white", foreground="#04364A", rowheight=20, columnwidth=1)
            style.map('Treeview',
                      background=[('selected', '#176B87')],
                      foreground=[('selected', 'white')])
            style.configure("Treeview.Heading", foreground="#04364A", font=("Arial", 8, "bold"))

        # Create the main window components
        self.configure(bg='#04364A')

        # Create the top frame
        top_frame = tk.Frame(self, bg="#64CCC5", height=40, bd=2, relief='solid', highlightbackground="#176B87", highlightcolor="#176B87")
        top_frame.pack(side="top", fill="x")

        # Add label to the top frame
        top_label = tk.Label(top_frame, text="Report", font=("Arial", 18), bg="#64CCC5", fg="#04364A")
        top_label.pack(pady=5)

        # Create the frame for the main content
        main_content = tk.Frame(self, bg="white", bd=2, relief='solid', highlightbackground="#176B87", highlightcolor="#176B87")
        main_content.pack(side="right", fill="both", expand=True)

        # Configure the grid layout for the main content
        main_content.grid_rowconfigure(0, weight=1)
        main_content.grid_rowconfigure(1, weight=1)
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)

        # Define columns and data for each section by fetching from the database
        best_selling_columns = ["Product", "ID", "Qty", "Turnover"]
        best_selling_data = fetch_best_selling_products()

        overview_columns = ["Metric", "Value"]
        overview_data = fetch_overview()

        inventory_columns = ["Item", "Qty", "Min", "Max", "Reorder"]
        inventory_data = fetch_inventory_levels()

        stock_columns = ["Month", "Inbound"]
        stock_data = fetch_stock_movement()

        # Add sections to the main content
        create_section(main_content, "Best Selling Product", best_selling_columns, best_selling_data, 0, 0)
        create_section(main_content, "Overview", overview_columns, overview_data, 0, 1)
        create_section(main_content, "Inventory Levels", inventory_columns, inventory_data, 1, 0)
        create_section(main_content, "Stock Movement", stock_columns, stock_data, 1, 1)

# Main application code
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Report Application")
    root.geometry("800x600")

    report_frame = Report(root)
    report_frame.pack(fill="both", expand=True)

    root.mainloop()

    # Close the database connection when the application exits
    conn.close()