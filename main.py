import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from auth import login, load_users, save_users
from dashboard import Dashboard
from expenses import load_expenses, save_expenses
from sales import load_sales, save_sales, load_items, save_items
from user_management import load_users as um_load_users

def start_app():
    root = tk.Tk()
    root.geometry("800x600")

    # Load data at the start of the application
    load_expenses()
    load_sales()
    load_items()
    um_load_users()  # Load users from user_management module

    def on_close():
        # Save all data before closing
        save_expenses()
        save_sales()
        save_items()
        save_users()  # Save users without arguments
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Login Frame
    login_frame = tk.Frame(root)
    login_frame.pack(fill="both", expand=True)

    # Load and resize the background image to cover the frame
    image = Image.open("resources/images/bgimg.png")  # Replace with your image path
    image = image.resize((800, 600), Image.Resampling.LANCZOS)  # Use Image.Resampling.LANCZOS instead of ANTIALIAS
    bg_image = ImageTk.PhotoImage(image)

    # Create a Canvas and set the background image
    canvas = tk.Canvas(login_frame, width=800, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=bg_image)

    # Create a frame on top of the canvas to hold the login widgets
    form_frame = tk.Frame(login_frame, bg="#ffffff", padx=20, pady=20)  # White background for better contrast
    canvas.create_window(400, 300, window=form_frame, anchor="center")  # Center the form frame

    # Username and Password labels and entries in the same row
    tk.Label(form_frame, text="Username", bg="#ffffff").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    username_entry = tk.Entry(form_frame)
    username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tk.Label(form_frame, text="Password", bg="#ffffff").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    password_entry = tk.Entry(form_frame, show='*')
    password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    def attempt_login():
        if login(username_entry.get(), password_entry.get()):
            login_frame.pack_forget() # Hide login frame
            
            Dashboard(root)

    tk.Button(form_frame, text="Login", command=attempt_login).grid(row=2, columnspan=2, pady=20)

    root.mainloop()

if __name__ == "__main__":
    start_app()

