import subprocess
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, simpledialog
from tkinter import Label, Listbox, Button
from datetime import datetime
import os
from user_management import UserManagement
import sys
import database
import file_operations
from database import get_encrypted_files, get_decrypted_files
from file_operations import download_file
import shutil
from database import delete_file


# Declare content_frame as a global variable
global content_frame

# Database configuration
db_config = {
    "host": "localhost",
    "port": "3306",
    "user": "root",
    "password": "johnes24",
    "database": "secure_file_transfer",
}

# Create an instance of UserManagement
user_manager = UserManagement(db_config)

# Retrieve the username argument
username = sys.argv[1] if len(sys.argv) > 1 else "Guest"
print(f"Username received in homepage.py: {username}")

# Function to handle logout
def logout(window):
    confirmation = messagebox.askyesno("Logout", "Are you sure you want to log out?")
    if confirmation:
        window.destroy()
        sys.exit()

# Function to open the homepage with the username argument
def open_homepage(username, login_window):
    global content_frame  # Declare content_frame as global

    print("Opening homepage...")

    # Assuming you have an instance of UserManagement
    user_manager = UserManagement(db_config)  # Initialize UserManagement instance with db_config

    # Get the user ID based on the provided username
    user_id = user_manager.get_user_id_by_username(username)

    if user_id is not None:
        print(f"User ID for {username}: {user_id}")
    else:
        print(f"No user found with the username: {username}")
        return

    # Create the main window
    window = Tk()
    window.title("Homepage")
    window.geometry('925x500+300+200')
    window.configure(bg='light blue')
    window.resizable(False, False)

    # Create a frame for the side panel
    side_panel = Frame(window, bg='white')
    side_panel.pack(side=LEFT, fill=Y)

    # Define the username_label as a global variable
    username_label = Label(side_panel, text=f"Welcome, {username}!", fg="black", bg="white", font=("Arial", 14))
    username_label.pack(pady=20, padx=10, anchor=W)

    # Create clickable sections for Encrypt/Decrypt Files, Encrypted Files, and Decrypted Files
    encrypt_decrypt_button = Button(side_panel, text="Encrypt/Decrypt Files", bg='#57a1f8', fg="white",
                                    font=("Arial", 12), command=encrypt_decrypt_page)
    encrypt_decrypt_button.pack(padx=10, pady=10, fill=X)

    encrypted_files_button = Button(side_panel, text="Encrypted Files", bg='#57a1f8', fg="white", font=("Arial", 12),
                                    command=lambda: open_encrypted_files(user_id))
    encrypted_files_button.pack(padx=10, pady=10, fill=X)

    decrypted_files_button = Button(side_panel, text="Decrypted Files", bg='#57a1f8', fg="white", font=("Arial", 12),
                                    command=lambda: open_decrypted_files(user_id))
    decrypted_files_button.pack(padx=10, pady=10, fill=X)

    # Create a logout button at the bottom of the side panel
    logout_button = Button(side_panel, text="Logout", bg='#57a1f8', fg="white", font=("Arial", 14), command=lambda: logout(window))
    logout_button.pack(side=BOTTOM, fill=X)

    # Create a frame to hold the content (center of the window)
    content_frame = Frame(window, bg='light blue')
    content_frame.pack(expand=True, fill=BOTH)  # Use BOTH to allow expansion in both directions

    # Start the GUI main loop
    window.mainloop()

    # Ensure that the login window is destroyed after opening the homepage window
    login_window.destroy()

    # Call the encrypt_file_operation function with the username
    encrypt_file_operation(username)
    decrypt_file_operation(username)
    # Call the function to open the Encrypted Files page
    open_encrypted_files(user_id)


# Function to handle success pop-up
def show_success_popup(action, file_path):
    messagebox.showinfo("Success", f"File {action}ed successfully. Path: {file_path}")


def get_password_from_user():
    password = simpledialog.askstring("Password", "Enter password:", show='*')
    return password


