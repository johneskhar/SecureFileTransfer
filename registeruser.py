from tkinter import *
from tkinter import messagebox
import mysql.connector
from user_management import UserManagement  # Assuming user_management.py contains your UserManagement class
import subprocess
import re
import pyotp
import qrcode
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

# Email regex pattern
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

def show_qr_code():
    # Create a new popup window
    popup = Toplevel(window)
    popup.title("2FA QR Code")

    # Add a Label with explanatory text
    Label(popup, text="Scan the QR code below with your 2FA app to activate your account.", padx=20, pady=20).pack()

    # Load and display the QR code image
    qr_image = PhotoImage(file="qr_code.png")
    Label(popup, image=qr_image).pack()

    # Run the popup window
    popup.mainloop()

# Function to perform user registration
def signup():
    email = mail.get()
    username = user.get()
    password = code.get()
    confirm_password = confirm_code.get()

    # Regular expression pattern to validate email format
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not (email and username and password and confirm_password):
        messagebox.showerror('Error', 'All fields are required.')
    elif not re.match(email_pattern, email):
        messagebox.showerror('Error', 'Invalid email format. Please use example@example.com format.')
    elif password != confirm_password:
        messagebox.showerror('Error', 'Passwords do not match.')
    elif user_manager.username_exists(username):
        messagebox.showerror('Error', 'Username already exists. Please choose a different username.')
    elif user_manager.email_exists(email):
        messagebox.showerror('Error', 'Email already exists. Please use a different email address.')
    else:
        # Call the register_user method and get the secret key as a return value
        success, message, secret_key = user_manager.register_user(username, password, email)

        if success:
            # Generate the provisioning URL from the retrieved secret key
            provisioning_url = pyotp.totp.TOTP(secret_key).provisioning_uri(email, issuer_name="Secure File Transfer")

            # Create a QR code from the provisioning URL (optional)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(provisioning_url)
            qr.make(fit=True)

            # Save the QR code as an image (optional)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("qr_code.png")

            messagebox.showinfo('Signup', 'Successfully Sign Up')
            # Clear the text fields after successful registration
            mail.delete(0, 'end')
            user.delete(0, 'end')
            code.delete(0, 'end')
            confirm_code.delete(0, 'end')
            # Show the QR code in a popup window
            show_qr_code()
        else:
            messagebox.showerror('Error', message)
            # Remove the QR code image if registration fails
            os.remove("qr_code.png")


# Create the GUI window
window = Tk()
window.title("Signup")
window.geometry('925x500+300+200')
window.configure(bg='#fff')
window.resizable(False, False)


img = PhotoImage(file="C:/Users/calie/PycharmProjects/FYP_Test1/sft pic.png")
Label(window, image=img, border=0, bg='white').place(x=50, y=90)

frame = Frame(window, width=350, height=500, bg='#fff')
frame.place(x=480, y=50)

heading = Label(frame, text='Sign Up', fg="#57a1f8", bg='white', font=('Microsoft Yahei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

# Email Address
def on_enter_email(e):
    if mail.get() == 'Email Address':
        mail.delete(0, 'end')
        mail.config(fg='black')

def on_leave_email(e):
    if mail.get() == '':
        mail.insert(0, 'Email Address')
        mail.config(fg='grey')

mail = Entry(frame, width=25, fg='grey', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
mail.place(x=30, y=80)
mail.insert(0, 'Email Address')
mail.bind("<FocusIn>", on_enter_email)
mail.bind("<FocusOut>", on_leave_email)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

# Username
def on_enter_user(e):
    if user.get() == 'Username':
        user.delete(0, 'end')
        user.config(fg='black')

def on_leave_user(e):
    if user.get() == '':
        user.insert(0, 'Username')
        user.config(fg='grey')

user = Entry(frame, width=25, fg='grey', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
user.place(x=30, y=150)
user.insert(0, 'Username')
user.bind("<FocusIn>", on_enter_user)
user.bind("<FocusOut>", on_leave_user)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

# Password
def on_enter_password(e):
    if code.get() == 'Password':
        code.delete(0, 'end')
        code.config(fg='black', show='*')

def on_leave_password(e):
    if code.get() == '':
        code.insert(0, 'Password')
        code.config(fg='grey', show='')

code = Entry(frame, width=25, fg='grey', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
code.place(x=30, y=220)
code.insert(0, 'Password')
code.bind("<FocusIn>", on_enter_password)
code.bind("<FocusOut>", on_leave_password)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)

password_visible = BooleanVar()  # Variable to track password visibility

def toggle_password_visibility():
    if password_visible.get():
        code.config(show='')  # Show the password
    else:
        code.config(show='*')  # Hide the password

code = Entry(frame, width=25, fg='grey', border=0, bg='white', font=('Microsoft Yahei UI Light', 11), show='*')
code.place(x=30, y=220)
code.insert(0, 'Password')
code.bind("<FocusIn>", on_enter_password)
code.bind("<FocusOut>", on_leave_password)

password_show_hide_button = Checkbutton(frame, text='View Password', variable=password_visible, command=toggle_password_visibility, bg='white')
password_show_hide_button.place(x=30, y=250)

# Confirm Password
def on_enter_confirm_password(e):
    if confirm_code.get() == 'Confirm Password':
        confirm_code.delete(0, 'end')
        confirm_code.config(fg='black', show='*')

def on_leave_confirm_password(e):
    if confirm_code.get() == '':
        confirm_code.insert(0, 'Confirm Password')
        confirm_code.config(fg='grey', show='')

confirm_code = Entry(frame, width=25, fg='grey', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
confirm_code.place(x=30, y=290)
confirm_code.insert(0, 'Confirm Password')
confirm_code.bind("<FocusIn>", on_enter_confirm_password)
confirm_code.bind("<FocusOut>", on_leave_confirm_password)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=317)

# Sign Up Button
Button(frame, width=39, pady=7, text='Sign Up', bg='#57a1f8', fg='white', border=0, command=signup).place(x=35, y=350)

# I have an account Label
label = Label(frame, text='I have an account', fg='black', bg='white', font=('Microsoft Yahei UI Light', 9))
label.place(x=90, y=410)

# Function to open the register script and close the login script
def open_login_script():
    subprocess.Popen(["C:/Users/calie/AppData/Local/Microsoft/WindowsApps/python.exe", "C:/Users/calie/PycharmProjects/FYP_Test1/loginuser.py"])
    window.destroy()  # Close the register window

# Sign In Button
signin = Button(frame, width=6, text='Sign In', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=open_login_script)
signin.place(x=200, y=410)

# Main loop
window.mainloop()
