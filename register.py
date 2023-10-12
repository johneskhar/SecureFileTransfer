# register_gui.py
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from user_management import UserManagement

class RegistrationApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registration")

        # Set window dimensions and center it (as shown in previous response)
        window_width = 400
        window_height = 300
        x_coordinate = (self.root.winfo_screenwidth() - window_width) // 2
        y_coordinate = (self.root.winfo_screenheight() - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Create and center the frame for content
        content_frame = tk.Frame(self.root)
        content_frame.pack(expand=True)  # Make the frame expand to fill the window

        # Username label and entry
        self.label_username = tk.Label(content_frame, text="Username:")
        self.label_username.pack(pady=5)  # Add padding to top

        self.entry_username = tk.Entry(content_frame)
        self.entry_username.pack(pady=5)  # Add padding to top

        # Password label and entry
        self.label_password = tk.Label(content_frame, text="Password:")
        self.label_password.pack(pady=5)  # Add padding to top

        self.entry_password = tk.Entry(content_frame, show="*")
        self.entry_password.pack(pady=5)  # Add padding to top

        # Register button
        self.register_button = tk.Button(content_frame, text="Register", command=self.register_user)
        self.register_button.pack(pady=10)  # Add padding to top and bottom

    def register_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Both username and password are required.")
            return

        # Initialize UserManagement class to interact with the MySQL database
        user_manager = UserManagement()

        if user_manager.register_user(username, password):
            messagebox.showinfo("Success", "Registration successful!")
        else:
            messagebox.showerror("Error", "Registration failed.")

        user_manager.close_db()

if __name__ == "__main__":
    app = RegistrationApp()
    app.root.mainloop()
