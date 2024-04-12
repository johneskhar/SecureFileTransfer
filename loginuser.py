from tkinter import *
from tkinter import messagebox
import subprocess
from tkinter import Toplevel, Label, Entry
from user_management import UserManagement

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


# Function to perform user login
def login():
    username = login_user.get()
    password = login_password.get()

    # Attempt to log in the user
    success, secret_key, logged_in_username = user_manager.login_user(username, password)

    if success:
        # If login is successful, prompt for 2FA code
        verification_window = Toplevel()
        verification_window.title("2FA Verification")
        verification_window.geometry('400x150')
        verification_window.geometry(
            f"+{verification_window.winfo_screenwidth() // 2 - 200}+"
            f"{verification_window.winfo_screenheight() // 2 - 150}")

        code_frame = Frame(verification_window)
        code_frame.pack(pady=20)

        code_entries = []
        for i in range(6):
            entry = Entry(code_frame, width=3, font=('Arial', 20), justify='center')
            entry.grid(row=0, column=i, padx=5)
            entry.config(validate="key", validatecommand=(entry.register(lambda char: len(char) <= 1), "%P"))
            code_entries.append(entry)

        submit_button = Button(verification_window, text="Submit",
                               command=lambda: verify_2fa_code(username, code_entries, verification_window, window),
                               bg='#57a1f8', fg='white', font=('Arial', 13))
        submit_button.pack()

    else:
        messagebox.showerror('Error', 'Incorrect Username or Password')


# Function to verify 2FA code
def verify_2fa_code(username, code_entries, verification_window, login_window):
    entered_code = "".join(entry.get() for entry in code_entries)

    if len(entered_code) == 6 and entered_code.isdigit():
        verification_result = user_manager.verify_2fa_code(username, entered_code)

        if verification_result:
            messagebox.showinfo("Success", "2FA code is correct.")
            print("About to call open_homepage for user:", username)
            open_homepage(username, verification_window, login_window)
        else:
            messagebox.showerror("Error", "Incorrect 2FA code. Please try again.")
            verification_window.lift()
            verification_window.grab_set()
    else:
        messagebox.showerror("Error", "Invalid 2FA code format. Please enter a 6-digit code.")
        verification_window.lift()
        verification_window.grab_set()


# Function to open the homepage with the username argument
def open_homepage(username, verification_window, login_window):
    current_user_id = user_manager.get_user_id_by_username(username)

    print("Inside open_homepage function")

    verification_window.withdraw()  # Hide the verification window

    # Define a function to destroy the login window after a delay
    def destroy_login_window():
        login_window.destroy()

    # Use the open_homepage function from homepage.py instead of opening a new instance of the script
    subprocess.Popen([
        "C:/Users/calie/AppData/Local/Microsoft/WindowsApps/python.exe",
        "C:/Users/calie/PycharmProjects/FYP_Test1/homepage.py",
        username,
        str(verification_window),
        "destroy_login_window"  # Pass the destroy_login_window function as a string argument
    ])


# Create the GUI window
window = Tk()
window.title("Login")
window.geometry('925x500+300+200')
window.configure(bg='#fff')
window.resizable(False, False)


# Function to toggle password visibility
def toggle_password_visibility():
    if login_password_visible.get():
        login_password.config(show='')  # Show the password
    else:
        login_password.config(show='*')  # Hide the password


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
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

# Password Entry
login_password_visible = BooleanVar()  # Variable to track password visibility
login_password = Entry(frame, width=25, fg='grey', border=0, bg='white', font=('Microsoft Yahei UI Light', 11),
                       show='*')
login_password.place(x=30, y=150)
login_password.insert(0, 'Password')
login_password.bind("<FocusIn>",
                    lambda e: login_password.delete(0, 'end') if login_password.get() == 'Password' else None)
login_password.bind("<FocusOut>",
                    lambda e: login_password.insert(0, 'Password') if login_password.get() == '' else None)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

# Create a button-like Checkbutton widget for showing/hiding the password
show_password_button = Checkbutton(frame, text="Show Password", variable=login_password_visible,
                                   command=toggle_password_visibility, bg='white')
show_password_button.place(x=30, y=185)

# Login Button
Button(frame, width=39, pady=7, text='Login', bg='#57a1f8', fg='white', border=0, command=login).place(x=35, y=220)

# Signup Label
label = Label(frame, text="Don't have an account?", fg='black', bg='white',
              font=('Microsoft Yahei UI Light', 9))
label.place(x=80, y=280)


def open_register_script():
    subprocess.Popen(
        ["C:/Users/calie/AppData/Local/Microsoft/WindowsApps/python.exe",
         "C:/Users/calie/PycharmProjects/FYP_Test1/registeruser.py"])
    window.destroy()  # Close the register window


# Signup Button
signup_button = Button(frame, width=6, text='Sign Up', border=0, bg='white', cursor='hand2', fg='#57a1f8',
                       command=open_register_script)
signup_button.place(x=220, y=280)

# Main loop
window.mainloop()
