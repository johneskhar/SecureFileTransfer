#file_operations.py

def delete_file_by_id(file_id, is_encrypted=True):
    try:
        # Remove the file from the database
        connection = database.get_database_connection()
        cursor = connection.cursor()

        # Determine the table based on the file type
        table_name = "encrypted_files" if is_encrypted else "decrypted_files"

        # Add print statements to check the values
        print(f"Deleting file with ID {file_id} from table {table_name}")

        # Delete the file entry from the corresponding table using file_id
        delete_query = f"DELETE FROM {table_name} WHERE file_id = %s"
        cursor.execute(delete_query, (file_id,))

        # Commit the changes and close the connection
        connection.commit()
        connection.close()

    except Exception as e:
        # Handle exceptions and show an error message
        print(f"Error deleting file: {e}")
        raise e  # Propagate the exception back to the calling function

#homepage.py

def delete_file(file_info, is_encrypted=True):
    try:
        # Check if file_info is a string
        if isinstance(file_info, str):
            # Extract file_id from the string
            parts = file_info.split(': ')
            if len(parts) == 2:
                file_id = parts[0]

                # Delete the file from the database based on the file type
                delete_file_by_id(file_id, is_encrypted)

                messagebox.showinfo("Success", "File deleted successfully.")
            else:
                raise ValueError("Invalid file information format.")
        else:
            messagebox.showerror("Error", "Invalid file information.")

    except Exception as e:
        # Handle exceptions and show an error message
        print(f"Error deleting file: {e}")
        messagebox.showerror("Error", "Failed to delete file.")

# Function to get encrypted files for a specific user
def get_encrypted_files(user_id):
    connection = database.get_database_connection()
    cursor = connection.cursor()

    # Select encrypted files for the user
    select_query = """
    SELECT ef.file_id, ef.file_path, ef.date_encrypted
    FROM encrypted_files ef
    JOIN users u ON ef.user_id = u.user_id
    WHERE u.user_id = %s
    """
    print("Encrypted Files Query:", cursor.mogrify(select_query, (user_id,)))  # Print the formatted query
    cursor.execute(select_query, (user_id,))
    encrypted_files = cursor.fetchall()

    # Print the result for debugging
    print("Encrypted Files:", encrypted_files)

    # Close the connection
    connection.close()

    return encrypted_files

def get_decrypted_files(user_id):
    connection = database.get_database_connection()
    cursor = connection.cursor()

    # Select decrypted files for the user
    select_query = """
    SELECT df.file_id, df.file_path, df.date_decrypted
    FROM decrypted_files df
    JOIN users u ON df.user_id = u.user_id
    WHERE u.user_id = %s
    """
    print("Decrypted Files Query:", cursor.mogrify(select_query, (user_id,)))  # Print the formatted query
    cursor.execute(select_query, (user_id,))
    decrypted_files = cursor.fetchall()

    # Print the result for debugging
    print("Decrypted Files:", decrypted_files)

    # Close the connection
    connection.close()

    return decrypted_files

import subprocess
from tkinter import *
from tkinter import messagebox, filedialog, simpledialog
import file_operations
from tkinter import Listbox, Button
import database
from database import get_encrypted_files, get_decrypted_files
global current_username


# Global variable to store the username
current_username = ""

# Declare selected_file_label as a global variable
selected_file_label = None

# Declare username_label as a global variable
username_label = None

# Function to update the username label
def update_username_label():
    global username_label, current_username
    if username_label:
        username_label.config(text=current_username)

# Function to open the homepage with the username argument
def open_homepage(username):
    global current_username
    current_username = username  # Set the global variable
    update_username_label()  # Update the label with the new username

def get_password_from_user():
    password = simpledialog.askstring("Password", "Enter password:", show='*')
    return password

# Function to get encrypted files for a specific user
def get_encrypted_files(user_id):
    connection = database.get_database_connection()
    cursor = connection.cursor()

    # Select encrypted files for the user
    select_query = "SELECT file_id, file_path, date_encrypted FROM encrypted_files WHERE user_id = %s"
    cursor.execute(select_query, (user_id,))
    encrypted_files = cursor.fetchall()

    # Close the connection
    connection.close()

    return encrypted_files

# Function to handle logout
def logout():
    confirmation = messagebox.askyesno("Logout", "Are you sure you want to log out?")
    if confirmation:
        window.destroy()
        subprocess.Popen(["C:/Users/calie/AppData/Local/Microsoft/WindowsApps/python.exe", "C:/Users/calie/PycharmProjects/FYP_Test1/loginuser.py"])