# Function to create the content for Encrypt/Decrypt Files page
def encrypt_decrypt_page():
    global selected_file_label  # Declare as global to update text in select_file function

    # Clear existing content
    clear_content_frame(content_frame)

    # Create a title label
    title_label = Label(content_frame, text="Encrypt/Decrypt Files", bg='light blue', font=("Arial", 16, "bold"))
    title_label.pack(pady=(100, 50))

    # Create a "Select File" button
    select_file_button = Button(content_frame, text="Select File", command=select_file_op, bg='green',
                                fg='white', width=15, height=1, font=("Arial", 12))
    select_file_button.pack(pady=20)

    # Create a label to display the selected file
    selected_file_label = Label(content_frame, text="", bg='light blue', font=("Arial", 11))
    selected_file_label.pack()

    # Create a frame for the "Encrypt" and "Decrypt" buttons
    buttons_frame = Frame(content_frame, bg='light blue')
    buttons_frame.pack()

    # Create "Encrypt File" and "Decrypt File" buttons side by side
    global encrypt_button, decrypt_button
    encrypt_button = Button(buttons_frame, text="Encrypt File", command=encrypt_file_operation, bg='blue',
                            fg='white', state=DISABLED, width=15, height=1, font=("Arial", 12))
    decrypt_button = Button(buttons_frame, text="Decrypt File", command=decrypt_file_operation, bg='blue',
                            fg='white', state=DISABLED, width=15, height=1, font=("Arial", 12))
    encrypt_button.grid(row=0, column=0, padx=5)
    decrypt_button.grid(row=0, column=1, padx=5)


# Function to open the file dialog and process the selected file
def select_file_op():
    global selected_file_label
    selected_file_path = filedialog.askopenfilename()
    if selected_file_path:
        # Display the selected file
        selected_file_label.config(text=selected_file_path)
        encrypt_button.config(state=NORMAL)  # Enable the "Encrypt File" button
        decrypt_button.config(state=NORMAL)  # Enable the "Decrypt File" button
    else:
        # Show an error popup when no file is selected
        messagebox.showerror("Error", "No file selected.")


# Function to handle success pop-up
def show_success_popup(action, file_path):
    messagebox.showinfo("Success", f"File {action}ed successfully. Path: {file_path}")


def encrypt_file_operation():
    global selected_file_label

    if selected_file_label is None:
        messagebox.showerror("Error", "No file selected.")
        return

    input_file = selected_file_label.cget("text")
    if input_file == "":
        messagebox.showerror("Error", "No file selected.")
        return

    password = get_password_from_user()

    # Get the logged-in user's username
    global username

    # Get the logged-in user's user ID
    user_id = user_manager.get_user_id_by_username(username)

    encrypted_file_path = file_operations.encrypt_file_op(input_file, password, user_id)
    messagebox.showinfo("Success", f"File successfully encrypted. Saved at: {encrypted_file_path}")


def decrypt_file_operation():
    input_file = selected_file_label.cget("text")
    if input_file == "":
        messagebox.showerror("Error", "No file selected.")
        return

    # Ask for the password
    password = get_password_from_user()

    try:
        # Get the user ID based on the provided username
        user_id = user_manager.get_user_id_by_username(username)

        # Decrypt the file with the provided input_file, password, and user_id
        decrypted_file_path = file_operations.decrypt_file_op(input_file, password, user_id)

        if decrypted_file_path is not None:
            # Show success message with the decrypted file path
            messagebox.showinfo("Success", f"File successfully decrypted. Saved at: {decrypted_file_path}")
        else:
            # Show error message for incorrect password
            messagebox.showerror("Error", "Incorrect password.")

    except ValueError as e:
        # Show an error message for incorrect password
        messagebox.showerror("Error", str(e))



# Function to clear content frame
def clear_content_frame(content_frame):
    # Destroy all widgets in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()


# Function to open the Encrypted Files page
def open_encrypted_files(user_id):
    try:
        print("Opening encrypted files page...")
        # Pass both the user_id and content_frame to open_encrypted_files_page
        clear_content_frame(content_frame)  # Clear the content frame
        open_encrypted_files_page(user_id)
    except Exception as e:
        print("Error opening encrypted files page:", e)


# Function to open the Decrypted Files page
def open_decrypted_files(user_id):
    try:
        print("Opening decrypted files page...")
        # Pass both the user_id and content_frame to open_decrypted_files_page
        clear_content_frame(content_frame)  # Clear the content frame
        open_decrypted_files_page(user_id)
    except Exception as e:
        print("Error opening decrypted files page:", e)


