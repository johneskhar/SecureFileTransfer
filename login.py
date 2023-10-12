# login_gui.py
import tkinter as tk
from tkinter import messagebox
from user_management import UserManagement

class LoginApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")

        self.label_username = tk.Label(self.root, text="Username:")
        self.label_username.pack()
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack()

        self.label_password = tk.Label(self.root, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack()

        self.login_button = tk.Button(self.root, text="Login", command=self.login_user)
        self.login_button.pack()

    def login_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Both username and password are required.")
            return

        # Initialize UserManagement class to interact with the MySQL database
        user_manager = UserManagement()
        user = user_manager.login_user(username, password)

        if user:
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

        user_manager.close_db()

if __name__ == "__main__":
    app = LoginApp()
    app.root.mainloop()
