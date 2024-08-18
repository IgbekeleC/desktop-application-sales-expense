import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import datetime

items = {}

# Function to load items from the CSV file
def load_items():
    global items
    try:
        with open('items.csv', mode='r') as file:
            reader = csv.reader(file)
            items = {}
            for rows in reader:
                if len(rows) >= 3:  # Ensure there are at least three elements (Item Name, Quantity, Unit Price)
                    item_name = rows[0]
                    quantity = int(rows[1])
                    unit_price = float(rows[2])
                    date_added = rows[3] if len(rows) > 3 else datetime.today().strftime('%Y-%m-%d')  # Handle cases where Date Added might be missing
                    items[item_name] = [quantity, unit_price, date_added]
                else:
                    # Handle cases where the row is improperly formatted
                    messagebox.showerror("Data Error", f"Row in items.csv is improperly formatted: {rows}")
    except FileNotFoundError:
        messagebox.showwarning("File Not Found", "items.csv not found, initializing with empty inventory.")
        items = {}

# Function to save items to the CSV file
def save_items():
    with open('items.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for item, details in items.items():
            writer.writerow([item, details[0], details[1], details[2]])

# Function to create the Inventory Management section
def create_inventory_management_section(parent):
    inventory_frame = tk.LabelFrame(parent, text="Inventory Management")
    inventory_frame.pack(fill="both", expand="yes", padx=10, pady=10)

    tk.Label(inventory_frame, text="Item Name").grid(row=0, column=0)
    tk.Label(inventory_frame, text="Quantity").grid(row=1, column=0)
    tk.Label(inventory_frame, text="Unit Price").grid(row=2, column=0)
    tk.Label(inventory_frame, text="Date Added").grid(row=3, column=0)

    item_name_entry = tk.Entry(inventory_frame)
    quantity_entry = tk.Entry(inventory_frame)
    unit_price_entry = tk.Entry(inventory_frame)
    date_added_entry = tk.Entry(inventory_frame)
    date_added_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))  # Default to today's date

    item_name_entry.grid(row=0, column=1)
    quantity_entry.grid(row=1, column=1)
    unit_price_entry.grid(row=2, column=1)
    date_added_entry.grid(row=3, column=1)

    # Buttons
    tk.Button(inventory_frame, text="Add Item", 
              command=lambda: add_item(item_name_entry, quantity_entry, unit_price_entry, date_added_entry)).grid(row=4, column=0, columnspan=2)

    tk.Button(inventory_frame, text="Update Item", 
              command=update_item).grid(row=5, column=0, columnspan=2)

    tk.Button(inventory_frame, text="Remove Item", 
              command=lambda: remove_item(item_name_entry)).grid(row=6, column=0, columnspan=2)

    tk.Button(inventory_frame, text="View Inventory", 
              command=view_inventory).grid(row=7, column=0, columnspan=2)

# Function to add new items to the inventory
def add_item(item_name_entry, quantity_entry, unit_price_entry, date_added_entry):
    item_name = item_name_entry.get().strip()
    quantity = int(quantity_entry.get().strip())
    unit_price = float(unit_price_entry.get().strip())
    date_added = date_added_entry.get().strip()

    if item_name == "":
        messagebox.showerror("Error", "Item Name cannot be empty!")
        return

    if item_name in items:
        messagebox.showerror("Error", f"Item '{item_name}' already exists in inventory! Use the Update button to modify it.")
        return

    items[item_name] = [quantity, unit_price, date_added]  # Add new item
    save_items()

    item_name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    unit_price_entry.delete(0, tk.END)
    date_added_entry.delete(0, tk.END)

    messagebox.showinfo("Success", f"Item '{item_name}' added successfully!")

# Function to remove items from the inventory
def remove_item(item_name_entry):
    item_name = item_name_entry.get().strip()

    if item_name in items:
        del items[item_name]  # Remove the item from inventory
        save_items()
        messagebox.showinfo("Success", f"Item '{item_name}' removed successfully!")
    else:
        messagebox.showerror("Error", f"Item '{item_name}' does not exist in inventory!")

    item_name_entry.delete(0, tk.END)

# Function to view current inventory in a pop-up window
def view_inventory():
    inventory_window = tk.Toplevel()
    inventory_window.title("Current Inventory")

    columns = ("Item Name", "Quantity", "Unit Price", "Date Added", "Subtotal")
    tree = ttk.Treeview(inventory_window, columns=columns, show="headings")
    tree.heading("Item Name", text="Item Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Unit Price", text="Unit Price")
    tree.heading("Date Added", text="Date Added")
    tree.heading("Subtotal", text="Subtotal")

    for item_name, details in items.items():
        subtotal = details[0] * details[1]
        tree.insert("", tk.END, values=(item_name, details[0], f"${details[1]:.2f}", details[2], f"${subtotal:.2f}"))

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(inventory_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

# Function to update existing items in the inventory
def update_item():
    update_window = tk.Toplevel()
    update_window.title("Update Inventory")

    columns = ("Item Name", "Quantity", "Unit Price", "Date Added")
    tree = ttk.Treeview(update_window, columns=columns, show="headings")
    tree.heading("Item Name", text="Item Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Unit Price", text="Unit Price")
    tree.heading("Date Added", text="Date Added")

    for item_name, details in items.items():
        tree.insert("", tk.END, text=item_name, values=(details[0], f"${details[1]:.2f}", details[2]))

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(update_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def on_item_selected(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item[0], "text")
            details = items[item]

            # Pre-fill the entries with the selected item's details
            item_name_entry.delete(0, tk.END)
            item_name_entry.insert(0, item)
            quantity_entry.delete(0, tk.END)
            quantity_entry.insert(0, details[0])
            unit_price_entry.delete(0, tk.END)
            unit_price_entry.insert(0, details[1])
            date_added_entry.delete(0, tk.END)
            date_added_entry.insert(0, details[2])

    tree.bind("<<TreeviewSelect>>", on_item_selected)

    # Entries for editing the selected item
    tk.Label(update_window, text="Item Name").pack(pady=5)
    item_name_entry = tk.Entry(update_window)
    item_name_entry.pack(pady=5)

    tk.Label(update_window, text="Quantity").pack(pady=5)
    quantity_entry = tk.Entry(update_window)
    quantity_entry.pack(pady=5)

    tk.Label(update_window, text="Unit Price").pack(pady=5)
    unit_price_entry = tk.Entry(update_window)
    unit_price_entry.pack(pady=5)

    tk.Label(update_window, text="Date Added").pack(pady=5)
    date_added_entry = tk.Entry(update_window)
    date_added_entry.pack(pady=5)

    def save_updates():
        item_name = item_name_entry.get().strip()
        quantity = int(quantity_entry.get().strip())
        unit_price = float(unit_price_entry.get().strip())
        date_added = date_added_entry.get().strip()

        if item_name == "":
            messagebox.showerror("Error", "Item Name cannot be empty!")
            return

        selected_item = tree.selection()
        if selected_item:
            original_item_name = tree.item(selected_item[0], "text")

            # Update the item in the inventory
            if original_item_name in items:
                del items[original_item_name]  # Remove the old item if the name has changed

            items[item_name] = [quantity, unit_price, date_added]
            save_items()

            messagebox.showinfo("Success", f"Item '{item_name}' updated successfully!")

            update_window.destroy()  # Close the update window after saving

    tk.Button(update_window, text="Save Changes", command=save_updates).pack(pady=20)

# Load items when the module is imported
load_items() 
