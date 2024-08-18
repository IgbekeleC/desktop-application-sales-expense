import tkinter as tk
import csv
from tkinter import messagebox, ttk
from datetime import datetime

sales_records = []
items = {}
low_stock_threshold = 10
vat_rate = 0.15  # 15% VAT

def load_sales():
    global sales_records
    try:
        with open('sales.csv', mode='r') as file:
            reader = csv.reader(file)
            sales_records = [row for row in reader]
    except FileNotFoundError:
        sales_records = []

def save_sales():
    with open('sales.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sales_records)

def load_items():
    global items
    try:
        with open('items.csv', mode='r') as file:
            reader = csv.reader(file)
            # Updating item structure to include quantity and price
            items = {rows[0]: [int(rows[1]), float(rows[2])] for rows in reader}
    except FileNotFoundError:
        # Default items structure: "ItemName": [Quantity, UnitPrice]
        items = {"iPhone": [1000, 10.00], "Watch": [500, 5.50], "Books": [1000, 2.50], "TV": [500, 50.50]} 

def save_items():
    with open('items.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for item, details in items.items():
            writer.writerow([item, details[0], details[1]])

def create_inventory_management_section(parent):
    inventory_frame = tk.LabelFrame(parent, text="Inventory Management")
    inventory_frame.pack(fill="both", expand="yes", padx=10, pady=10)

    tk.Label(inventory_frame, text="Item Name").grid(row=0, column=0)
    tk.Label(inventory_frame, text="Quantity").grid(row=1, column=0)
    tk.Label(inventory_frame, text="Unit Price").grid(row=2, column=0)

    item_name_entry = tk.Entry(inventory_frame)
    quantity_entry = tk.Entry(inventory_frame)
    unit_price_entry = tk.Entry(inventory_frame)

    item_name_entry.grid(row=0, column=1)
    quantity_entry.grid(row=1, column=1)
    unit_price_entry.grid(row=2, column=1)

    tk.Button(inventory_frame, text="Add Item", 
              command=lambda: add_item(item_name_entry, quantity_entry, unit_price_entry)).grid(row=3, column=0, columnspan=2)

def add_item(item_name_entry, quantity_entry, unit_price_entry):
    item_name = item_name_entry.get()
    quantity = int(quantity_entry.get())
    unit_price = float(unit_price_entry.get())

    if item_name in items:
        items[item_name][0] += quantity  # Update quantity if item already exists
    else:
        items[item_name] = [quantity, unit_price]  # Add new item

    save_items()

    item_name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    unit_price_entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Item added/updated successfully!")

def create_sales_section(parent):
    sales_frame = tk.LabelFrame(parent, text="Record Sales")
    sales_frame.pack(fill="both", expand="yes", padx=10, pady=10)

    tk.Label(sales_frame, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
    tk.Label(sales_frame, text="Customer").grid(row=1, column=0)
    tk.Label(sales_frame, text="Select Item").grid(row=2, column=0)
    tk.Label(sales_frame, text="Quantity").grid(row=3, column=0)

    sales_date_entry = tk.Entry(sales_frame)
    sales_date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
    customer_entry = tk.Entry(sales_frame)
    item_dropdown = ttk.Combobox(sales_frame, values=list(items.keys()))
    quantity_dropdown = ttk.Combobox(sales_frame, values=list(range(1, 101)))

    sales_date_entry.grid(row=0, column=1)
    customer_entry.grid(row=1, column=1)
    item_dropdown.grid(row=2, column=1)
    quantity_dropdown.grid(row=3, column=1)

    # Create summary section
    summary_table, vat_label, grand_total_label = create_summary_section(parent)

    tk.Button(sales_frame, text="Add Item", 
              command=lambda: add_item_to_cart(item_dropdown, quantity_dropdown, summary_table, vat_label, grand_total_label)).grid(row=4, column=0, columnspan=2)

    tk.Button(sales_frame, text="Complete Sale", 
              command=lambda: complete_sale(sales_date_entry, customer_entry, summary_table)).grid(row=5, column=0, columnspan=2)

def create_summary_section(parent):
    summary_frame = tk.LabelFrame(parent, text="Summary")
    summary_frame.pack(fill="both", expand="yes", padx=10, pady=10)

    columns = ('Item', 'Quantity', 'Unit Price', 'Total Price')
    summary_table = ttk.Treeview(summary_frame, columns=columns, show='headings')
    summary_table.grid(row=0, column=0, columnspan=4)

    for col in columns:
        summary_table.heading(col, text=col)
        summary_table.column(col, width=100)

    tk.Label(summary_frame, text="VAT (15%)").grid(row=1, column=2)
    vat_label = tk.Label(summary_frame, text="0.00")
    vat_label.grid(row=1, column=3)

    tk.Label(summary_frame, text="Grand Total").grid(row=2, column=2)
    grand_total_label = tk.Label(summary_frame, text="0.00")
    grand_total_label.grid(row=2, column=3)

    return summary_table, vat_label, grand_total_label

def add_item_to_cart(item_dropdown, quantity_dropdown, summary_table, vat_label, grand_total_label):
    item = item_dropdown.get()
    quantity = int(quantity_dropdown.get())

    if item in items:
        if items[item][0] >= quantity:
            unit_price = items[item][1]
            total_price = quantity * unit_price

            summary_table.insert('', 'end', values=(item, quantity, f"${unit_price:.2f}", f"${total_price:.2f}"))

            update_totals(summary_table, vat_label, grand_total_label)

            items[item][0] -= quantity
            save_items()

            if items[item][0] <= low_stock_threshold:
                messagebox.showwarning("Low Stock", f"{item} is running low on stock!")
        else:
            messagebox.showerror("Error", "Not enough stock available.")
    else:
        messagebox.showerror("Error", "Item not found.")

    item_dropdown.set('')
    quantity_dropdown.set('')

def update_totals(summary_table, vat_label, grand_total_label):
    total = 0
    for child in summary_table.get_children():
        total += float(summary_table.item(child, 'values')[3][1:])

    vat = total * vat_rate
    grand_total = total + vat

    vat_label.config(text=f"${vat:.2f}")
    grand_total_label.config(text=f"${grand_total:.2f}")

def complete_sale(date_entry, customer_entry, summary_table):
    date = date_entry.get()
    customer = customer_entry.get()

    for child in summary_table.get_children():
        item, quantity, unit_price, total_price = summary_table.item(child, 'values')
        sales_records.append([date, customer, item, quantity, float(unit_price[1:]), float(total_price[1:])])

    save_sales()

    date_entry.delete(0, tk.END)
    customer_entry.delete(0, tk.END)
    for child in summary_table.get_children():
        summary_table.delete(child)

    messagebox.showinfo("Success", "Sales recorded successfully!")

# Load sales and items data on start
load_sales()
load_items()


