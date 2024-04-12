import tkinter as tk
from tkinter import filedialog
import os
import pyAesCrypt

# Create a new window
root = tk.Tk()
root.title("AES File Encryptor/Decryptor")

# Create a text widget to display information
text_widget = tk.Text(root, height=10, width=50)
text_widget.pack()

# Create a function to select a file
def select_file():
    file_path = filedialog.askopenfilename()
    text_widget.insert(tk.END, f"Selected file: {file_path}\n")
    return file_path

# Create a function to encrypt the file
def encrypt_file():
    file_path = select_file()
    password = tk.simpledialog.askstring("Enter password", "Enter a password to encrypt the file")
    output_path = f"{file_path}_encrypted"
    pyAesCrypt.encryptFile(file_path, output_path, password, 64*1024)
    text_widget.insert(tk.END, f"Encrypted file saved at: {output_path}\n")

# Create a function to decrypt the file
def decrypt_file():
    file_path = select_file()
    password = tk.simpledialog.askstring("Enter password", "Enter the password to decrypt the file")
    output_path = file_path.replace("_encrypted", "")
    pyAesCrypt.decryptFile(file_path, output_path, password, 64*1024)
    text_widget.insert(tk.END, f"Decrypted file saved at: {output_path}\n")

# Create buttons to perform the required operations
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_file)
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_file)
decrypt_button.pack()

# Start the main event loop
root.mainloop()