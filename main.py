import tkinter as tk
from tkinter import messagebox
from user_management import UserManagement  # Import the UserManagement class from user_management.py

class SecureFileTransferApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Secure File Transfer")
        self.current_user = None
        self.user_manager = UserManagement()  # Initialize the UserManagement class

        # Create a login window
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=20, pady=20)

        self.label_username = tk.Label(self.login_frame, text="Username:")
        self.label_username.pack()
        self.entry_username = tk.Entry(self.login_frame)
        self.entry_username.pack()

        self.label_password = tk.Label(self.login_frame, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self.login_frame, show="*")
        self.entry_password.pack()

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Both username and password are required.")
            return

        user = self.user_manager.login_user(username, password)

        if user:
            self.current_user = user
            messagebox.showinfo("Success", "Login successful!")
            # You can add code here to transition to the main menu or other parts of your application.
        else:
            messagebox.showerror("Error", "Invalid username or password.")

if __name__ == "__main__":
    app = SecureFileTransferApp()
    app.root.mainloop()
