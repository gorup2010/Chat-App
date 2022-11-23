import socket
import threading
import tkinter
from tkinter import simpledialog
import tkinter.scrolledtext

login = tkinter.Tk()
login.title('Đăng nhập')
login.geometry('250x200')

label = tkinter.Label(master=login ,text='Tên người dùng', font=20)
label.pack(pady=15)

username_entry = tkinter.Entry(master=login ,background='white', width=20, font=17)
username_entry.pack(pady=15)

frm_button = tkinter.Frame(master=login)
frm_button.pack(pady=10)

btn_login = tkinter.Button(master=frm_button, text='Đăng nhập', width=10)
btn_login.grid(column=1,row=1, padx=10)

btn_signup = tkinter.Button(master=frm_button, text='Đăng kí', width=10)
btn_signup.grid(column=2,row=1, padx=10)

def pro():
    print("DDDDDD")
    login.destroy()

login.protocol("WM_DELETE_WINDOW", pro)
login.mainloop()