# Function to open the Encrypted Files page
def open_encrypted_files_page(user_id):
    try:
        print("Opening encrypted files page...")

        # Get the user ID for the logged-in user
        user_id = user_manager.get_user_id_by_username(username)

        # Get encrypted files for the current user
        encrypted_files = database.get_files_by_user_id(user_id, is_encrypted=True)
        # Clear existing widgets in content_frame
        clear_content_frame(content_frame)

        # Create a title label
        title_label = Label(content_frame, text="Encrypted Files", bg='light blue', font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Create a frame to hold the listbox
        list_frame = Frame(content_frame, bg='light blue')
        list_frame.pack(expand=True, fill='both')

        # Create a listbox to display encrypted files
        files_listbox = Listbox(list_frame, height=15)
        files_listbox.pack(expand=True, fill='both')

        for file_id, file_path, date_encrypted in encrypted_files:
            files_listbox.insert(END, f"{file_path} - {date_encrypted}")

        # Button to download the selected file
        download_button = tk.Button(content_frame, text="Download",
                                    command=lambda: download_selected_file(files_listbox))
        download_button.pack()

        is_encrypted = True

        # Button to delete the selected file
        delete_button = Button(content_frame, text="Delete", command=lambda: delete_file(
            files_listbox.get(files_listbox.curselection()), is_encrypted))
        delete_button.pack()

    except Exception as e:
        print("Error opening encrypted files page:", e)


# Function to open the Decrypted Files page
def open_decrypted_files_page(user_id):
    try:
        print("Opening decrypted files page...")

        # Get the user ID for the logged-in user
        user_id = user_manager.get_user_id_by_username(username)

        # Get decrypted files for the current user
        decrypted_files = database.get_files_by_user_id(user_id, is_encrypted=False)
        # Clear existing widgets in content_frame
        clear_content_frame(content_frame)

        # Create a title label
        title_label = Label(content_frame, text="Decrypted Files", bg='light blue', font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Create a frame to hold the listbox
        list_frame = Frame(content_frame, bg='light blue')
        list_frame.pack(expand=True, fill='both')

        # Create a listbox to display encrypted files
        files_listbox = Listbox(list_frame, height=10)
        files_listbox.pack(expand=True, fill='both')

        for file_id, file_path, date_decrypted in decrypted_files:
            files_listbox.insert(END, f"{file_path} - {date_decrypted}")

        # Button to download the selected file
        # Create the "Download" button
        download_button = tk.Button(content_frame, text="Download",
                                    command=lambda: download_selected_file(files_listbox))
        download_button.pack()

        is_encrypted = False
        # Button to delete the selected file
        delete_button = Button(content_frame, text="Delete", command=lambda: delete_file(
            files_listbox.get(files_listbox.curselection()), is_encrypted))
        delete_button.pack()

    except Exception as e:
        print("Error opening decrypted files page:", e)


# Function to download the selected file
def download_selected_file(files_listbox):
    try:
        # Get the selected file from the listbox
        selected_file_with_date = files_listbox.get(tk.ACTIVE)

        # Parse the file name and date from the selected file path
        selected_file_parts = selected_file_with_date.split(" - ")
        if len(selected_file_parts) == 2:
            selected_file = selected_file_parts[0]
        else:
            # If the file name does not contain a date, use the entire selected file path
            selected_file = selected_file_with_date

        # Check if the selected file exists
        if os.path.exists(selected_file):
            # Open a file dialog to choose the destination folder
            default_download_dir = "C:/Users/calie/Downloads"
            destination_folder = filedialog.askdirectory(initialdir=default_download_dir)

            # If a destination folder is selected, download the file to that folder
            if destination_folder:
                try:
                    # Copy the file to the destination folder
                    shutil.copy(selected_file, destination_folder)
                    messagebox.showinfo("Success", f"File downloaded successfully to {destination_folder}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error downloading file: {e}")
            else:
                # If no destination folder is selected, show an error message
                messagebox.showerror("Error", "No destination folder selected.")
        else:
            # If the selected file does not exist, show an error message
            messagebox.showerror("Error", f"The selected file does not exist: {selected_file}")

    except Exception as e:
        print("Error downloading file:", e)
        messagebox.showerror("Error", f"Error downloading file: {e}")


# Call the function to open the homepage after successful login
open_homepage(username, None)
