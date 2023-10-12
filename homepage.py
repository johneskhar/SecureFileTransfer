from tkinter import *
from tkinter import messagebox
import subprocess

# Function to handle logout
def logout():
    confirmation = messagebox.askyesno("Logout", "Are you sure you want to log out?")
    if confirmation:
        window.destroy()
        subprocess.Popen(["C:/Users/calie/AppData/Local/Microsoft/WindowsApps/python.exe", "C:/Users/calie/PycharmProjects/FYP_Test1/loginuser.py"])

# Create the main window
window = Tk()
window.title("Homepage")
window.geometry('925x500+300+200')
window.configure(bg='light green')
window.resizable(False, False)

# Create a frame for the side panel
side_panel = Frame(window, bg='white')  # Customize the background color
side_panel.pack(side=LEFT, fill=Y)

# Define the username_label as a global variable
username_label = Label(side_panel, text="Username", fg="white", bg="#333", font=("Arial", 14))
username_label.pack(pady=20, padx=10, anchor=W)

# Global variable to store the username
current_username = ""

# Function to update the username label
def update_username_label():
    username_label.config(text=current_username)

# Function to open the homepage with the username argument
def open_homepage(username):
    global current_username
    current_username = username  # Set the global variable
    update_username_label()  # Update the label with the new username

# Create clickable sections for Encrypt/Decrypt Files, Encrypted Files, and Decrypted Files
encrypt_decrypt_button = Button(side_panel, text="Encrypt/Decrypt Files", bg='#57a1f8', fg="white", font=("Arial", 12))
encrypt_decrypt_button.pack(padx=10, pady=10, fill=X)

# Create clickable sections for Encrypted Files and Decrypted Files
encrypted_files_button = Button(side_panel, text="Encrypted Files", bg='#57a1f8', fg="white", font=("Arial", 12))
encrypted_files_button.pack(padx=10, pady=10, fill=X)

decrypted_files_button = Button(side_panel, text="Decrypted Files", bg='#57a1f8', fg="white", font=("Arial", 12))
decrypted_files_button.pack(padx=10, pady=10, fill=X)

# Function to handle clicks on the Encrypt/Decrypt Files button
def open_encrypt_decrypt():
    # Add your code to open the encrypt/decrypt files section
    pass

encrypt_decrypt_button.config(command=open_encrypt_decrypt)

# Function to handle clicks on the Encrypted Files button
def open_encrypted_files():
    # Add your code to open the encrypted files section
    pass

encrypted_files_button.config(command=open_encrypted_files)

# Function to handle clicks on the Decrypted Files button
def open_decrypted_files():
    # Add your code to open the decrypted files section
    pass

decrypted_files_button.config(command=open_decrypted_files)

# Create a logout button at the bottom of the side panel
logout_button = Button(side_panel, text="Logout", bg='#57a1f8', fg="white", font=("Arial", 14), command=logout)
logout_button.pack(side=BOTTOM, fill=X)

# Start the GUI main loop
window.mainloop()
