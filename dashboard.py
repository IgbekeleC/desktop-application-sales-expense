import tkinter as tk
from tkinter import ttk
from inventory_management import create_inventory_management_section  # Corrected spelling
from sales import create_sales_section
from expenses import create_expense_section
from profit import create_profit_section
from user_management import create_user_management_section
from auth import logout


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales and Expense Tracker")
        self.root.geometry("900x600")  # Set a fixed size for the entire app

        self.sales_records = []  # Load or initialize sales records here
        self.expense_records = []  # Load or initialize expense records here

        self.create_sidebar()
        self.create_display_area()

    def create_sidebar(self):
        sidebar_width = int(self.root.winfo_width() / 3)  # 1/3 of the root width
        sidebar = tk.Frame(self.root, width=sidebar_width, bg='lightgray', relief='sunken', borderwidth=2)
        sidebar.pack(expand=False, fill='y', side='left', anchor='nw')

        # Sidebar buttons for different sections
        tk.Button(sidebar, text="Inventory Management", bg="orange", fg="blue", command=self.show_inventory_management, width=15, height=5).pack(fill="x", padx=10, pady=5)
        tk.Button(sidebar, text="Record Sales", bg="orange", fg="blue", command=self.show_sales, width=15, height=5).pack(fill="x", padx=10, pady=5)
        tk.Button(sidebar, text="Record Expense", bg="orange", fg="blue", command=self.show_expenses, width=15, height=5).pack(fill="x", padx=10, pady=5)
        tk.Button(sidebar, text="Calculate Profit", bg="orange", fg="blue", command=self.show_profit, width=15, height=5).pack(fill="x", padx=10, pady=5)
        tk.Button(sidebar, text="User Management", bg="orange", fg="blue", command=self.show_user_management, width=15, height=5).pack(fill="x", padx=10, pady=5)
        tk.Button(sidebar, text="Logout", bg="red", fg="black", command=self.logout, width=15, height=5).pack(fill="x", padx=10, pady=5)

        # Currency Selection and Exchange Rate
        currency_frame = tk.Frame(sidebar)
        tk.Label(currency_frame, text="Currency:").pack(side='left')
        currency_dropdown = ttk.Combobox(currency_frame, values=["NGN", "USD"])
        currency_dropdown.current(0)
        currency_dropdown.pack(side='left')

        tk.Label(currency_frame, text="Rate:").pack(side='left')
        exchange_rate_entry = tk.Entry(currency_frame, width=10)
        exchange_rate_entry.insert(0, "1.0")
        exchange_rate_entry.pack(side='left')

        currency_frame.pack(pady=10, fill="x")

    def create_display_area(self):
        self.display_area = tk.Frame(self.root, bg='white')
        self.display_area.pack(expand=True, fill='both', side='right')

    def show_inventory_management(self):
        self.clear_display_area()
        create_inventory_management_section(self.display_area)

    def show_sales(self):
        self.clear_display_area()
        create_sales_section(self.display_area)

    def show_expenses(self):
        self.clear_display_area()
        create_expense_section(self.display_area)

    def show_profit(self):
        self.clear_display_area()
        create_profit_section(self.display_area)

    def show_user_management(self):
        self.clear_display_area()
        create_user_management_section(self.display_area)

    def logout(self):
        self.clear_display_area()
        if logout():
            self.root.quit()

    def clear_display_area(self):
        for widget in self.display_area.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    dashboard = Dashboard(root)
    root.mainloop()

