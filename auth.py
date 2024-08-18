import csv
import tkinter as tk
from tkinter import messagebox
import os

users = {}

def load_users(file_path="users.csv"):
    global users
    if os.path.exists(file_path):
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                users = {row['Username']: {'password': row['Password'], 'role': row['Role'], 'status': row['Status']} for row in reader}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {e}")
            users = {}  # Initialize with empty dictionary if loading fails
    else:
        # Initialize with default user if file does not exist
        users = {"admin": {"password": "password123", "role": "Read, Write, Update, Delete", "status": "active"}}
        save_users(file_path)  # Create the file with default user

def save_users(file_path="users.csv"):
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Password", "Role", "Status"])
            for username, details in users.items():
                writer.writerow([username, details['password'], details['role'], details['status']])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save users: {e}")

def login(username, password):
    if username in users and users[username]['password'] == password:
        return True
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
        return False

def logout():
    messagebox.showinfo("Logout", "You have been logged out.")
    return True

load_users()  # Load users when the module is imported



