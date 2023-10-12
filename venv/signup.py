from tkinter import *
from tkinter import messagebox
import ast

window=Tk()
window.title("Signup")
window.geometry('925x500+300+200')
window.configure(bg='#fff')
window.resizable(False,False)

def signup():
    email=mail.get()
    username=user.get()
    password=code.get()
    confirm_password=confirm_code.get()

    if password==confirm_password:
        try:
            file=open('datasheet.txt','r+')
            d=file.read()
            r=ast.literal_eval(d)

            dict2={username:password}
            r.update(dict2)
            file.truncate(0)
            file.close()

            file.open('datasheet.txt','w')
            w=file.write(str(r))

            messagebox.showinfo('Signup','Successfully Sign Up')

        except:
            file=open('datasheet.txt','w')
            pp=str({'Username':'password'})
            file.write(pp)
            file.close()
    else:
        messagebox:showerror('Invalid',"Both Password should match")


img = PhotoImage(file="C:/Users/calie/PycharmProjects/FYP_Test1/login.gif")
Label(window,image=img,border=0,bg='white').place(x=50,y=90)

frame=Frame(window,width=350,height=500,bg='#fff')
frame.place(x=480,y=50)

heading=Label(frame,text='Sign Up',fg="#57a1f8",bg='white',font=('Microsoft Yahei UI Light',23, 'bold'))
heading.place(x=100,y=5)

##############################################################################
#Email Address
def on_enter(e):
    mail.delete(0,'end')
def on_leave(e):
    if mail.get()=='':
        mail.insert(0,'Email Address')

mail = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
mail.place(x=30,y=80)
mail.insert(0, 'Email Address')
mail.bind("<FocusIn>",on_enter)
mail.bind("<FocusOut>",on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

##############################################################################
#Username
def on_enter(e):
    user.delete(0,'end')
def on_leave(e):
    if user.get()=='':
        user.insert(0,'Username')

user = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
user.place(x=30,y=150)
user.insert(0, 'Username')
user.bind("<FocusIn>",on_enter)
user.bind("<FocusOut>",on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

##############################################################################
#Password
def on_enter(e):
    code.delete(0,'end')
def on_leave(e):
    if code.get()=='':
        code.insert(0,'Password')

code = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
code.place(x=30,y=220)
code.insert(0, 'Password')
code.bind("<FocusIn>",on_enter)
code.bind("<FocusOut>",on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)

##############################################################################
#Confirm Password
def on_enter(e):
    confirm_code.delete(0,'end')
def on_leave(e):
    if confirm_code.get()=='':
        confirm_code.insert(0,'Confirm Password')

confirm_code = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
confirm_code.place(x=30,y=290)
confirm_code.insert(0, 'Confirm Password')
confirm_code.bind("<FocusIn>",on_enter)
confirm_code.bind("<FocusOut>",on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=317)

##############################################################################

Button(frame,width=39,pady=7,text='Sign Up',bg='#57a1f8',fg='white',border=0,command=signup).place(x=35,y=350)
label=Label(frame,text='I have an account',fg='black',bg='white',font=('Microsoft Yahei UI Light',9))
label.place(x=90,y=410)

signin=Button(frame,width=6,text='Sign In',border=0,bg='white',cursor='hand2',fg='#57a1f8')
signin.place(x=200,y=410)


##############################################################################

window.mainloop()