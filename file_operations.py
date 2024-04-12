from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import pyAesCrypt
from tkinter import filedialog, simpledialog
import database
from datetime import datetime
import shutil
from tkinter import messagebox
import webbrowser
import file_operations
connection = database.get_database_connection()

#fixed_key = b'\xc0\xa7\xf5\x90\xec7P\xb0)\xe1\xd9\x83\xc4G$~'


def select_file():
    file_path = filedialog.askopenfilename()
    return file_path


def encrypt_file_op(file_path, password, user_id):
    output_path = file_path + ".enc"
    buffer_size = 64 * 1024

    with open(file_path, 'rb') as input_file, open(output_path, 'wb') as output_file:
        pyAesCrypt.encryptStream(input_file, output_file, password, buffer_size)

    date_encrypted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database.save_encrypted_file_info(user_id, output_path, date_encrypted)

    return output_path

def decrypt_file_op(file_path, password, user_id):
    try:
        output_path = file_path.replace(".enc", "")
        pyAesCrypt.decryptFile(file_path, output_path, password, 64 * 1024)

        date_decrypted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        database.save_decrypted_file_info(user_id, output_path, date_decrypted)

        return output_path

    except ValueError:
        print("Incorrect password")
        return None
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

def encrypt_file_button():
    file_path = select_file()
    password = simpledialog.askstring("Enter password", "Enter the password to encrypt the file")
    encrypted_file_path = encrypt_file_op(file_path, password)
    return encrypted_file_path

def decrypt_file_button():
    file_path = select_file()
    password = simpledialog.askstring("Enter password", "Enter the password to decrypt the file")
    decrypted_file_path = decrypt_file_op(file_path, password)
    return decrypted_file_path

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=os.urandom(16))
    cipher_text = cipher.encrypt(pad(data, AES.block_size))
    return cipher_text


def decrypt_data(cipher_text, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(cipher_text), AES.block_size)
    return decrypted_data


# Function to save encrypted file information in the database
def save_encrypted_file_info(user_id, file_path, date_encrypted):
    database.save_encrypted_file_info(file_path, date_encrypted)


# Function to save decrypted file information in the database
def save_decrypted_file_info(user_id, file_path, date_decrypted):
    upload_file(user_id, file_path, is_encrypted=False, date_decrypted=date_decrypted)


def upload_file(user_id, file_path, is_encrypted=True):
    try:
        # Insert the file information into the corresponding table with user_id
        table_name = "encrypted_files" if is_encrypted else "decrypted_files"
        database.insert_file_info(user_id, file_path, table_name)

    except Exception as e:
        # Handle exceptions and show an error message
        print(f"Error uploading file: {e}")
        raise e  # Propagate the exception back to the calling function


# Function to get all encrypted files
def get_encrypted_files():
    return database.get_files_by_user_id(database.get_current_user_id(), is_encrypted=True)


# Function to get all decrypted files
def get_decrypted_files():
    return database.get_files_by_user_id(database.get_current_user_id(), is_encrypted=False)


# Function to download a file
def download_file(file_path, destination_folder):
    try:
        # Copy the file to the destination folder
        shutil.copyfile(file_path, os.path.join(destination_folder, os.path.basename(file_path)))
        print("File downloaded successfully.")
    except Exception as e:
        print(f"Error downloading file: {e}")




