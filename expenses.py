import tkinter as tk
import csv
from tkinter import messagebox, ttk
from datetime import datetime
from sales import items  # Assuming items is imported from sales.py

expense_records = []

def load_expenses():
    global expense_records
    try:
        with open('expenses.csv', mode='r') as file:
            reader = csv.reader(file)
            expense_records = [row for row in reader]
    except FileNotFoundError:
        expense_records = []

def save_expenses():
    with open('expenses.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(expense_records)

def create_expense_section(parent):
    global sales_subtotal_label, fixed_subtotal_label, variable_subtotal_label, grand_total_label

    # Creating a canvas to add scrolling functionality
    canvas = tk.Canvas(parent)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add scrollbars
    v_scrollbar = tk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    h_scrollbar = tk.Scrollbar(parent, orient=tk.HORIZONTAL, command=canvas.xview)
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    # Configure canvas to work with scrollbars
    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Frame inside the canvas
    expense_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=expense_frame, anchor="nw")

    # Date Selection
    tk.Label(expense_frame, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
    expense_date_entry = tk.Entry(expense_frame)
    expense_date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
    expense_date_entry.grid(row=0, column=1)

    # Sales Items Expenses Table
    sales_items_frame = tk.LabelFrame(expense_frame, text="Sales Items")
    sales_items_frame.grid(row=1, column=0, columnspan=3, pady=5, sticky="w")
    sales_items_table, sales_subtotal_label = create_sales_items_table(sales_items_frame)

    # Fixed Assets Table
    fixed_assets_frame = tk.LabelFrame(expense_frame, text="Fixed Assets")
    fixed_assets_frame.grid(row=3, column=0, columnspan=3, pady=5, sticky="w")
    fixed_assets_table, fixed_subtotal_label = create_fixed_assets_table(fixed_assets_frame)

    # Variable Costs Table
    variable_costs_frame = tk.LabelFrame(expense_frame, text="Variable Costs")
    variable_costs_frame.grid(row=5, column=0, columnspan=3, pady=5, sticky="w")
    variable_costs_table, variable_subtotal_label = create_variable_costs_table(variable_costs_frame)

    # Summary Frame
    summary_frame = tk.LabelFrame(expense_frame, text="Summary")
    summary_frame.grid(row=7, column=0, columnspan=3, pady=10, sticky="w")

    tk.Label(summary_frame, text="Sales Items Subtotal:").grid(row=0, column=0, sticky="w")
    sales_subtotal_label = tk.Label(summary_frame, text="0.00")
    sales_subtotal_label.grid(row=0, column=1, sticky="w")

    tk.Label(summary_frame, text="Fixed Assets Subtotal:").grid(row=1, column=0, sticky="w")
    fixed_subtotal_label = tk.Label(summary_frame, text="0.00")
    fixed_subtotal_label.grid(row=1, column=1, sticky="w")

    tk.Label(summary_frame, text="Variable Costs Subtotal:").grid(row=2, column=0, sticky="w")
    variable_subtotal_label = tk.Label(summary_frame, text="0.00")
    variable_subtotal_label.grid(row=2, column=1, sticky="w")

    grand_total_label = tk.Label(summary_frame, text="Grand Total: $0.00")
    grand_total_label.grid(row=3, column=0, columnspan=2, sticky="w")

    # Add Expense Button
    tk.Button(expense_frame, text="Add Expense", command=lambda: add_expense(
        expense_date_entry, sales_items_table, fixed_assets_table, variable_costs_table, grand_total_label
    )).grid(row=8, column=0, columnspan=3, pady=10)

def create_sales_items_table(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="x")

    headers = ["Item", "Quantity", "Cost per Unit", "Total Cost"]
    for i, header in enumerate(headers):
        tk.Label(frame, text=header).grid(row=0, column=i)

    entries = []
    subtotal_label = tk.Label(frame, text="Subtotal: $0.00")
    subtotal_label.grid(row=99, column=3, sticky="e")

    def add_item():
        row = len(entries) + 1
        item_dropdown = ttk.Combobox(frame, values=list(items.keys()))
        item_dropdown.grid(row=row, column=0)

        quantity_entry = tk.Entry(frame)
        quantity_entry.grid(row=row, column=1)

        # Define cost per unit and total cost labels to display the values
        cost_per_unit_label = tk.Label(frame, text="0.00")  # This was the missing definition
        cost_per_unit_label.grid(row=row, column=2)

        total_cost_label = tk.Label(frame, text="0.00")
        total_cost_label.grid(row=row, column=3)

        def update_costs(event=None):
            item = item_dropdown.get()
            quantity = quantity_entry.get()
            if item in items and quantity.isdigit():
                cost_per_unit = items[item][1]  # Assuming items[item][1] is the cost per unit
                cost_per_unit_label.config(text=f"{cost_per_unit:.2f}")
                total_cost = int(quantity) * cost_per_unit
                total_cost_label.config(text=f"{total_cost:.2f}")
                update_subtotal()

        item_dropdown.bind("<<ComboboxSelected>>", update_costs)
        quantity_entry.bind("<KeyRelease>", update_costs)

        entries.append((item_dropdown, quantity_entry, cost_per_unit_label, total_cost_label))

    def update_subtotal():
        subtotal = sum(float(entry[3].cget("text")) for entry in entries)
        subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")
        update_grand_total()

    tk.Button(frame, text="Add Sales Item", command=add_item).grid(row=100, column=0, columnspan=4)

    return entries, subtotal_label

def create_fixed_assets_table(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="x")

    fixed_assets = {"Furniture": 500, "Laptop": 1000, "Fittings": 300, "TV": 800, "Car": 20000}

    headers = ["Asset", "Quantity", "Unit Cost", "Total Cost"]
    for i, header in enumerate(headers):
        tk.Label(frame, text=header).grid(row=0, column=i)

    entries = []
    subtotal_label = tk.Label(frame, text="Subtotal: $0.00")
    subtotal_label.grid(row=99, column=3, sticky="e")

    def add_asset():
        row = len(entries) + 1
        asset_dropdown = ttk.Combobox(frame, values=list(fixed_assets.keys()))
        asset_dropdown.grid(row=row, column=0)

        quantity_entry = tk.Entry(frame)
        quantity_entry.grid(row=row, column=1)

        unit_cost_label = tk.Label(frame, text="0.00")
        unit_cost_label.grid(row=row, column=2)

        total_cost_label = tk.Label(frame, text="0.00")
        total_cost_label.grid(row=row, column=3)

        def update_costs(event=None):
            asset = asset_dropdown.get()
            quantity = quantity_entry.get()
            if asset in fixed_assets and quantity.isdigit():
                unit_cost = fixed_assets[asset]
                unit_cost_label.config(text=f"{unit_cost:.2f}")
                total_cost = int(quantity) * unit_cost
                total_cost_label.config(text=f"{total_cost:.2f}")
                update_subtotal()

        asset_dropdown.bind("<<ComboboxSelected>>", update_costs)
        quantity_entry.bind("<KeyRelease>", update_costs)

        entries.append((asset_dropdown, quantity_entry, unit_cost_label, total_cost_label))

    def update_subtotal():
        subtotal = sum(float(entry[3].cget("text")) for entry in entries)
        subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")
        update_grand_total()

    tk.Button(frame, text="Add Fixed Asset", command=add_asset).grid(row=100, column=0, columnspan=4)

    return entries, subtotal_label

def create_variable_costs_table(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="x")

    headers = ["Description", "Cost"]
    for i, header in enumerate(headers):
        tk.Label(frame, text=header).grid(row=0, column=i)

    entries = []
    subtotal_label = tk.Label(frame, text="Subtotal: $0.00")
    subtotal_label.grid(row=99, column=1, sticky="e")

    def add_variable_cost():
        row = len(entries) + 1
        description_entry = tk.Entry(frame)
        description_entry.grid(row=row, column=0)

        cost_entry = tk.Entry(frame)
        cost_entry.grid(row=row, column=1)

        def update_costs(event=None):
            update_subtotal()

        description_entry.bind("<KeyRelease>", update_costs)
        cost_entry.bind("<KeyRelease>", update_costs)

        entries.append((description_entry, cost_entry))

    def update_subtotal():
        subtotal = sum(float(entry[1].get()) for entry in entries if entry[1].get().isdigit())
        subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")
        update_grand_total()

    tk.Button(frame, text="Add Variable Cost", command=add_variable_cost).grid(row=100, column=0, columnspan=2)

    return entries, subtotal_label

def update_grand_total():
    try:
        sales_text = sales_subtotal_label.cget("text")
        if '$' in sales_text:
            sales_subtotal = float(sales_text.split('$')[1])
        else:
            sales_subtotal = 0.0
    except (IndexError, ValueError):
        sales_subtotal = 0.0
    
    try:
        fixed_text = fixed_subtotal_label.cget("text")
        if '$' in fixed_text:
            fixed_subtotal = float(fixed_text.split('$')[1])
        else:
            fixed_subtotal = 0.0
    except (IndexError, ValueError):
        fixed_subtotal = 0.0
    
    try:
        variable_text = variable_subtotal_label.cget("text")
        if '$' in variable_text:
            variable_subtotal = float(variable_text.split('$')[1])
        else:
            variable_subtotal = 0.0
    except (IndexError, ValueError):
        variable_subtotal = 0.0

    grand_total = sales_subtotal + fixed_subtotal + variable_subtotal
    grand_total_label.config(text=f"Grand Total: ${grand_total:.2f}")


def add_expense(date_entry, sales_items_table, fixed_assets_table, variable_costs_table, grand_total_label):
    date = date_entry.get()

    # Collect data from all tables
    sales_items = [(
        item_dropdown.get(),
        quantity_entry.get(),
        cost_per_unit_label.cget("text"),
        total_cost_label.cget("text")
    ) for item_dropdown, quantity_entry, cost_per_unit_label, total_cost_label in sales_items_table]

    fixed_assets = [(
        asset_dropdown.get(),
        quantity_entry.get(),
        unit_cost_label.cget("text"),
        total_cost_label.cget("text")
    ) for asset_dropdown, quantity_entry, unit_cost_label, total_cost_label in fixed_assets_table]

    variable_costs = [(
        description_entry.get(),
        cost_entry.get()
    ) for description_entry, cost_entry in variable_costs_table]

    # Calculate total expense
    total_expense = grand_total_label.cget("text").split('$')[1]
    expense_records.append([date, sales_items, fixed_assets, variable_costs, total_expense])
    save_expenses()

    messagebox.showinfo("Success", "Expense record added successfully!")

    # Clear the entry fields and reset totals
    date_entry.delete(0, tk.END)
    for lbl in [sales_subtotal_label, fixed_subtotal_label, variable_subtotal_label, grand_total_label]:
        lbl.config(text="0.00")

    for table in [sales_items_table, fixed_assets_table, variable_costs_table]:
        for entry in table:
            for widget in entry:
                widget.destroy()

load_expenses()  # Load expenses when the module is imported