# Function to create the content for Encrypt/Decrypt Files page
def encrypt_decrypt_page():
    global selected_file_label  # Declare as global to update text in select_file function
    if not hasattr(encrypt_decrypt_page, "first_run"):
        encrypt_decrypt_page.first_run = True

        # Create a title label
        title_label = Label(content_frame, text="Encrypt/Decrypt Files", bg='darkgray', font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Create a "Select File" button
        select_file_button = Button(content_frame, text="Select File", command=select_file_op, bg='green', fg='white', width=15, height=1, font=("Arial", 12))
        select_file_button.pack(pady=20)

        # Create a label to display the selected file
        selected_file_label = Label(content_frame, text="", bg='darkgray', font=("Arial", 11))
        selected_file_label.pack()

        # Create a frame for the "Encrypt" and "Decrypt" buttons
        buttons_frame = Frame(content_frame, bg='darkgray')
        buttons_frame.pack()

        # Create "Encrypt File" and "Decrypt File" buttons side by side
        global encrypt_button, decrypt_button
        encrypt_button = Button(buttons_frame, text="Encrypt File", command=encrypt_file_operation, bg='blue', fg='white', state=DISABLED, width=15, height=1, font=("Arial", 12))
        decrypt_button = Button(buttons_frame, text="Decrypt File", command=decrypt_file_operation, bg='blue', fg='white', state=DISABLED, width=15, height=1, font=("Arial", 12))
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
    input_file = selected_file_label.cget("text")
    if input_file == "":
        messagebox.showerror("Error", "No file selected.")
        return
    password = get_password_from_user()
    encrypted_file_path = file_operations.encrypt_file_op(input_file, password)  # Provide the password
    messagebox.showinfo("Success", f"File successfully encrypted. Saved at: {encrypted_file_path}")

def decrypt_file_operation():
    input_file = selected_file_label.cget("text")
    if input_file == "":
        messagebox.showerror("Error", "No file selected.")
        return

    # Ask for the password
    password = get_password_from_user()

    try:
        decrypted_file_path = file_operations.decrypt_file_op(input_file, password)  # Provide the password
        messagebox.showinfo("Success", f"File successfully decrypted. Saved at: {decrypted_file_path}")

    except ValueError as e:
        # Show an error message for incorrect password
        messagebox.showerror("Error", str(e))

# Function to handle success pop-up
def show_success_popup(action, file_path):
    messagebox.showinfo("Success", f"File {action}ed successfully. Path: {file_path}")

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
    encrypt_decrypt_page()

encrypt_decrypt_button.config(command=open_encrypt_decrypt)

def open_encrypted_files_page():
    # Get encrypted files for the current user
    encrypted_files = get_encrypted_files(current_username)

    # Clear existing widgets in content_frame
    clear_content_frame()

    # Create a title label
    title_label = Label(content_frame, text="Encrypted Files", bg='darkgray', font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Create a frame to hold the listbox
    list_frame = Frame(content_frame, bg='darkgray')
    list_frame.pack(expand=True)

    # Create a listbox to display encrypted files
    files_listbox = Listbox(list_frame)
    files_listbox.pack(expand=True)

    for file_path, date_encrypted in encrypted_files:
        files_listbox.insert(END, f"{file_path} - {date_encrypted}")

    # Button to download the selected file
    download_button = Button(content_frame, text="Download", command=lambda: download_file(files_listbox.get(files_listbox.curselection())))
    download_button.pack()

    # Button to delete the selected file
    delete_button = Button(content_frame, text="Delete", command=lambda: delete_file(files_listbox.get(files_listbox.curselection())))
    delete_button.pack()

def open_decrypted_files_page():
    # Get decrypted files for the current user
    decrypted_files = get_decrypted_files(current_username)

    # Clear existing widgets in content_frame
    clear_content_frame()

    # Create a title label
    title_label = Label(content_frame, text="Decrypted Files", bg='darkgray', font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Create a frame to hold the listbox
    list_frame = Frame(content_frame, bg='darkgray')
    list_frame.pack(expand=True)

    # Create a listbox to display decrypted files
    files_listbox = Listbox(list_frame)
    files_listbox.pack(expand=True)

    for file_path, date_decrypted in decrypted_files:
        files_listbox.insert(END, f"{file_path} - {date_decrypted}")

    # Button to download the selected file
    download_button = Button(content_frame, text="Download", command=lambda: download_file(files_listbox.get(files_listbox.curselection())))
    download_button.pack()

    # Button to delete the selected file
    delete_button = Button(content_frame, text="Delete", command=lambda: delete_file(files_listbox.get(files_listbox.curselection())))
    delete_button.pack()

def clear_content_frame():
    # Destroy all widgets in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

# Function to handle clicks on the Encrypted Files button
def open_encrypted_files():
    open_encrypted_files_page()

encrypted_files_button.config(command=open_encrypted_files)

# Function to handle clicks on the Decrypted Files button
def open_decrypted_files():
    open_decrypted_files_page()

decrypted_files_button.config(command=open_decrypted_files)


# Create a logout button at the bottom of the side panel
logout_button = Button(side_panel, text="Logout", bg='#57a1f8', fg="white", font=("Arial", 14), command=logout)
logout_button.pack(side=BOTTOM, fill=X)

# Create a frame to hold the content (center of the window)
content_frame = Frame(window, bg='white')
content_frame.pack(expand=True)

# Withdraw the window initially
window.withdraw()

# Start the GUI main loop
window.mainloop()


##############################################################

def open_homepage(username):
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

    # Create the main window
    window = Tk()
    window.title("Homepage")
    window.geometry('925x500+300+200')
    window.configure(bg='light blue')
    window.resizable(False, False)


    # Create a frame for the side panel
    side_panel = Frame(window, bg='white')  # Customize the background color
    side_panel.pack(side=LEFT, fill=Y)

    # Define the username_label as a global variable
    username_label = Label(side_panel, text=f"Welcome, {username}!", fg="black", bg="white", font=("Arial", 14))
    username_label.pack(pady=20, padx=10, anchor=W)

    # Create clickable sections for Encrypt/Decrypt Files, Encrypted Files, and Decrypted Files
    encrypt_decrypt_button = Button(side_panel, text="Encrypt/Decrypt Files", bg='#57a1f8', fg="white",
                                    font=("Arial", 12), command=lambda: encrypt_decrypt_page(content_frame))
    encrypt_decrypt_button.pack(padx=10, pady=10, fill=X)

    encrypted_files_button = Button(side_panel, text="Encrypted Files", bg='#57a1f8', fg="white", font=("Arial", 12),
                                    command=lambda: open_encrypted_files(content_frame))
    encrypted_files_button.pack(padx=10, pady=10, fill=X)

    decrypted_files_button = Button(side_panel, text="Decrypted Files", bg='#57a1f8', fg="white", font=("Arial", 12),
                                    command=lambda: open_decrypted_files(content_frame))
    decrypted_files_button.pack(padx=10, pady=10, fill=X)

    # Create a logout button at the bottom of the side panel
    logout_button = Button(side_panel, text="Logout", bg='#57a1f8', fg="white", font=("Arial", 14), command=logout)
    logout_button.pack(side=BOTTOM, fill=X)

    # Create a frame to hold the content (center of the window)
    content_frame = Frame(window, bg='white')
    content_frame.pack(expand=True)

    # Start the GUI main loop
    window.mainloop()

    # Ensure that the window is destroyed after the main loop exits
    window.destroy()

###########################################################################

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

###########################################
# Function to delete a file by its ID
def delete_file_by_id(file_id, is_encrypted=True):
    user_id = database.get_current_user_id()
    database.delete_file_by_id(file_id, user_id, is_encrypted)
###########################################
def delete_file_by_id(file_id, user_id, is_encrypted=True):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Determine the table based on the encryption status
        table_name = "decrypted_files" if is_encrypted else "encrypted_files"

        # Delete the file from the table
        delete_query = f"DELETE FROM {table_name} WHERE file_id = %s AND user_id = %s"
        cursor.execute(delete_query, (file_id, user_id))

        # Commit the changes and close the connection
        connection.commit()
    except Exception as e:
        print(f"Error deleting file: {e}")
    finally:
        connection.close()

############################################
# Function to create the content for Encrypt/Decrypt Files page
def encrypt_decrypt_page():
    global selected_file_label  # Declare as global to update text in select_file function
    if not hasattr(encrypt_decrypt_page, "first_run"):
        encrypt_decrypt_page.first_run = True

        # Create a title label
        title_label = Label(content_frame, text="Encrypt/Decrypt Files", bg='light blue', font=("Arial", 16, "bold"))
        title_label.pack(pady=(100, 50))  # Added padding for top and bottom to center vertically

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
        encrypt_button.pack(side=LEFT, padx=10)
        decrypt_button.pack(side=LEFT, padx=10)