import tkinter as tk
from tkinter import messagebox, ttk
from auth import save_users
import csv
import os  # Import os module to check if file exists

# Initialize users
users = {}

def load_users(file_path="users.csv"):
    global users
    if not os.path.exists(file_path):
        messagebox.showwarning("File Not Found", "users.csv not found, initializing with empty user database.")
        users = {}
        save_users(file_path)  # Create the file with default content
    else:
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                users = {row['Username']: {'password': row['Password'], 'role': row['Role'], 'status': row['Status']} for row in reader}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {e}")
            users = {}  # Initialize with empty dictionary if loading fails

def save_users(file_path="users.csv"):
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Password", "Role", "Status"])
            for username, details in users.items():
                writer.writerow([username, details['password'], details['role'], details['status']])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save users: {e}")


#ALTERNATIVE OR ANOTHER OPTION

def create_user_management_section(parent):
    user_management_frame = tk.LabelFrame(parent, text="User Management")
    user_management_frame.pack(fill="both", expand="yes", padx=10, pady=10)

    tk.Label(user_management_frame, text="Username").grid(row=0, column=0)
    username_entry = tk.Entry(user_management_frame)
    username_entry.grid(row=0, column=1)

    tk.Label(user_management_frame, text="Password").grid(row=1, column=0)
    password_entry = tk.Entry(user_management_frame, show='*')
    password_entry.grid(row=1, column=1)

    # Replaced role selection with the Roles button
    roles_button = tk.Button(user_management_frame, text="Roles", command=open_roles_dialog)
    roles_button.grid(row=2, column=0, columnspan=2)

    tk.Button(user_management_frame, text="Create User", command=lambda: create_user(username_entry, password_entry)).grid(row=3, column=0, columnspan=2)
    tk.Button(user_management_frame, text="Update User", command=update_user).grid(row=4, column=0, columnspan=2)
    tk.Button(user_management_frame, text="View Users", command=view_users).grid(row=5, column=0, columnspan=2)

def open_roles_dialog():
    global role_vars, dialog
    dialog = tk.Toplevel()
    dialog.title("Assign Roles")

    role_names = [
        "View",
        "Write",
        "Read",
        "Add",
        "Create",
        "Update", 
        "Delete",
        "Admin"
    ]
    #global role_vars
    role_vars = {}

    # Create a Checkbutton for each role
    for i, role in enumerate(role_names):
        var = tk.BooleanVar()
        checkbutton = tk.Checkbutton(dialog, text=role, variable=var)
        checkbutton.pack(anchor="w")
        role_vars[role] = var

    # Add a button to confirm role assignment
    assign_button = tk.Button(dialog, text="Assign Roles", command=assign_roles)
    assign_button.pack(pady=10)

def assign_roles():
    global selected_roles
    selected_roles = [role for role, var in role_vars.items() if var.get()]
    if selected_roles:
        messagebox.showinfo("Assigned Roles", f"Roles assigned: {', '.join(selected_roles)}")
        dialog.destroy()  # Close the role dialog after roles are assigned
    else:
        messagebox.showwarning("No Selection", "No roles selected!")

def create_user(username_entry, password_entry):
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    selected_roles = [role for role, var in role_vars.items() if var.get()]
    roles_str = ', '.join(selected_roles)  # Convert list to a comma-separated string
    users[username] = {'password': password, 'role': roles_str, 'status': 'active'}

    if not username or not password:
        messagebox.showerror("Error", "Username and Password cannot be empty.")
        return

    if username in users:
        messagebox.showerror("Error", "User already exists.")
    else:
        users[username] = {'password': password, 'roles': selected_roles, 'status': 'active'}
        save_users()
        messagebox.showinfo("Success", f"User {username} created successfully with roles: {', '.join(selected_roles)}")

    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


def update_user():
    update_window = tk.Toplevel()
    update_window.title("Update User")

    columns = ("Username", "Password", "Role", "Status")
    tree = ttk.Treeview(update_window, columns=columns, show="headings")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")
    tree.heading("Role", text="Role")
    tree.heading("Status", text="Status")

    for username, details in users.items():
        tree.insert("", tk.END, text=username, values=(details['password'], details['role'], details['status']))

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(update_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Entries for editing the selected user
    tk.Label(update_window, text="Username").pack(pady=5)
    username_entry = tk.Entry(update_window)
    username_entry.pack(pady=5)

    tk.Label(update_window, text="Password").pack(pady=5)
    password_entry = tk.Entry(update_window, show='*')
    password_entry.pack(pady=5)

    tk.Label(update_window, text="Role").pack(pady=5)
    role_entry = ttk.Combobox(update_window, values=["View Only", "Write Only", "Read, Write, Update, Delete"])
    role_entry.pack(pady=5)

    tk.Label(update_window, text="Status").pack(pady=5)
    status_entry = ttk.Combobox(update_window, values=["active", "inactive"])
    status_entry.pack(pady=5)

    def on_item_selected(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item[0], "text")
            details = users[item]

            username_entry.delete(0, tk.END)
            username_entry.insert(0, item)
            password_entry.delete(0, tk.END)
            password_entry.insert(0, details['password'])
            role_entry.set(details['role'])
            status_entry.set(details['status'])

    tree.bind("<<TreeviewSelect>>", on_item_selected)

    def save_updates():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        role = role_entry.get()
        status = status_entry.get()

        if username == "":
            messagebox.showerror("Error", "Username cannot be empty!")
            return

        selected_item = tree.selection()
        if selected_item:
            original_username = tree.item(selected_item[0], "text")

            if original_username in users:
                del users[original_username]  # Remove the old user if the username has changed

            users[username] = {'password': password, 'role': role, 'status': status}
            save_users()

            messagebox.showinfo("Success", f"User '{username}' updated successfully!")
            update_window.destroy()

    tk.Button(update_window, text="Save Changes", command=save_updates).pack(pady=20)
    tk.Button(update_window, text="Delete User", command=lambda: delete_user(tree)).pack(pady=5)


def delete_user(tree):
    selected_item = tree.selection()
    if selected_item:
        username = tree.item(selected_item[0], "text")
        if username in users:
            del users[username]
            save_users()
            messagebox.showinfo("Success", f"User '{username}' deleted successfully!")
            tree.delete(selected_item[0])
        else:
            messagebox.showerror("Error", "User not found!")

def view_users():
    view_window = tk.Toplevel()
    view_window.title("View Users")

    columns = ("Username", "Role", "Status")
    tree = ttk.Treeview(view_window, columns=columns, show="headings")
    tree.heading("Username", text="Username")
    tree.heading("Role", text="Role")
    tree.heading("Status", text="Status")

    for username, details in users.items():
        tree.insert("", tk.END, values=(username, details['role'], details['status']))

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

def save_users():
    # This is a placeholder function where you would save the users to a file or database.
    print("Users saved:", users)

# Load users when the module is imported
load_users()  





