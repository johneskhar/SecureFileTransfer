from tkinter import *
from tkinter import messagebox
import mysql.connector
from user_management import UserManagement
import subprocess
import logging
import pyotp
import homepage
from tkinter import Toplevel, Label

# Database configuration
db_config = {
    "host": "localhost",
    "port": "3306",
    "user": "root",
    "password": "johnes24",
    "database": "secure_file_transfer",
}

# Initialize the UserManagement class for database operations
user_manager = UserManagement(db_config)

# Function to perform user login with 2FA
def login_2fa(username, password):
    def verify_2fa_code():
        entered_code = "".join(entry.get() for entry in code_entries)  # Get the entered 2FA code

        # Validate the entered code (you can add more validation here)
        if len(entered_code) == 6 and entered_code.isdigit():
            # Call a function to verify the 2FA code in your user management module
            # Replace this with your actual verification logic
            verification_result = user_manager.verify_2fa_code(username, entered_code)

            if verification_result:
                messagebox.showinfo("Success", "2FA code is correct.")
                window.destroy()  # Close the verification window on success
                open_homepage(username)  # Open the homepage with the username
            else:
                messagebox.showerror("Error", "Incorrect 2FA code. Please try again.")
                window.lift()  # Bring the window to the front again on incorrect code
                window.grab_set()  # Keep the window in front
        else:
            messagebox.showerror("Error", "Invalid 2FA code format. Please enter a 6-digit code.")
            window.lift()  # Bring the window to the front again on invalid input
            window.grab_set()  # Keep the window in front

    def open_homepage(username):
        # Use subprocess to open the homepage.py script as a separate process
        subprocess.Popen(["C:/Users/calie/AppData/Local/Microsoft/WindowsApps/python.exe",
                          "C:/Users/calie/PycharmProjects/FYP_Test1/homepage.py", username])
        window.destroy()

    # Create a new Toplevel window for 2FA verification
    window = Toplevel()
    window.title("2FA Verification")
    window.geometry('400x150')  # Set the window size
    window.geometry(f"+{window.winfo_screenwidth() // 2 - 200}+{window.winfo_screenheight() // 2 - 150}")  # Center the window

    # Create separate boxes for each digit of the 2FA code
    code_frame = Frame(window)
    code_frame.pack(pady=20)

    code_entries = []
    for i in range(6):
        entry = Entry(code_frame, width=3, font=('Arial', 20), justify='center')
        entry.grid(row=0, column=i, padx=5)

        # Limit the input to a single character and allow deletion
        entry.config(validate="key", validatecommand=(entry.register(lambda char: len(char) <= 1), "%P"))

        code_entries.append(entry)

    # Create a Submit button with a modern look
    submit_button = Button(window, text="Submit", command=verify_2fa_code, bg='#57a1f8', fg='white', font=('Arial', 13))
    submit_button.pack()

# Function to perform user login
def login():
    username = login_user.get()
    password = login_password.get()

    success, secret_key, logged_in_username = user_manager.login_user(username, password)

    if success:
        if secret_key:
            # 2FA is required, open the 2FA window
            login_2fa(username, password)
        else:
            # 2FA is not required, set the current_username and open the homepage directly
            homepage.current_username = logged_in_username  # Set the username in homepage.py
            open_homepage(username)  # Pass the username as an argument
    else:
        messagebox.showerror('Error', 'Incorrect Username or Password')


# Function to toggle password visibility
def toggle_password_visibility():
    if login_password_visible.get():
        login_password.config(show='')  # Show the password
    else:
        login_password.config(show='*')  # Hide the password

# Create the GUI window
window = Tk()
window.title("Login")
window.geometry('925x500+300+200')
window.configure(bg='#fff')
window.resizable(False, False)

img = PhotoImage(file="C:/Users/calie/PycharmProjects/FYP_Test1/sft pic.png")
Label(window, image=img, border=0, bg='white').place(x=50, y=90)

frame = Frame(window, width=350, height=500, bg='#fff')
frame.place(x=480, y=50)

heading = Label(frame, text='Sign In', fg="#57a1f8", bg='white', font=('Microsoft Yahei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

# Username Entry
def on_enter_login_user(e):
    if login_user.get() == 'Username':
        login_user.delete(0, 'end')
        login_user.config(fg='black')

def on_leave_login_user(e):
    if login_user.get() == '':
        login_user.insert(0, 'Username')
        login_user.config(fg='grey')

login_user = Entry(frame, width=25, fg='grey', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
login_user.place(x=30, y=80)
login_user.insert(0, 'Username')
login_user.bind("<FocusIn>", on_enter_login_user)
login_user.bind("<FocusOut>", on_leave_login_user)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

# Password Entry
login_password_visible = BooleanVar()  # Variable to track password visibility
login_password = Entry(frame, width=25, fg='grey', border=0, bg='white', font=('Microsoft Yahei UI Light', 11), show='*')
login_password.place(x=30, y=150)
login_password.insert(0, 'Password')
login_password.bind("<FocusIn>", lambda e: login_password.delete(0, 'end') if login_password.get() == 'Password' else None)
login_password.bind("<FocusOut>", lambda e: login_password.insert(0, 'Password') if login_password.get() == '' else None)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

# Create a button-like Checkbutton widget for showing/hiding the password
show_password_button = Checkbutton(frame, text="Show Password", variable=login_password_visible, command=toggle_password_visibility, bg='white')
show_password_button.place(x=30, y=185)

# Login Button
Button(frame, width=39, pady=7, text='Login', bg='#57a1f8', fg='white', border=0, command=login).place(x=35, y=220)

# Signup Label
label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft Yahei UI Light', 9))
label.place(x=80, y=280)

def open_register_script():
    subprocess.Popen(["C:/Users/calie/AppData/Local/Microsoft/WindowsApps/python.exe", "C:/Users/calie/PycharmProjects/FYP_Test1/registeruser.py"])
    window.destroy()  # Close the register window

# Signup Button
signup_button = Button(frame, width=6, text='Sign Up', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=open_register_script)
signup_button.place(x=220, y=280)

# Main loop
window.mainloop()
